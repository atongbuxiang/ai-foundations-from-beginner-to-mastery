#!/usr/bin/env node

/**
 * Audit the teaching unit around every active Obsidian image embed.
 *
 * A formal figure must follow this sequence:
 * visual question -> image -> figure callout with provenance -> read-back ->
 * explicit boundary ("the figure does not prove...").  The checker ignores
 * fenced code blocks and accepts a short adjacent gallery as one figure unit.
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
    if ([".git", "node_modules", ".obsidian"].includes(entry.name)) continue;
    const fullPath = path.join(directory, entry.name);
    if (entry.isDirectory()) files.push(...walk(fullPath));
    else if (entry.isFile() && entry.name.endsWith(".md")) files.push(fullPath);
  }
  return files;
}

function visibleLines(markdownPath) {
  const raw = fs.readFileSync(markdownPath, "utf8").split(/\r?\n/);
  const visible = raw.map(() => "");
  let fenceCharacter = null;

  for (let index = 0; index < raw.length; index += 1) {
    const line = raw[index];
    const fence = line.match(/^\s*(`{3,}|~{3,})/);
    if (fence) {
      const character = fence[1][0];
      if (fenceCharacter === null) fenceCharacter = character;
      else if (fenceCharacter === character) fenceCharacter = null;
      continue;
    }
    if (fenceCharacter === null) visible[index] = line;
  }
  return visible;
}

function embedsInLine(line) {
  const embeds = [];
  const pattern = /!\[\[([^\]\n]+)\]\]/g;
  for (const match of line.matchAll(pattern)) {
    if (match.index > 0 && line[match.index - 1] === "\\") continue;
    const fields = match[1].split("|").map((field) => field.trim());
    embeds.push({
      target: fields[0],
      width: fields.length > 1 ? fields.at(-1) : null,
      numericWidth: fields.length > 1 && /^\d+(?:\.\d+)?$/.test(fields.at(-1)),
    });
  }
  return embeds;
}

function findIndex(lines, start, end, pattern) {
  for (let index = start; index < Math.min(end, lines.length); index += 1) {
    if (pattern.test(lines[index])) return index;
  }
  return -1;
}

function calloutText(lines, start) {
  if (start < 0) return "";
  const block = [];
  for (let index = start; index < lines.length; index += 1) {
    if (!/^\s*>/.test(lines[index])) break;
    block.push(lines[index]);
  }
  return block.join("\n");
}

function paragraphText(lines, start) {
  if (start < 0) return "";
  const block = [];
  for (let index = start; index < lines.length; index += 1) {
    const line = lines[index];
    if (index > start && (line.trim() === "" || /^#{1,6}\s/.test(line))) break;
    block.push(line);
  }
  return block.join("\n");
}

const questionPattern = /(先.{0,12}(?:看|用|读).{0,12}图|图.{0,10}(?:回答|观察|问题)|(?:为什么|为何|怎样|如何|什么|哪|是否|能否|何时|哪里|多大|究竟)).{0,260}[？?]/s;
const provenancePattern = /(来源|图源与(?:生成|改绘)|生成脚本|\*\*生成[:：]|生成[:：]|原作|数据来源)[:：]?/i;

const records = [];
for (const markdownPath of walk(root)) {
  const lines = visibleLines(markdownPath);
  for (let lineIndex = 0; lineIndex < lines.length; lineIndex += 1) {
    for (const embed of embedsInLine(lines[lineIndex])) {
      const before = lines.slice(Math.max(0, lineIndex - 18), lineIndex).join("\n");
      const captionIndex = findIndex(lines, lineIndex + 1, lineIndex + 17, /\[!figure\]/i);
      const readIndex = findIndex(lines, lineIndex + 1, lineIndex + 56, /(怎样读图|如何读图|读图路径|读图说明)/);
      const boundaryIndex = findIndex(lines, lineIndex + 1, lineIndex + 56, /(适用边界|图没有证明什么)/);
      const caption = calloutText(lines, captionIndex);
      const readBack = paragraphText(lines, readIndex);
      const boundary = paragraphText(lines, boundaryIndex);
      const templatePlaceholder = markdownPath.includes(`${path.sep}_templates${path.sep}`)
        && embed.target.endsWith("/待填写.svg");

      const checks = {
        numericWidth: embed.numericWidth,
        visualQuestion: questionPattern.test(before),
        figureCaption: captionIndex >= 0,
        captionSubstantive: caption.replace(/\s/g, "").length >= 50,
        provenance: provenancePattern.test(caption),
        readBack: readIndex > captionIndex && readBack.replace(/\s/g, "").length >= 45,
        explicitBoundary: boundaryIndex > readIndex && boundary.replace(/\s/g, "").length >= 45,
      };
      records.push({
        file: path.relative(root, markdownPath),
        line: lineIndex + 1,
        ...embed,
        templatePlaceholder,
        checks,
        pass: Object.values(checks).every(Boolean),
      });
    }
  }
}

const failed = records.filter((record) => !record.pass);
const summary = {
  markdownFilesWithFigures: new Set(records.map((record) => record.file)).size,
  figureEmbeds: records.length,
  templatePlaceholders: records.filter((record) => record.templatePlaceholder).length,
  passed: records.length - failed.length,
  failed: failed.length,
};

if (jsonMode) {
  process.stdout.write(`${JSON.stringify({ summary, records }, null, 2)}\n`);
} else {
  process.stdout.write(`Markdown files with figures: ${summary.markdownFilesWithFigures}\n`);
  process.stdout.write(`Figure embeds: ${summary.figureEmbeds}\n`);
  process.stdout.write(`Template placeholders: ${summary.templatePlaceholders}\n`);
  process.stdout.write(`Passed figure units: ${summary.passed}\n`);
  process.stdout.write(`Failed figure units: ${summary.failed}\n`);
  if (failed.length > 0) {
    process.stdout.write("\nFailed figure units:\n");
    for (const record of failed) {
      const missing = Object.entries(record.checks)
        .filter(([, passed]) => !passed)
        .map(([name]) => name)
        .join(", ");
      process.stdout.write(`- ${record.file}:${record.line} -> ${record.target} (${missing})\n`);
    }
  }
}

if (failMode && failed.length > 0) process.exitCode = 1;
