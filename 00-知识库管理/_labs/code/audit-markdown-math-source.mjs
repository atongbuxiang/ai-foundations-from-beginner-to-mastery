#!/usr/bin/env node

/**
 * Audit high-confidence Markdown/TeX source corruption.
 *
 * This is deliberately conservative: it catches control bytes and command
 * names whose missing backslash is very likely a rendering error, while
 * leaving ordinary prose and legitimate multi-letter variables alone.
 */

import fs from "node:fs";
import path from "node:path";

const args = process.argv.slice(2);
const jsonMode = args.includes("--json");
const failMode = args.includes("--fail");
const rootArg = args.find((arg) => !arg.startsWith("--")) ?? ".";
const root = path.resolve(rootArg);

function walk(directory) {
  const files = [];
  for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
    if ([".git", "node_modules", ".obsidian", "__pycache__"].includes(entry.name)) continue;
    const fullPath = path.join(directory, entry.name);
    if (entry.isDirectory()) files.push(...walk(fullPath));
    else if (entry.isFile() && entry.name.endsWith(".md")) files.push(fullPath);
  }
  return files;
}

function stripInlineCode(line) {
  return line.replace(/`+[^`]*`+/g, "");
}

function inlineMathSegments(line) {
  const segments = [];
  let start = -1;
  for (let index = 0; index < line.length; index += 1) {
    if (line[index] !== "$" || (index > 0 && line[index - 1] === "\\")) continue;
    if (line[index + 1] === "$" || line[index - 1] === "$") continue;
    if (start < 0) start = index + 1;
    else {
      segments.push(line.slice(start, index));
      start = -1;
    }
  }
  return segments;
}

const commandPatterns = [
  {
    kind: "missing-structural-command",
    pattern: /(?<![\\A-Za-z])(?:qquad|quad|operatorname|mathcal|mathbb|mathrm|mathbf|boldsymbol)(?=\s|\{|[A-Z])/g,
  },
  {
    kind: "missing-fraction-or-root-command",
    pattern: /(?<![\\A-Za-z])(?:frac|tfrac|dfrac|sqrt)(?=\s|\{|\d|\\)/g,
  },
  {
    kind: "missing-delimiter-command",
    pattern: /(?<![\\A-Za-z])(?:left|right)(?=\s*[\(\[\]|]|\s*\\(?:l|r)?(?:floor|ceil|vert|Vert))/g,
  },
  {
    kind: "missing-accent-command",
    pattern: /(?<![\\A-Za-z])(?:widehat|widetilde|tilde)(?=\s|\{)/g,
  },
  {
    kind: "missing-greek-command",
    pattern: /(?<![\\A-Za-z])(?:theta|lambda|alpha|epsilon|varepsilon|rho|sigma|tau|phi|psi|mu|kappa)(?=\s*(?:_|\(|=|\}|,))/g,
  },
];

function scanMath(text, file, line, findings) {
  for (const { kind, pattern } of commandPatterns) {
    pattern.lastIndex = 0;
    for (const match of text.matchAll(pattern)) {
      findings.push({
        file,
        line,
        kind,
        token: match[0],
        excerpt: text.trim().slice(0, 220),
      });
    }
  }
}

const findings = [];
let filesScanned = 0;

for (const markdownPath of walk(root)) {
  filesScanned += 1;
  const relative = path.relative(root, markdownPath);
  const raw = fs.readFileSync(markdownPath);
  const text = raw.toString("utf8");

  for (let index = 0; index < raw.length; index += 1) {
    const byte = raw[index];
    if ([0x0b, 0x0c, 0x0d].includes(byte)) {
      const line = raw.subarray(0, index).toString("utf8").split("\n").length;
      findings.push({ file: relative, line, kind: "forbidden-control-byte", token: `0x${byte.toString(16).padStart(2, "0")}` });
    }
  }
  for (const match of text.matchAll(/\t(?:heta|ext|frac|au|o|ilde)/g)) {
    const line = text.slice(0, match.index).split("\n").length;
    findings.push({ file: relative, line, kind: "tab-corrupted-command", token: JSON.stringify(match[0]) });
  }

  const lines = text.split(/\n/);
  let fenceCharacter = null;
  let mathBlock = false;
  let blockStart = null;

  for (let index = 0; index < lines.length; index += 1) {
    const lineNumber = index + 1;
    const line = lines[index];
    const fence = line.match(/^\s*(`{3,}|~{3,})/);
    if (fence) {
      const character = fence[1][0];
      if (fenceCharacter === null) fenceCharacter = character;
      else if (fenceCharacter === character) fenceCharacter = null;
      continue;
    }
    if (fenceCharacter !== null) continue;

    const visible = stripInlineCode(line);
    let cursor = 0;
    let marker = visible.indexOf("$$", cursor);
    while (marker >= 0) {
      const segment = visible.slice(cursor, marker).replace(/^\s*>\s?/, "");
      if (mathBlock) scanMath(segment, relative, lineNumber, findings);
      else for (const inline of inlineMathSegments(segment)) scanMath(inline, relative, lineNumber, findings);

      mathBlock = !mathBlock;
      if (mathBlock) blockStart = lineNumber;
      else blockStart = null;
      cursor = marker + 2;
      marker = visible.indexOf("$$", cursor);
    }

    const tail = visible.slice(cursor).replace(/^\s*>\s?/, "");
    if (mathBlock) scanMath(tail, relative, lineNumber, findings);
    else for (const inline of inlineMathSegments(tail)) scanMath(inline, relative, lineNumber, findings);
  }

  if (mathBlock) {
    findings.push({ file: relative, line: blockStart, kind: "unclosed-display-math", token: "$$" });
  }
}

const byKind = Object.fromEntries(
  [...new Set(findings.map((finding) => finding.kind))]
    .sort()
    .map((kind) => [kind, findings.filter((finding) => finding.kind === kind).length]),
);
const summary = { filesScanned, findings: findings.length, byKind };

if (jsonMode) {
  process.stdout.write(`${JSON.stringify({ summary, findings }, null, 2)}\n`);
} else {
  process.stdout.write(`Markdown files scanned: ${filesScanned}\n`);
  process.stdout.write(`Math-source findings: ${findings.length}\n`);
  for (const [kind, count] of Object.entries(byKind)) process.stdout.write(`- ${kind}: ${count}\n`);
  if (findings.length > 0) {
    process.stdout.write("\nFindings:\n");
    for (const finding of findings) {
      const excerpt = finding.excerpt ? ` -> ${finding.excerpt}` : "";
      process.stdout.write(`- ${finding.file}:${finding.line} [${finding.kind}] ${finding.token}${excerpt}\n`);
    }
  }
}

if (failMode && findings.length > 0) process.exitCode = 1;
