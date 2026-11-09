---
metadata-version: "1.0.0"
title: ".NET P/Invoke"
description: "Preserve scoped source guidance for dotnet-pinvoke."
document-type: "reference"
repository: "vc.Agentic"
language: "Standard Technical English"
updated: "2026-11-08"
---

# .NET P/Invoke

Agent uses this skill to create, review, or debug managed and native interop declarations.

## When to Use

| User prompt | Use |

|---|---|

| User writes `DllImport` or `LibraryImport` declarations | Agent uses this skill |

| User reports crashes, corruption, or leaks at a native boundary | Agent uses this skill |

| User migrates interop code for trimming or AOT | Agent uses this skill |

## When Not to Use

| User prompt | Route |

|---|---|

| User asks about COM interop or C++/CLI | Agent uses a different interop workflow |

| User edits pure managed code | Agent uses a managed-code workflow |

| User asks for broad `DllImport` to `LibraryImport` migration with no defect scope | Agent uses a separate refactor workflow |

## Required Inputs

| Input | Required | Notes |

|---|---|---|

| Native header or signature document | Yes | Agent uses headers as the source of truth. |

| Target framework | Yes | Agent chooses `DllImport` or `LibraryImport` from this input. |

| Target platforms | Recommended | Agent uses this input for width and calling-convention decisions. |

| Ownership contract | Yes | Agent identifies who allocates and who frees each resource. |

## Workflow

| Step | Agent action | Test | Pass |

|---|---|---|---|

| 1 | Agent reads the real native signature and `references/type-mapping.md` for exact width and layout mapping. | Compare the declaration to the header. | Types, parameter order, and return type match the header contract. |

| 2 | Agent chooses `DllImport` or `LibraryImport`. | Read the target TFM and import declaration. | Import style matches the framework and AOT scope. |

| 3 | Agent makes encoding, calling convention, and ownership explicit. | Read marshalling attributes and wrapper code. | String encoding, calling convention, and free path are explicit. |

| 4 | Agent wraps long-lived handles with `SafeHandle`. | Run `rg -n "SafeHandle|CriticalHandle" <scope>`. | Long-lived native handles avoid raw `IntPtr`. |

| 5 | Agent runs a smoke build or targeted test and reads `references/diagnostics.md` when crashes, corruption, or loader defects need failure-mode triage. | Run `dotnet build <project-or-solution>` or `dotnet test <project>`. | Interop code builds and the target call path passes. |

## Reference Files

| File | Covers | Agent Reads |
|---|---|---|
| `references/diagnostics.md` | Failure modes, pitfall recovery, and debugger-first triage for loader, marshalling, lifetime, and corruption defects. | Agent reads it during validation or defect triage when interop calls crash, corrupt data, or fail to load. |
| `references/type-mapping.md` | Exact mapping tables for C and Win32 primitive, string, handle, and layout-sensitive types. | Agent reads it during signature transcription and struct review before changing the managed declaration. |

## Mapping Matrix

| Native concept | Agent action |

|---|---|

| C `long` | Agent uses `CLong`. |

| `size_t` | Agent uses `nuint` or `UIntPtr`. |

| Win32 `BOOL` | Agent uses 4-byte bool marshalling. |

| C `bool` | Agent uses 1-byte bool marshalling. |

| Native handles | Agent uses `SafeHandle` when handle lifetime crosses method scope. |

| Strings | Agent selects UTF-8 or UTF-16 explicitly and avoids `CharSet.Auto`. |

## Validation Checklist

- [ ] Agent matched the declaration to the native header.

- [ ] Agent made encoding and calling convention explicit.

- [ ] Agent documented or encoded the ownership contract.

- [ ] Agent used `SafeHandle` for long-lived handles.

- [ ] Agent ran build or targeted test verification.

## Common Pitfalls

| Pitfall | Agent fix |

|---|---|

| Agent trusts simplified prose docs over headers | Agent uses the header as the source of truth. |

| Agent frees native memory with the wrong allocator | Agent matches the allocator and free function exactly. |

| Agent uses `bool`, `long`, or `ulong` casually | Agent maps width-sensitive types deliberately. |

| Agent leaves handles as raw `IntPtr` | Agent wraps the handle. |
