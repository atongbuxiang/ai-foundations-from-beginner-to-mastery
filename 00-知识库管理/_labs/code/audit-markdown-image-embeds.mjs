#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";

const args = process.argv.slice(2);
const jsonMode = args.includes("--json");
const failMissing = args.includes("--fail-missing");
const failFormat = args.includes("--fail-format");
const rootArg = args.find((arg) => !arg.startsWith("--")) ?? ".";
const root = path.resolve(rootArg);

function walk(directory) {
  const entries = fs.readdirSync(directory, { withFileTypes: true });
  const files = [];

  for (const entry of entries) {
    if ([".git", "node_modules", ".obsidian"].includes(entry.name)) continue;
    const fullPath = path.join(directory, entry.name);
    if (entry.isDirectory()) files.push(...walk(fullPath));
    else if (entry.isFile()) files.push(fullPath);
  }

  return files;
}

function activeEmbeds(markdownPath) {
  const lines = fs.readFileSync(markdownPath, "utf8").split(/\r?\n/);
  const embeds = [];
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

    const pattern = /!\[\[([^\]\n]+)\]\]/g;
    for (const match of line.matchAll(pattern)) {
      if (match.index > 0 && line[match.index - 1] === "\\") continue;
      const fields = match[1].split("|").map((field) => field.trim());
      const target = fields[0];
      const width = fields.length > 1 ? fields.at(-1) : null;
      embeds.push({
        target,
        width,
        numericWidth: width !== null && /^\d+(?:\.\d+)?$/.test(width),
        line: index + 1,
      });
    }
  }

  return embeds;
}

function classifyVersion(target) {
  if (/-v1\.(?:svg|png|webp|jpe?g)$/i.test(target)) return "v1";
  if (/-v2\.(?:svg|png|webp|jpe?g)$/i.test(target)) return "v2";
  return "nonversioned";
}

const allFiles = walk(root);
const markdownFiles = allFiles.filter((file) => file.endsWith(".md"));
const filesByBasename = new Map();

for (const file of allFiles) {
  const basename = path.basename(file);
  const matches = filesByBasename.get(basename) ?? [];
  matches.push(file);
  filesByBasename.set(basename, matches);
}

const records = [];
for (const markdownPath of markdownFiles) {
  for (const embed of activeEmbeds(markdownPath)) {
    records.push({
      file: path.relative(root, markdownPath),
      ...embed,
      version: classifyVersion(embed.target),
      rootStable: embed.target.startsWith("00-知识库管理/_assets/"),
    });
  }
}

for (const record of records) {
  const target = record.target.replace(/^\/+/, "");
  const markdownDirectory = path.dirname(path.join(root, record.file));
  const directCandidates = [path.join(root, target), path.join(markdownDirectory, target)];
  const directMatch = directCandidates.find((candidate) => fs.existsSync(candidate));

  if (directMatch) {
    record.resolution = "direct";
    record.resolved = path.relative(root, directMatch);
    continue;
  }

  const basenameMatches = filesByBasename.get(path.basename(target)) ?? [];
  if (basenameMatches.length === 1) {
    record.resolution = "unique-basename";
    record.resolved = path.relative(root, basenameMatches[0]);
  } else if (basenameMatches.length > 1) {
    record.resolution = "ambiguous";
    record.candidates = basenameMatches.map((candidate) => path.relative(root, candidate));
  } else {
    record.resolution = "missing";
  }
}

const count = (predicate) => records.filter(predicate).length;
const summary = {
  markdownFilesWithActiveEmbeds: new Set(records.map((record) => record.file)).size,
  activeEmbeds: records.length,
  v1: count((record) => record.version === "v1"),
  v2: count((record) => record.version === "v2"),
  nonversioned: count((record) => record.version === "nonversioned"),
  rootStable: count((record) => record.rootStable),
  relative: count((record) => !record.rootStable),
  numericWidth: count((record) => record.numericWidth),
  missingWidth: count((record) => record.width === null),
  nonNumericWidth: count((record) => record.width !== null && !record.numericWidth),
  missing: count((record) => record.resolution === "missing"),
  ambiguous: count((record) => record.resolution === "ambiguous"),
};

if (jsonMode) {
  process.stdout.write(`${JSON.stringify({ summary, records }, null, 2)}\n`);
} else {
  const labels = {
    markdownFilesWithActiveEmbeds: "Markdown files with active embeds",
    activeEmbeds: "Active Obsidian image embeds",
    v1: "v1 embeds",
    v2: "v2 embeds",
    nonversioned: "Nonversioned embeds",
    rootStable: "Root-stable embeds",
    relative: "Relative embeds",
    numericWidth: "Embeds with numeric widths",
    missingWidth: "Embeds without widths",
    nonNumericWidth: "Embeds with nonnumeric widths",
    missing: "Missing targets",
    ambiguous: "Ambiguous basename targets",
  };
  for (const [key, value] of Object.entries(summary)) {
    process.stdout.write(`${labels[key]}: ${value}\n`);
  }

  const unresolved = records.filter((record) => ["missing", "ambiguous"].includes(record.resolution));
  if (unresolved.length > 0) {
    process.stdout.write("\nUnresolved embeds:\n");
    for (const record of unresolved) {
      process.stdout.write(`- ${record.file}:${record.line} -> ${record.target} (${record.resolution})\n`);
    }
  }
}

if (failMissing && (summary.missing > 0 || summary.ambiguous > 0)) process.exitCode = 1;
if (failFormat && (summary.relative > 0 || summary.missingWidth > 0 || summary.nonNumericWidth > 0)) {
  process.exitCode = 1;
}
