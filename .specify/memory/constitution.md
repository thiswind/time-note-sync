<!--
Sync Impact Report:
Version change: 1.2.0 → 1.3.0 (MINOR: architecture principle added - monolith structure requirement)
Modified principles:
  - VII. Architecture & Compatibility: Added requirement for monolithic Flask application structure (frontend in static/templates, no separate frontend build)
Added sections: N/A
Removed sections: N/A
Templates requiring updates:
  ✅ .specify/templates/plan-template.md (updated - architecture section)
  ✅ .specify/templates/tasks-template.md (updated - path conventions)
Follow-up TODOs: None
-->

# time-note-sync Constitution

## Core Principles

### I. Code Quality Standards

All code MUST be formatted using Black and pass lint checks. Code style prioritizes simplicity and practicality. Comments are minimal—only include essential comments where the code's intent is not self-evident. Python code should be self-documenting through clear naming and structure. Code MUST pass code review before merge.

**Rationale**: Consistent formatting reduces cognitive load and merge conflicts. Lint checks catch errors early. Code review ensures quality and knowledge sharing. Minimal comments keep code maintainable and force clarity in implementation.

### II. Testing Requirements (NON-NEGOTIABLE)

Unit tests and integration tests are REQUIRED for core functionality and major functions. All major features and critical functions MUST have unit test coverage. Test coverage must be maintained for critical paths. Tests must be written and pass before features are considered complete. The system MUST support automatic rollback on failure to maintain service stability.

**Rationale**: Comprehensive testing ensures reliability and enables confident refactoring. Core functionality and critical functions require test coverage to prevent regressions. Automatic rollback minimizes downtime and user impact when failures occur.

### III. Deployment & Version Control

The project is deployed to Vercel. Git is used for version control with `main` as the primary branch. Each development cycle MUST follow this workflow:

1. Create a development branch from `main`
2. Complete the development iteration on the branch
3. Merge back to `main` only after successful completion
4. Delete the development branch after merge

**Rationale**: Branch-based workflow ensures `main` remains stable and deployable. Branch cleanup prevents repository clutter.

### IV. Performance & Scalability

Maintain standard Python project performance expectations. Code should be efficient but not prematurely optimized. Focus on clarity and maintainability first.

**Rationale**: Python projects have established performance baselines. Premature optimization can harm code clarity without measurable benefit.

### V. Security & Privacy (NON-NEGOTIABLE)

User privacy and security are the highest priority. All data MUST be encrypted in transit (mandatory encryption). Data access MUST be restricted to the owner only. Authentication MUST be required to prevent unauthorized access. All important operations MUST have logging to enable operation traceability. Logs must capture sufficient context to reconstruct operation sequences and diagnose issues.

**Rationale**: User data protection is fundamental. Mandatory encryption in transit prevents interception. Access restrictions and authentication ensure data privacy and prevent unauthorized access. Logging is essential for debugging, security auditing, and operational visibility. Important operations require audit trails.

### VI. Technology Stack Standards

MUST use mature, mainstream libraries and standard protocols to reduce maintenance and upgrade costs. Avoid experimental or unproven technologies unless there is a compelling, documented justification.

**Rationale**: Mature, mainstream technologies have proven stability, community support, and documentation. This reduces long-term maintenance burden, upgrade costs, and integration complexity.

### VII. Architecture & Compatibility

The application MUST use a monolithic Flask application structure. Frontend content (HTML templates, CSS, JavaScript, and static assets) MUST be served directly from Flask's `static/` and `templates/` directories. The application MUST NOT use a separate frontend build process or separate frontend server. All frontend assets MUST be integrated into the Flask application structure.

Frontend and backend MUST be designed for easy compatibility upgrades without requiring additional installation burden for users. API contracts and interfaces MUST maintain backward compatibility where possible, or provide clear migration paths. The application MUST NOT require users to install third-party applications. It MUST only depend on native browsers and iPhone system built-in tools.

**Rationale**: Monolithic Flask structure simplifies deployment, reduces complexity, and eliminates the need for separate build processes. Serving frontend from Flask's static/templates directories provides a unified application structure that is easier to maintain and deploy. Easy upgrades reduce user friction and maintenance overhead. Backward compatibility ensures smooth transitions and reduces breaking changes. Zero installation burden improves user adoption and reduces support overhead.

### VIII. User Interface & Experience (iOS-First)

All interfaces and interactions MUST prioritize iOS system style and operation habits to ensure consistent and coherent user experience. Design decisions MUST align with iOS Human Interface Guidelines where applicable.

**Rationale**: iOS-native design patterns create familiar, intuitive experiences for iPhone users. Consistency with system conventions reduces learning curve and improves user satisfaction.

## Development Workflow

### Code Review

Code review is REQUIRED. All code MUST pass code review before merge to `main`.

### Quality Gates

- All code must pass Black formatting checks and lint checks
- All code must pass code review before merge to `main`
- All tests must pass before merge to `main`
- Major features and critical functions must have unit test coverage
- Important operations must have appropriate logging
- All data must be encrypted in transit (mandatory)
- Authentication must be implemented to prevent unauthorized access
- Automatic rollback capability must be verified
- UI/UX must align with iOS system style and operation habits

## Governance

This constitution supersedes all other development practices. Amendments require:

1. Documentation of the change rationale
2. Version increment following semantic versioning:
   - **MAJOR**: Backward incompatible changes to principles or governance
   - **MINOR**: New principles or materially expanded guidance
   - **PATCH**: Clarifications, wording improvements, typo fixes
3. Update of dependent templates and documentation
4. Update of this file's Sync Impact Report

All development work must verify compliance with this constitution. Complexity beyond these principles must be explicitly justified.

**Version**: 1.3.0 | **Ratified**: 2025-11-17 | **Last Amended**: 2025-11-19
