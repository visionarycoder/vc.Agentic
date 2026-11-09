---
name: "database-design-standards"
description: "Apply data modeling, naming, data type, dimensional model, data mart, and security rules when the developer layer is database."
metadata:
  metadata-version: "1.0.0"
  title: "Database Design Standards"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "optional"
---

# Database Design Standards

Load this skill when the `developer` agent works in layer `database` (write scope `database/**`).

## Gate 2 Additions

- Submit a proposal to `application-architect` before changing any schema. Include tables, keys, relationships, and deviations from the detailed design.
- Stop and ask `application-architect` through the work item when the detailed design is ambiguous.
- Write documentation and data model diagrams directly under `docs/**`.

## Design Rules

- Normalize to third normal form.
- Enforce business rules in the structure: relationship constraints, data domains, and null rules.
- Use referential integrity (foreign keys) to prevent orphaned records and unmatched deletes.
- Every table has a primary key. Use a surrogate primary key of type integer, named with the complete table name plus `Id`. Prefer surrogate keys to compound keys.
- Use foreign keys, not natural keys, to relate tables.
- Reuse existing data. Consult the Data Library and Conformed Dimensions before creating a new entity. Propose additions through the owning team and never duplicate their data.
- Sub-types inherit from the parent type through identifying relationships and hold only their own attributes.
- Create database objects from SQL scripts that the logical and physical models specify.

## Data Types

- Use `Date` when only a date is needed. Use `Datetime2(7)` when time is needed. Store UTC.
- Use `nchar`/`nvarchar` for strings unless another type is necessary.
- Use `decimal(19,4)` instead of `money`.
- In data warehouses, set the minimum `varchar` length to 5. Use an integer for a current-row indicator.
- Match types, formats, and sizes used for identical data in existing databases.

## Naming Rules

- Use singular, Pascal-case names with no underscores and no special characters.
- Use present tense (`RecordCreateDate`, not `RecordCreatedDate`).
- Use meaningful, consistent names with the class word (`StartDate`, not `Start`).
- Logical models: spell every name fully.
- Physical models: spell out single-word names of four characters or fewer. Abbreviate longer words only with the project's standard abbreviation list (for example `CustName`, `RevnSrcType`, `AcctTypeCode`). The surrogate primary key keeps the complete table name.
- Name objects with the `dbo` owner unless a security or subject-area need requires otherwise.
- Name staging tables with the `stg` prefix in non-staging databases, or use a `staging` schema with no prefix.
- Name views that differ in definition differently. Objects with the same definition share the same name.
- Name associative entities by concatenating the two entity names or by the function of the association.
- Name foreign key constraints `FK` + parent table + child table + role name. The table names use standard abbreviations and the role name is spelled out. A role name ends with the parent primary key suffix.

## Dimensional Models

- Order columns with the primary key first, then the load date and time.
- Fact tables use an ETL-populated surrogate key that is not an identity column.
- Every dimension has `<TableName>RowLoadDate`. Type 1 adds `<TableName>RowUpdateDate`. Type 2 adds `<TableName>RowBeginDate` and `<TableName>RowEndDate`. Type 6 adds both current and historical attribute columns.

## Data Management

- Define, name, and document every data element in the enterprise data catalog. Record entity and attribute definitions in the data model.
- Classify all data under WaTech SEC-08-01-S. Include an agency security review in the database design process.
- Require a backup and recovery plan for every database. Handle user-inactivity timeouts in the application, not the DBMS.
- Review database passwords annually under the network access standard.
- Design databases to be shared unless privacy, security, licensing, or performance prohibits it.

## Data Marts

Applies only to enterprise data warehouse data marts.

- Use Kimball star schemas: fact tables surrounded by dimension tables.
- Hold only Category 1 and 2 data. Category 3 data needs encryption at rest and restricted access with a stated business need.
- Build fact tables at the lowest grain. Every measure matches the grain. Never mix grains in one fact table.
- A fact table holds a primary key, foreign keys to dimensions, measures, and an ETL-populated row load date that users never see. Accumulating snapshot facts add a row update date.
- Foreign key values in fact tables are never null. Use the dimension's exception records.
- Store degenerate dimensions on the fact table with no join.
- Transaction and periodic snapshot facts insert only. Accumulating snapshot facts insert and update.
- Conformed dimensions live in the `ConformedDimensions` database. Each data mart reads them through a view and may rename columns in the view.
- Dimensions hold one discrete subject, are denormalized, and use a single integer surrogate key named `<TableName>Id`.
- Reserve dimension keys 0 to 99 for exception records (0 `DW Unknown`, 1 `DW Not Applicable`, 2 `DW No History`, 3 `DW Not Required`, 4 `DW Error Record`, 5 `DW System Error`, 6 blank). Keys 0 to 49 are enterprise-wide, 50 to 99 are data-mart-specific, and real keys start at 100. Number and date columns use null for exception values.
- Prefer Type 1 slowly changing dimensions. Type 2 needs a row effective date (initial value 1900-01-01) and row end date. Type 6 is the preferred option when history is required.
- Grant access through Active Directory groups. The department query tool is the preferred access model.
- Put staging tables in a designated staging database, never in a data mart. The `stg` prefix rule applies only to non-staging, non-data-mart databases.
- Name stored procedures, schemas, triggers, and functions under the DRM Database Management Standard.

## Security and Exemptions

- Notify the DBA and the agency cybersecurity office when a database holds WaTech category 3 or 4 data.
- Never store full magnetic-stripe track data, card-validation codes, or PINs. Protect any permitted cardholder data per PCI DSS.
- The DBA keeps final authority over physical structure. Route physical-design disagreements to `application-architect`.
- Document every deviation from the standard with its reason, mitigation, and remediation plan. A deviation needs signed approval from the IT Assistant Director, Data Management Services. Never deviate without a human approval recorded on the work item.
