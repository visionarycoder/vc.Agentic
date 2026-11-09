---
metadata-version: "1.0.0"
title: ".NET Performance Patterns"
description: "Preserve scoped source guidance for analyzing-dotnet-performance."
document-type: "reference"
repository: "vc.Agentic"
language: "Standard Technical English"
updated: "2026-11-08"
---

# .NET Performance Patterns

Agent uses this skill to scan C# code for counted performance defects and concrete fixes.

## When to Use

| User prompt | Use |

|---|---|

| User asks for a performance review of .NET code | Agent uses this skill |

| User asks to audit hot paths for allocations or inefficient APIs | Agent uses this skill |

| User asks for a systematic anti-pattern scan before release | Agent uses this skill |

## When Not to Use

| User prompt | Route |

|---|---|

| User asks for algorithm redesign | Agent uses a design review workflow |

| User asks for production tracing or profiling only | Agent uses tracing or profiling skills |

| User has no performance requirement and no hot path | Agent skips speculative optimization |

## Required Inputs

| Input | Required | Notes |

|---|---|---|

| Source scope | Yes | Agent scans files, folders, or code blocks. |

| Hot-path context | Recommended | Agent raises severity for known hot paths. |

| Target framework | Recommended | Agent uses runtime facts for fix viability. |

| Scan depth | No | Agent uses `critical-only`, `standard`, or `comprehensive`. |

## Workflow

| Step | Agent action | Test | Pass |

|---|---|---|---|

| 1 | Agent identifies hot paths, target framework, and scan depth. | Read the prompt and scope note. | Scope note states hot-path status, TFM, and scan depth. |

| 2 | Agent detects category signals and selects scan recipes. Agent reads `references/critical-patterns.md` to front-load deadlocks, catastrophic regex, serializer caching, and `HttpClient` reuse defects. | Run `rg -n "async|await|Task|ValueTask|Span<|Memory<|Regex|Dictionary<|JsonSerializer|HttpClient|Stream" <scope>`. | Agent has a category list with counted hits. |

| 3 | Agent runs recipe groups and records hit counts. Agent reads `references/async-patterns.md`, `references/memory-and-strings.md`, `references/collections-and-linq.md`, `references/regex-patterns.md`, and `references/io-and-serialization.md` for category-specific scan recipes and fix patterns. | Run the selected `rg` commands from the recipe matrix. | Recipe log lists every command and a hit count, including zero. |

| 4 | Agent applies inverse counts for ratio findings. Agent reads `references/structural-patterns.md` for absence-based counting rules such as sealed versus unsealed class ratios. | Count both positive and negative patterns, such as sealed and unsealed classes. | Ratio findings report `N of M` values. |

| 5 | Agent classifies findings by severity and hot-path context. Agent reads `references/critical-patterns.md` to keep deadlocks, catastrophic backtracking, and runtime-wide regressions above moderate findings. | Review the finding list. | Each finding has severity, count, files, and a concrete fix. |

| 6 | Agent writes a compact summary table. | Read the output footer. | Summary table lists severity counts and the top defect. |

## Recipe Matrix

| Category | Agent action |

|---|---|

| Strings | Agent scans for `.IndexOf(`, `.StartsWith(`, `.EndsWith(`, `.Contains(`, `.ToLower()`, `.ToUpper()`, `.Substring(`, and `.Replace(`. |

| Collections and LINQ | Agent scans for `.Where(`, `.Select(`, `.OrderBy(`, `.GroupBy(`, `.Any(`, `.All(`, `new List<`, and `new Dictionary<`. |

| Regex | Agent scans for `new Regex(`, `RegexOptions.Compiled`, and `GeneratedRegex`. |

| Async | Agent scans for `Task`, `ValueTask`, sync-over-async calls, and hidden allocations in closures. |

| I/O and serialization | Agent scans for `JsonSerializer`, `HttpClient`, `Stream`, and file I/O on hot paths. |

| Structural | Agent counts `sealed class` and non-sealed class declarations. |

## Reference Files

| File | Covers | Agent reads when |
|---|---|---|
| `references/critical-patterns.md` | High-severity .NET performance defects that cause deadlocks, catastrophic backtracking, socket exhaustion, severe regressions, or repeated allocations. | Agent reads during category selection and severity classification. |
| `references/async-patterns.md` | Async and concurrency anti-patterns such as sync-over-async, `ValueTask` misuse, wrapper APIs, channels, and thread-sharing defects. | Agent reads when the scope contains async, task, or concurrency signals. |
| `references/memory-and-strings.md` | Span, stack allocation, UTF-8 literals, string chains, and string-allocation reduction patterns. | Agent reads when the scope contains slicing, formatting, string transforms, or temporary-buffer work. |
| `references/collections-and-linq.md` | Collection allocation, dictionary lookup, LINQ hot-path, and capacity-planning patterns. | Agent reads when the scope contains `List`, `Dictionary`, `HashSet`, or LINQ operators. |
| `references/regex-patterns.md` | Regex engine mode, source generation, enumeration, counting, and allocation-free matching patterns. | Agent reads when the scope contains `Regex` construction or regex API calls. |
| `references/io-and-serialization.md` | `HttpClient`, stream, file I/O, JSON serialization, formatting, and general runtime optimization patterns. | Agent reads when the scope contains I/O, networking, serializer, or stream usage. |
| `references/structural-patterns.md` | Codebase-wide absence patterns such as sealed-class ratios and other inverse counting rules. | Agent reads when findings depend on `N of M` structure counts instead of direct matches. |

## Severity Matrix

| Severity | Agent action |

|---|---|

| Critical | Agent reports deadlocks, crashes, severe regressions, and security-sensitive performance defects first. |

| Moderate | Agent reports counted API and allocation defects that affect hot paths or appear at scale. |

| Info | Agent reports lower-impact patterns outside hot paths. |

| Scale escalation | Agent raises repeated patterns with 11+ instances and flags 50+ instances as systematic. |

## Output Contract

| Field | Agent action |

|---|---|

| Title | Agent writes a short defect title with instance count. |

| Impact | Agent states one-line performance effect. |

| Files | Agent lists `File.cs:L42` locations inline. |

| Fix | Agent states the concrete code change. |

| Caveat | Agent adds a caveat only when runtime or correctness risk matters. |

## Validation Checklist

- [ ] Agent logged each scan recipe and hit count.

- [ ] Agent reported zero-hit recipes when they add evidence.

- [ ] Agent reported `N of M` ratios for inverse patterns.

- [ ] Agent attached a concrete fix to each finding.

- [ ] Agent grouped findings by severity.

- [ ] Agent ended with a summary table.

## Common Pitfalls

| Pitfall | Agent fix |

|---|---|

| Agent flags every `Dictionary` as a `FrozenDictionary` defect | Agent flags only read-only dictionaries. |

| Agent suggests `Span<T>` inside async code | Agent uses `Memory<T>` for async paths. |

| Agent reports LINQ outside hot paths as a universal defect | Agent ties severity to hot-path scope. |

| Agent suggests `ValueTask` everywhere | Agent limits `ValueTask` to measured hot paths with frequent synchronous completion. |
