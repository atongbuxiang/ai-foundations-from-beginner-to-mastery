#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";

const files = process.argv.slice(2);

if (files.length === 0) {
  console.error("Usage: node validate-svg-figure.mjs FILE.svg [FILE.svg ...]");
  process.exit(2);
}

let failed = false;

for (const filename of files) {
  const errors = [];
  const warnings = [];
  let source = "";

  try {
    source = fs.readFileSync(filename, "utf8");
  } catch (error) {
    errors.push(`cannot read file: ${error.message}`);
  }

  if (source) {
    if (!/<svg\b[^>]*>/i.test(source)) errors.push("missing <svg> root");
    if (!/<title\b[^>]*>\s*[^<]+\s*<\/title>/i.test(source)) errors.push("missing non-empty <title>");
    if (!/<desc\b[^>]*>\s*[^<]+\s*<\/desc>/i.test(source)) errors.push("missing non-empty <desc>");
    if (!/aria-labelledby=["'][^"']*title[^"']*desc[^"']*["']/i.test(source)) {
      warnings.push("root should connect <title>/<desc> with aria-labelledby");
    }

    const viewBox = source.match(/viewBox=["']\s*([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s*["']/i);
    if (!viewBox) {
      errors.push("missing numeric viewBox");
    } else {
      const width = Number(viewBox[3]);
      const height = Number(viewBox[4]);
      if (width !== 1200) warnings.push(`viewBox width is ${width}; course default is 1200`);
      if (height < 360 || height > 800) warnings.push(`viewBox height ${height} is outside the usual 360–800 range`);
    }

    // Accept both CSS declarations (`font-family: ...`) and the standard SVG
    // presentation attribute (`font-family="..."`).  Both make the fallback
    // stack explicit and survive standalone SVG rendering.
    if (!/font-family\s*(?::|=)/i.test(source)) errors.push("missing explicit font-family stack");
    if (/<(?:filter|linearGradient|radialGradient)\b/i.test(source)) {
      warnings.push("contains filter or gradient; verify that it is semantically necessary");
    }
    if (/<foreignObject\b/i.test(source)) warnings.push("contains foreignObject; export compatibility may be poor");
    if (/href=["']https?:\/\//i.test(source)) errors.push("contains external href; self-drawn SVG should be self-contained");

    const sizes = [...source.matchAll(/font-size\s*(?::|=)\s*["']?([\d.]+)/gi)].map((match) => Number(match[1]));
    for (const declaration of source.matchAll(/font\s*:\s*([^;}{]+)/gi)) {
      const shorthandSize = declaration[1].match(/([\d.]+)px(?:\s*\/\s*[\d.]+(?:px)?)?/i);
      if (shorthandSize) sizes.push(Number(shorthandSize[1]));
    }
    const tooSmall = sizes.filter((size) => size < 15);
    if (tooSmall.length > 0) warnings.push(`contains font sizes below 15 px: ${[...new Set(tooSmall)].join(", ")}`);

    const accentColors = ["#2563eb", "#0f766e", "#b7791f", "#c24135"].filter((color) =>
      source.toLowerCase().includes(color),
    );
    if (accentColors.length > 3) warnings.push("uses all four accent colors; confirm that every color has a stable logical role");

    if (/\[(?:TODO|TBD|placeholder|待填写|图号|标题|来源)\]/i.test(source)) {
      warnings.push("contains bracketed placeholder text; replace it before publishing");
    }
  }

  const label = path.relative(process.cwd(), filename) || filename;
  if (errors.length === 0) {
    console.log(`PASS ${label}`);
  } else {
    failed = true;
    console.error(`FAIL ${label}`);
  }

  for (const message of errors) console.error(`  error: ${message}`);
  for (const message of warnings) console.warn(`  warning: ${message}`);
}

if (failed) process.exitCode = 1;
