#!/usr/bin/env node

/** Audit active Obsidian wiki links against file names, rooted paths and aliases. */

import fs from "node:fs";
import path from "node:path";

const args = process.argv.slice(2);
const jsonMode = args.includes("--json");
const failMode = args.includes("--fail");
const includePrefix = args.find((arg) => arg.startsWith("--include-prefix="))?.split("=", 2)[1] ?? null;
const rootArg = args.find((arg) => !arg.startsWith("--")) ?? ".";
const root = path.resolve(rootArg);

function walk(directory) {
  const files = [];
  for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
    if ([".git", "node_modules", ".obsidian", "__pycache__"].includes(entry.name)) continue;
    const fullPath = path.join(directory, entry.name);
    if (entry.isDirectory()) files.push(...walk(fullPath));
    else if (entry.isFile()) files.push(fullPath);
  }
  return files;
}

function relative(file) {
  return path.relative(root, file).split(path.sep).join("/");
}

function add(index, key, file) {
  if (!key) return;
  const values = index.get(key) ?? new Set();
  values.add(file);
  index.set(key, values);
}

function aliases(markdown) {
  if (!markdown.startsWith("---\n")) return [];
  const end = markdown.indexOf("\n---", 4);
  if (end < 0) return [];
  const match = markdown.slice(4, end).match(/^aliases:\s*(.*)$/m);
  if (!match) return [];
  const raw = match[1].trim();
  if (raw.startsWith("[") && raw.endsWith("]")) {
    return raw.slice(1, -1).split(",").map((item) => item.trim().replace(/^['"]|['"]$/g, "")).filter(Boolean);
  }
  return raw ? [raw.replace(/^['"]|['"]$/g, "")] : [];
}

function activeTargets(markdown) {
  const targets = [];
  const lines = markdown.split(/\r?\n/);
  let fenceCharacter = null;

  for (let index = 0; index < lines.length; index += 1) {
    const line = lines[index];
    const fence = line.match(/^\s*(`{3,}|~{3,})/);
    if (fence) {
      const character = fence[1][0];
      if (fenceCharacter === null) fenceCharacter = character;
      else if (fenceCharacter === character) fenceCharacter = null;
      continue;
    }
    if (fenceCharacter !== null) continue;

    const visible = line.replace(/`+[^`]*`+/g, "");
    const pattern = /(?<!!)\[\[([^\]\n]+)\]\]/g;
    for (const match of visible.matchAll(pattern)) {
      const target = match[1].split(/\\?\|/, 1)[0].replace(/\\\|/g, "|").split("#", 1)[0].trim();
      if (target) targets.push({ target, line: index + 1 });
    }
  }
  return targets;
}

const allFiles = walk(root);
const byKey = new Map();
const byAlias = new Map();

for (const file of allFiles) {
  const rel = relative(file);
  add(byKey, path.basename(file), file);
  add(byKey, path.parse(file).name, file);
  add(byKey, rel, file);
  add(byKey, rel.replace(/\.md$/i, ""), file);
  if (file.endsWith(".md")) {
    const markdown = fs.readFileSync(file, "utf8");
    for (const alias of aliases(markdown)) add(byAlias, alias, file);
  }
}

function resolve(target) {
  if (target.includes("/")) {
    const direct = path.join(root, target);
    const candidates = [direct, target.endsWith(".md") ? direct : `${direct}.md`].filter((file) => fs.existsSync(file));
    if (candidates.length > 0) return [...new Set(candidates)];
  }

  const keys = [target, target.endsWith(".md") ? target.slice(0, -3) : `${target}.md`, path.basename(target)];
  const candidates = new Set();
  for (const key of keys) {
    for (const file of byKey.get(key) ?? []) candidates.add(file);
    for (const file of byAlias.get(key) ?? []) candidates.add(file);
  }
  return [...candidates];
}

const records = [];
const markdownFiles = allFiles.filter((file) => file.endsWith(".md") && (!includePrefix || relative(file).startsWith(includePrefix)));
for (const file of markdownFiles) {
  const markdown = fs.readFileSync(file, "utf8");
  for (const link of activeTargets(markdown)) {
    const matches = resolve(link.target);
    records.push({
      file: relative(file),
      ...link,
      resolution: matches.length === 0 ? "missing" : matches.length === 1 ? "unique" : "ambiguous",
      matches: matches.map(relative).sort(),
    });
  }
}

const missing = records.filter((record) => record.resolution === "missing");
const ambiguous = records.filter((record) => record.resolution === "ambiguous");
const summary = {
  markdownFilesScanned: markdownFiles.length,
  wikiLinks: records.length,
  unique: records.length - missing.length - ambiguous.length,
  missing: missing.length,
  ambiguous: ambiguous.length,
};

if (jsonMode) {
  process.stdout.write(`${JSON.stringify({ summary, records }, null, 2)}\n`);
} else {
  process.stdout.write(`Markdown files scanned: ${summary.markdownFilesScanned}\n`);
  process.stdout.write(`Active wiki links: ${summary.wikiLinks}\n`);
  process.stdout.write(`Unique resolutions: ${summary.unique}\n`);
  process.stdout.write(`Missing: ${summary.missing}\n`);
  process.stdout.write(`Ambiguous: ${summary.ambiguous}\n`);
  for (const record of [...missing, ...ambiguous]) {
    const detail = record.matches.length > 0 ? ` -> ${record.matches.join(", ")}` : "";
    process.stdout.write(`- ${record.file}:${record.line} ${record.target} (${record.resolution})${detail}\n`);
  }
}

if (failMode && (missing.length > 0 || ambiguous.length > 0)) process.exitCode = 1;
