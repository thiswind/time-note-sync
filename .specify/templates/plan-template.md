# Implementation Plan: [FEATURE]

**Branch**: `[###-feature-name]` | **Date**: [DATE] | **Spec**: [link]
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

[Extract from feature spec: primary requirement + technical approach from research]

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: [e.g., Python 3.11, Swift 5.9, Rust 1.75 or NEEDS CLARIFICATION]  
**Primary Dependencies**: [e.g., FastAPI, UIKit, LLVM or NEEDS CLARIFICATION]  
**Storage**: [if applicable, e.g., PostgreSQL, CoreData, files or N/A]  
**Testing**: [e.g., pytest, XCTest, cargo test or NEEDS CLARIFICATION]  
**Target Platform**: [e.g., Linux server, iOS 15+, WASM or NEEDS CLARIFICATION]
**Project Type**: [single/web/mobile - determines source structure]  
**Performance Goals**: [domain-specific, e.g., 1000 req/s, 10k lines/sec, 60 fps or NEEDS CLARIFICATION]  
**Constraints**: [domain-specific, e.g., <200ms p95, <100MB memory, offline-capable or NEEDS CLARIFICATION]  
**Scale/Scope**: [domain-specific, e.g., 10k users, 1M LOC, 50 screens or NEEDS CLARIFICATION]

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Code Quality**: All code must be formatted with Black and pass lint checks. Code must pass code review before merge. Minimal comments, self-documenting code.

**Testing**: Unit tests and integration tests required for core functionality and major functions. All major features and critical functions must have unit test coverage. System must support automatic rollback on failure.

**Deployment**: Project deploys to Vercel. Use `main` branch. Create development branch for each iteration, merge after completion, then delete branch.

**Performance**: Maintain standard Python project performance expectations.

**Security & Privacy**: User privacy and security are highest priority. All data must be encrypted in transit (mandatory). Data access restricted to owner only. Authentication required to prevent unauthorized access. Important operations must have logging for traceability.

**Technology Stack**: Must use mature, mainstream libraries and standard protocols. Avoid experimental or unproven technologies unless justified.

**Architecture & Compatibility**: The application must use a monolithic Flask application structure. Frontend content (HTML templates, CSS, JavaScript, and static assets) must be served directly from Flask's `static/` and `templates/` directories. The application must not use a separate frontend build process or separate frontend server. All frontend assets must be integrated into the Flask application structure. Frontend and backend must be designed for easy compatibility upgrades without additional installation burden. API contracts must maintain backward compatibility or provide clear migration paths. Application must not require third-party installations. Must only depend on native browsers and iPhone system built-in tools.

**UI/UX**: All interfaces and interactions must prioritize iOS system style and operation habits. Design must align with iOS Human Interface Guidelines where applicable.

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)
<!--
  ACTION REQUIRED: Replace the placeholder tree below with the concrete layout
  for this feature. Delete unused options and expand the chosen structure with
  real paths (e.g., apps/admin, packages/something). The delivered plan must
  not include Option labels.
-->

```text
# [REMOVE IF UNUSED] Option 1: Single project (DEFAULT)
src/
├── models/
├── services/
├── cli/
└── lib/

tests/
├── contract/
├── integration/
└── unit/

# [REMOVE IF UNUSED] Option 2: Web application (Flask monolithic structure)
app.py                 # Flask application entry point
templates/             # HTML templates (Jinja2)
static/                # Static assets (CSS, JavaScript, images)
├── css/
├── js/
└── images/
models/                # Data models
services/              # Business logic services
api/                   # API routes (if needed)
tests/                  # Test files

# [REMOVE IF UNUSED] Option 3: Mobile + API (when "iOS/Android" detected)
api/
└── [same as backend above]

ios/ or android/
└── [platform-specific structure: feature modules, UI flows, platform tests]
```

**Structure Decision**: [Document the selected structure and reference the real
directories captured above]

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
