# Volatility-Based Decomposition Principles

Understanding the architectural philosophy behind VBD generators.

## Core Concept

**Volatility-Based Decomposition (VBD)** organizes systems around *what changes together* rather than traditional layering or domain boundaries.

**Key insight:** Things that change for the same reasons should be grouped together. Things that change for different reasons should be separated.

## The Volatility Question

"What causes this code to change?"

- **Business logic volatility** — Rules change as business evolves
- **UI volatility** — Presentation changes frequently
- **Data schema volatility** — Storage structure evolves
- **Integration volatility** — External APIs change
- **Infrastructure volatility** — Hosting, deployment, scaling needs shift

Each volatility type deserves its own boundary.

## Service Boundary Structure

A VBD service boundary contains:

### 1. Contract Project
**Purpose:** Define the public interface
**Volatility:** Stable — changes break consumers
**Dependencies:** Zero external dependencies
**Contents:** Interfaces, DTOs, enums only

**Why:** Contracts are the most stable part of a service. They change only when the service's fundamental purpose changes. Zero dependencies ensure consumers aren't dragged into implementation details.

### 2. Service Project (Engines)
**Purpose:** Implement business logic
**Volatility:** High — business rules evolve constantly
**Dependencies:** Contracts only
**Contents:** Pure business logic, no infrastructure

**Why:** Business logic changes frequently as requirements evolve. Isolating it from infrastructure means business changes don't force infrastructure changes and vice versa.

### 3. Access Project
**Purpose:** Handle external dependencies
**Volatility:** Medium — APIs, databases, external systems change
**Dependencies:** Contracts only
**Contents:** Database access, API clients, file I/O

**Why:** External systems change on their own schedule. Isolating access means you can swap databases, change APIs, or mock externals without touching business logic.

### 4. Manager Project
**Purpose:** Orchestrate engines and workflows
**Volatility:** Medium — workflows evolve as processes change
**Dependencies:** Service + Contracts
**Contents:** Multi-engine coordination, transaction boundaries

**Why:** Workflows change as business processes evolve, but less frequently than individual rules. Managers coordinate without duplicating logic.

### 5. Emulator Project
**Purpose:** Enable offline testing
**Volatility:** Low — changes when contracts change
**Dependencies:** Contracts only
**Contents:** In-memory implementations for testing

**Why:** Tests shouldn't depend on external systems. Emulators provide deterministic, fast test doubles.

### 6. Test Project
**Purpose:** Verify boundary behavior
**Volatility:** Medium — changes when contracts or behavior change
**Dependencies:** Contracts + Emulator
**Contents:** Regression tests, contract tests

**Why:** Tests verify public behavior without coupling to implementation details.

### 7. UI Projection
**Purpose:** Present boundary data
**Volatility:** Very high — UI changes constantly
**Dependencies:** Contracts only
**Contents:** Framework-specific components, views, forms

**Why:** UI is the most volatile part of most systems. Isolating it means UI churn doesn't affect business logic.

### 8. Deployment Project
**Purpose:** Define infrastructure
**Volatility:** Low-medium — infrastructure evolves slowly
**Dependencies:** None (infrastructure as code)
**Contents:** Bicep/Terraform templates

**Why:** Infrastructure changes are expensive and infrequent. Separating them prevents infrastructure decisions from leaking into code.

## Dependency Rules

**The Contract Rule:** All cross-boundary references go through Contracts only.

**Why it matters:**
- Service implementations can change freely
- UI never couples to business logic details
- Tests remain stable across refactorings
- Services can version independently

**Enforcement:** Analyzers detect violations at compile time.

## Contrast with Traditional Layering

**Traditional layering:**
```
UI Layer → Business Layer → Data Layer
```
Problem: UI changes force business layer changes, business changes force data layer changes. Everything is coupled.

**VBD:**
```
UI → Contracts ← Service
              ← Access
```
UI and Service both depend on stable Contracts. They can change independently.

## When to Create a Boundary

Create a new service boundary when:

1. **Different change drivers** — "We change X when business rules change, Y when external APIs change"
2. **Different teams** — "Team A owns this, Team B owns that"
3. **Different deployment cadences** — "We deploy X weekly, Y quarterly"
4. **Different scaling needs** — "X needs to scale horizontally, Y doesn't"

**Don't** create boundaries for:
- Arbitrary "layers"
- Small helper utilities
- Code that always changes together

## Benefits of VBD

1. **Change isolation** — Business logic changes don't force UI changes
2. **Independent deployment** — Services deploy without coordinating
3. **Team autonomy** — Teams own entire boundaries
4. **Testability** — Emulators enable fast, deterministic tests
5. **Clarity** — Structure makes volatility explicit

## Generators Enforce VBD

Generators make VBD automatic:

- **Structure generation** — Correct project topology from a definition
- **Dependency enforcement** — Analyzers prevent violations
- **Consistency** — Every boundary follows the same pattern
- **Friction reduction** — Correct architecture is the easiest path

Without generators, developers must manually maintain structure. With generators, structure is automatic and violations are caught at compile time.

## Example: Billing Boundary

**Volatility analysis:**
- Billing rules change frequently (new pricing models, discounts)
- Payment gateway API changes occasionally
- Invoice UI changes constantly
- Database schema changes rarely

**Boundary structure:**
- **Contracts:** `IBillingService`, `Invoice` DTO
- **Service:** Pricing engines, discount engines
- **Access:** Payment gateway client, invoice repository
- **Manager:** Orchestrates pricing + payment + storage
- **UI:** Invoice display, payment forms
- **Emulator:** In-memory billing for tests

**Result:** Pricing rule changes don't touch UI. UI redesigns don't touch business logic. Payment gateway swaps don't affect pricing.

## Further Reading

VBD originates from:
- "Designing Software Architectures" by Humberto Cervantes and Rick Kazman
- "Structured Design" by Constantine and Yourdon (volatility as a decomposition criterion)
- Microservices patterns (bounded contexts, independent deployment)

VBD + generators = microservices architecture enforced at compile time.
