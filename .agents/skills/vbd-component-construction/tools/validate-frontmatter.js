#!/usr/bin/env node
/* eslint-disable no-console */
const fs = require("fs");
const path = require("path");
const cp = require("child_process");

const REQUIRED_KEYS = ["title", "doc_type", "status", "last_updated"];
const DOC_TYPES = new Set([
  "readme",
  "guide",
  "reference",
  "runbook",
  "plan",
  "report",
  "policy",
  "skill",
  "prompt",
  "archive",
]);
const STATUSES = new Set(["draft", "active", "deprecated", "archived"]);
const DATE_RE = /^\d{4}-\d{2}-\d{2}$/;

const args = new Set(process.argv.slice(2));
const shouldFix = args.has("--fix");
const shouldCheck = args.has("--check") || !shouldFix;

function getTrackedMarkdownFiles(repoRoot) {
  try {
    const output = cp.execSync("git ls-files *.md", {
      cwd: repoRoot,
      stdio: ["ignore", "pipe", "ignore"],
      encoding: "utf8",
    });
    return output
      .split(/\r?\n/)
      .map((line) => line.trim())
      .filter(Boolean)
      .map((rel) => path.join(repoRoot, rel));
  } catch {
    return walkMarkdownFiles(repoRoot);
  }
}

function walkMarkdownFiles(root) {
  const ignored = new Set([".git", "node_modules", "bin", "obj", "packages", ".vs", ".vscode"]);
  const files = [];
  const stack = [root];
  while (stack.length > 0) {
    const dir = stack.pop();
    const entries = fs.readdirSync(dir, { withFileTypes: true });
    for (const entry of entries) {
      const full = path.join(dir, entry.name);
      if (entry.isDirectory()) {
        if (!ignored.has(entry.name)) {
          stack.push(full);
        }
        continue;
      }
      if (entry.isFile() && entry.name.toLowerCase().endsWith(".md")) {
        files.push(full);
      }
    }
  }
  return files;
}

function splitFrontMatter(content) {
  if (!content.startsWith("---\n") && !content.startsWith("---\r\n")) {
    return null;
  }
  const normalized = content.replace(/\r\n/g, "\n");
  const end = normalized.indexOf("\n---\n", 4);
  if (end === -1) {
    return null;
  }
  const fm = normalized.slice(4, end);
  const body = normalized.slice(end + 5);
  return { fm, body, normalized };
}

function parseTopLevelYaml(fm) {
  const result = {};
  const lines = fm.split("\n");
  for (const line of lines) {
    const match = line.match(/^([A-Za-z0-9_\-]+):\s*(.*)$/);
    if (!match) {
      continue;
    }
    const key = match[1];
    const raw = match[2].trim();
    let value = raw;
    if ((value.startsWith("\"") && value.endsWith("\"")) || (value.startsWith("'") && value.endsWith("'"))) {
      value = value.slice(1, -1);
    }
    result[key] = value;
  }
  return result;
}

function inferTitle(filePath, body) {
  const h1 = body.match(/^#\s+(.+)$/m);
  if (h1 && h1[1].trim()) {
    return h1[1].trim();
  }
  const base = path.basename(filePath, ".md");
  return base
    .replace(/[_-]+/g, " ")
    .replace(/\b\w/g, (c) => c.toUpperCase());
}

function inferDocType(relPath) {
  const p = relPath.replace(/\\/g, "/").toLowerCase();
  const file = path.basename(p);
  if (p.includes("/.github/skills/") || p.endsWith("/skill.md")) return "skill";
  if (p.includes("/.github/prompts/") || p.endsWith(".prompt.md")) return "prompt";
  if (p.includes("/archive/")) return "archive";
  if (p.includes("/runbook") || p.includes("/runbooks/")) return "runbook";
  if (p.includes("/plan") || p.includes("/plans/") || file.includes("plan")) return "plan";
  if (p.includes("/report") || p.includes("/reports/") || file.includes("report")) return "report";
  if (file === "readme.md") return "readme";
  if (file.includes("policy")) return "policy";
  if (p.includes("/reference/") || file.includes("reference")) return "reference";
  return "guide";
}

function today() {
  return new Date().toISOString().slice(0, 10);
}

function buildRequiredFrontMatter(values) {
  return [
    "---",
    `title: ${values.title}`,
    `doc_type: ${values.doc_type}`,
    `status: ${values.status}`,
    `last_updated: ${values.last_updated}`,
    "---",
    "",
  ].join("\n");
}

function insertMissingKeysIntoFrontMatter(content, existingFm, missingMap) {
  const normalized = content.replace(/\r\n/g, "\n");
  const lines = existingFm.split("\n");
  for (const [key, value] of Object.entries(missingMap)) {
    lines.push(`${key}: ${value}`);
  }
  const updatedFm = lines.join("\n");
  const split = splitFrontMatter(normalized);
  if (!split) {
    return normalized;
  }
  return `---\n${updatedFm}\n---\n${split.body}`;
}

function validateRecord(meta, relPath, issues) {
  for (const key of REQUIRED_KEYS) {
    if (!meta[key] || !String(meta[key]).trim()) {
      issues.push(`${relPath}: missing required key '${key}'`);
    }
  }
  if (meta.doc_type && !DOC_TYPES.has(meta.doc_type)) {
    issues.push(`${relPath}: invalid doc_type '${meta.doc_type}'`);
  }
  if (meta.status && !STATUSES.has(meta.status)) {
    issues.push(`${relPath}: invalid status '${meta.status}'`);
  }
  if (meta.last_updated && !DATE_RE.test(meta.last_updated)) {
    issues.push(`${relPath}: invalid last_updated '${meta.last_updated}' (expected YYYY-MM-DD)`);
  }
}

function main() {
  const repoRoot = process.cwd();
  const files = getTrackedMarkdownFiles(repoRoot);
  const issues = [];
  let fixedCount = 0;

  for (const file of files) {
    const relPath = path.relative(repoRoot, file).replace(/\\/g, "/");
    if (!fs.existsSync(file)) {
      continue;
    }
    const content = fs.readFileSync(file, "utf8");
    const split = splitFrontMatter(content);

    if (!split) {
      if (shouldFix) {
        const bodyNorm = content.replace(/\r\n/g, "\n");
        const fm = buildRequiredFrontMatter({
          title: inferTitle(file, bodyNorm),
          doc_type: inferDocType(relPath),
          status: "active",
          last_updated: today(),
        });
        fs.writeFileSync(file, fm + bodyNorm, "utf8");
        fixedCount += 1;
      } else if (shouldCheck) {
        issues.push(`${relPath}: missing front matter`);
      }
      continue;
    }

    const meta = parseTopLevelYaml(split.fm);
    const missingMap = {};

    if (!meta.title || !String(meta.title).trim()) {
      missingMap.title = inferTitle(file, split.body);
    }
    if (!meta.doc_type || !String(meta.doc_type).trim()) {
      missingMap.doc_type = inferDocType(relPath);
    }
    if (!meta.status || !String(meta.status).trim()) {
      missingMap.status = "active";
    }
    if (!meta.last_updated || !String(meta.last_updated).trim()) {
      missingMap.last_updated = today();
    }

    if (shouldFix && Object.keys(missingMap).length > 0) {
      const updated = insertMissingKeysIntoFrontMatter(content, split.fm, missingMap);
      fs.writeFileSync(file, updated, "utf8");
      fixedCount += 1;
    }

    if (shouldCheck) {
      const current = parseTopLevelYaml(splitFrontMatter(fs.readFileSync(file, "utf8")).fm);
      validateRecord(current, relPath, issues);
    }
  }

  if (shouldFix) {
    console.log(`Front matter fix complete. Updated ${fixedCount} files.`);
  }

  if (shouldCheck) {
    if (issues.length > 0) {
      console.error(`Front matter validation failed with ${issues.length} issue(s):`);
      for (const issue of issues) {
        console.error(`- ${issue}`);
      }
      process.exit(1);
    }
    console.log("Front matter validation passed.");
  }
}

main();
