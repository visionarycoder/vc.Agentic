---
title: VBD Coding Evidence
doc_type: reference
status: active
last_updated: 2026-10-09
---

# Evidence labels

Use paraphrase. Do not paste book text into code or reviews.

## Sources

| ID | Source | Type | Date checked | Use | Limit |
| --- | --- | --- | --- | --- | --- |
| E1 | Juval Löwy, *Righting Software*, Addison-Wesley, 2019/2020, ISBN 9780136524038 | Primary book identity | 2026-10-09 | Book title and two-part Method | Full text was not copied. |
| E2 | InformIT excerpt, Software System Decomposition, page 1, `https://www.informit.com/articles/article.aspx?p=2995357` | Primary author excerpt | 2026-10-09 | Functional and domain decomposition defects | Excerpt, not the whole book. |
| E3 | InformIT excerpt, page 2, `https://www.informit.com/articles/article.aspx?p=2995357&seqNum=2` | Primary author excerpt | 2026-10-09 | Decompose by volatility; contain change | Excerpt, not the whole book. |
| E4 | InformIT excerpt, page 3, `https://www.informit.com/articles/article.aspx?p=2995357&seqNum=3` | Primary author excerpt | 2026-10-09 | Axes, variability, masquerading solutions, longevity | Excerpt, not the whole book. |
| E5 | InfoQ Q&A, 2020-02-10, `https://www.infoq.com/articles/book-review-righting-software/` | Secondary author interview | 2026-10-09 | Composable design; about-ten observation | Not a full standard. |
| E6 | SE Radio 407 transcript, 2020-04-24, `https://se-radio.net/2020/04/episode-407-juval-lowy-on-righting-software/` | Secondary transcript | 2026-10-09 | Manager, Engine, Access, Resource, Client, Utility | Transcript, not Chapter 3 rule text. |
| E7 | Pearson contents sample, `https://www.pearson.de/media/muster/toc/toc_9780136523987.pdf` | Primary contents list | 2026-10-09 | Chapter 3 topic names | Names only. No rule text. |
| E8 | `https://www.idesign.net/Resources/Standards` | Gated location | 2026-10-09 | Evidence gap | Detailed standard was not retrieved. |

## Rule labels

| Rule | Label | Source |
| --- | --- | --- |
| Decompose by volatility. Implement behavior as interaction. | Primary guidance | E3 |
| Do not design the structure against the requirements. | Primary guidance | E2, E5 |
| Functional decomposition couples structure to the current feature list, blocks reuse, bloats clients, and spreads change. | Primary guidance | E2 |
| Domain decomposition is functional decomposition under domain names. | Primary guidance | E2 |
| Functional decomposition is a requirements-discovery technique. Do not map it onto the design. | Primary guidance | E2 |
| Encapsulate open-ended ripple change. Keep closed local difference in ordinary code. | Primary guidance | E4 |
| Use the time axis and the customer axis. | Primary guidance | E4 |
| Strip solutions that masquerade as requirements. | Primary guidance | E4 |
| Do not encapsulate the nature of the business. Reject speculative design. | Primary guidance | E4 |
| Volatility list to blocks is not one-to-one. | Primary guidance | E4 |
| Implementation technology is detailed design, not the decomposition. | Primary guidance | E2 |
| Core use cases stay few. Other cases are different interactions of the same blocks. | Secondary interpretation | E5 |
| About ten services is an order-of-magnitude observation, not a target. | Secondary interpretation | E5 |
| Manager owns sequence volatility. Engine owns activity volatility. Access owns the access mechanism. Resource owns the accessed thing. Client owns presentation. Utility owns infrastructure. | Secondary interpretation | E6 |
| A Manager groups related use cases. Engines are shareable. A Manager uses zero or more Engines. | Secondary interpretation | Public slide summary, 2022. Not Chapter 3 text. |
| Call bans, the four questions, and the Managers-to-Engines ratio | Heuristic/Unknown | E7 names the topics. E8 was not retrieved. |
| Upward calls are always forbidden. | Heuristic/Unknown | No public rule text on 2026-10-09. Reject cycles with a dependency reason. |
