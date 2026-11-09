---
title: VBD Source Register and Rule Matrix
doc_type: reference
status: active
last_updated: 2026-09-28
---

# VBD source register and rule matrix

## Source register

| ID | Source | Type | Date checked | Use | Limit |
| --- | --- | --- | --- | --- | --- |
| S1 | Juval Löwy, *Righting Software*, first edition, 2019/2020, ISBN 9780136524038 | Primary source metadata | 2026-09-28 | Verified book identity and scope | Full text was not copied. |
| S2 | `https://www.informit.com/articles/article.aspx?p=2995357&seqNum=2` | Primary author excerpt | 2026-09-28 | Volatility, encapsulation, bounded variability | Use paraphrase only. |
| S3 | `https://www.informit.com/articles/article.aspx?p=2995357&seqNum=3` | Primary author excerpt | 2026-09-28 | Identifying volatility and business invariants | Use paraphrase only. |
| S4 | `https://www.infoq.com/articles/book-review-righting-software/` | Secondary review and author Q&A | 2026-09-28 | Interpretation and caution on service count | Not a full standard. |
| S5 | `https://se-radio.net/2020/04/episode-407-juval-lowy-on-righting-software/` | Secondary transcript with author interview | 2026-09-28 | Role language around Client, Manager, Engine, Access, Resource, Utility | Transcript timing supports role discussion. |
| S6 | `https://www.informit.com/store/righting-software-9780136524038` | Primary store table of contents | 2026-09-28 | Book structure and terms | No detailed rule text. |
| S7 | `https://www.idesign.net/Resources/Standards` | Gated source location | 2026-09-28 | Evidence gap | Detailed standard was not retrieved. |
| S8 | Financial IDL `.agents/skills/vbd-system-design/SKILL.md` | Repository rule | 2026-09-28 | Local contract and mapper rules | Applies only where that repository governs work. |

## Rule classification

| Rule | Classification | Section | Scope | Exceptions and limits |
| --- | --- | --- | --- | --- |
| Components hide a reason to change behind a contract. | Primary guidance | S2 volatility excerpt | Global guidance | The exact implementation contract depends on local rules. |
| Customer and time axes help identify volatility. | Primary guidance | S3 identifying excerpt | Discovery | Do not invent changes that lack business evidence. |
| A single volatility does not automatically produce one component. | Secondary interpretation | S4 author Q&A | Design review | Merge or split after contract and interaction review. |
| About ten services is an observation. | Secondary interpretation | S4 author Q&A | Size review | Do not use the number as a target or gate. |
| Client, Manager, Engine, Access, Resource, and Utility name useful roles. | Secondary interpretation | S5 transcript 29:41-33:26 | Role vocabulary | Detailed call restrictions remain unverified. |
| The relationship matrix in this guidance is team policy. | Team policy | `vbd-boundary-design` relationship policy | Shared workflow | Do not present it as a full Lowy standard. |
| Financial IDL callers depend on immediate contracts and mapping services. | Repository rule | S8 lines 52-61 and 98-116 | Financial IDL | Local rules remain stricter than global guidance. |
| Upward calls and callbacks are always forbidden. | Heuristic/Unknown | S7 evidence gap | Review | Inspect each case. Reject cycles with dependency rationale. |
