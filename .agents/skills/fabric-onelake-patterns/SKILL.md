---
name: "fabric-onelake-patterns"
description: "Plan Microsoft OneLake architectures, shortcuts, and ADLS Gen2 interoperability when one logical data lake spans Fabric workloads."
metadata:
  metadata-version: "1.0.0"
  title: "Fabric OneLake Patterns"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-23"
  collection: "data"
---

# Fabric OneLake Patterns

Agent plans OneLake as the unified storage layer for Fabric. Agent uses workspaces, domains, shortcuts, and open storage access to keep one logical lake with distributed ownership.

## When Not to Use

| User prompt | Route |

|---|---|

| User asks for detailed lakehouse table design | Use `fabric-lakehouses` |

| User asks for CDC replication from operational databases | Use `fabric-shortcuts-mirroring` |

| User asks for workspace security and release governance | Use `fabric-workspaces-governance` |

## Required Inputs

| Input | Required | Description |

|---|---|---|

| Organization layout | Yes | State domains, teams, and workspace ownership boundaries. |

| Data locations | Yes | State Fabric-native, ADLS Gen2, AWS, or mixed sources. |

| Access paths | Yes | State Fabric UX, API, file explorer, or external engine access. |

| Duplication tolerance | Yes | State whether edge copies are allowed. |

| Governance controls | Recommended | State catalog, lineage, and security expectations. |

## Shortcut rule

Document source ownership and break conditions for every shortcut, because targets may lack lifecycle control.
