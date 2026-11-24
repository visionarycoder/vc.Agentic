---
name: "using-git-worktrees"
description: "Use when starting feature work that needs isolation from current workspace or before executing implementation plans - ensures an isolated workspace exists via native tools or git worktree fallback"
metadata:
  metadata-version: "1.0.0"
  title: "Using Git Worktrees"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-23"
  collection: "optional"
---

# Using Git Worktrees

## Overview

Ensure work happens in an isolated workspace. Prefer your platform's native worktree tools. Fall back to manual git worktrees only when no native tool is available.

**Core principle:** Detect existing isolation first. Then use native tools. Then fall back to git. Never fight the harness.

**Announce at start:** "I'm using the using-git-worktrees skill to set up an isolated workspace."

## Step 0: Detect Existing Isolation

Compare resolved `git rev-parse --git-dir` with `git rev-parse --git-common-dir`. If they differ and `git rev-parse --show-superproject-working-tree` returns nothing, you are already in a linked worktree (a returned path means a submodule; treat it as a normal repo). Skip to Step 2 and do not create another worktree. Report the path and branch, or for detached HEAD: "Already in isolated workspace at `<path>` (detached HEAD, externally managed). Branch creation needed at finish time."

In a normal checkout, ask consent before creating a worktree unless the user already declared a preference. Honor a declared preference; if the user declines, work in place and skip to Step 2.

## Step 1: Create Isolated Workspace

### 1a. Native tools (preferred)

If a native worktree tool exists (`EnterWorktree`, `WorktreeCreate`, `/worktree`, `--worktree`), use it and skip to Step 2. Manual `git worktree add` alongside a native tool creates phantom state the harness cannot manage.

### 1b. Git fallback (no native tool only)

Directory priority: declared user preference, then existing `.worktrees` (wins over `worktrees`), then default `.worktrees/` at the project root.

Before creating a project-local directory, verify `git check-ignore -q <dir>`. If not ignored, add it to `.gitignore` and commit first.

Then `git worktree add "<dir>/<branch>" -b "<branch>"` and `cd` into it. If creation fails with a sandbox permission error, tell the user, work in place, and run setup and baseline tests there.

## Step 2: Project Setup

Auto-detect and run dependency install (npm install, cargo build, pip install -r requirements.txt, poetry install, go mod download); skip when no manifest exists.

## Step 3: Verify Clean Baseline

Run the project tests. On failure, report the failures and ask whether to proceed or investigate; never proceed silently. On success report:

```
Worktree ready at <full-path>
Tests passing (<N> tests, 0 failures)
Ready to implement <feature-name>
```
