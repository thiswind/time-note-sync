# Implementation Plan: Personal Journal Web Application

**Branch**: `001-personal-journal-web` | **Date**: 2025-11-19 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-personal-journal-web/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Build a web-based personal journal management tool that allows users to create, edit, and manage journal entries with title, content, and date fields. The system provides bidirectional synchronization with iPhone Calendar via CalDAV protocol, one-click export to iPhone Notes via Shortcuts, and quick navigation to iPhone native apps. The application uses Flask as a monolithic web application with frontend content served from Flask's `templates/` and `static/` directories, SQLite for data storage, and CalDAV for calendar integration, all deployed on Vercel with iOS-first UI/UX design.

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: Python 3.11+  
**Primary Dependencies**: Flask (web framework), caldav-library (CalDAV server), ics (iCalendar generation), Flask-SQLAlchemy (database ORM), SQLite (database), Jinja2 (template engine)  
**Storage**: SQLite database for journal entries and user data  
**Testing**: pytest for unit and integration tests  
**Target Platform**: Web application (Safari on iPhone), deployed on Vercel serverless platform  
**Project Type**: Web application (monolithic Flask application with templates and static assets)  
**Performance Goals**: 
- Journal entry creation: < 30 seconds user time
- Date-based browsing: < 10 seconds to find entry
- Calendar sync: 95% success rate within 5 seconds
- Export to Notes: 98% success rate within 3 seconds
**Constraints**: 
- Must work in native browsers without third-party installations
- Must use only iPhone built-in apps (Calendar, Notes, Shortcuts)
- All data encrypted in transit (HTTPS/TLS mandatory)
- Single-user application (owner-only access)
- Must use industry-standard protocols (CalDAV, HTTPS) for long-term compatibility
- Must use monolithic Flask structure (frontend in templates/ and static/ directories per constitution)
**Scale/Scope**: 
- Single-user personal journal application
- Typical usage: 10-100 journal entries per month
- Calendar sync events: 10-100 events per month
- Export operations: occasional (backup/portability)

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
specs/001-personal-journal-web/
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
app.py                 # Flask application entry point
templates/             # HTML templates (Jinja2)
├── base.html         # Base template
├── index.html         # Home page
├── entry_detail.html # Entry detail/edit page
├── login.html         # Login page
└── settings.html      # Settings page
static/                # Static assets (CSS, JavaScript, images)
├── css/
│   └── main.css      # Main stylesheet (iOS-style)
├── js/
│   ├── main.js       # Main JavaScript (vanilla JS or minimal framework)
│   └── components/   # JavaScript components/modules
└── images/            # Images and icons
models/                # Data models
├── __init__.py
├── journal_entry.py  # Journal Entry model
├── calendar_event.py # Calendar Event model
└── user.py           # User model
services/              # Business logic services
├── __init__.py
├── journal_service.py # Journal CRUD operations
├── caldav_service.py  # CalDAV server implementation
├── ics_generator.py   # iCalendar format generation
├── export_service.py  # Export to Notes functionality
├── native_app_service.py # Native app URL schemes
└── auth_service.py    # Authentication service
api/                   # API routes (for AJAX/fetch calls)
├── __init__.py
├── journal_routes.py  # Journal REST API endpoints
└── caldav_routes.py   # CalDAV protocol endpoints
utils/                 # Utility functions
├── __init__.py
└── validation.py      # Input validation utilities
tests/                 # Test files
├── unit/
│   ├── test_journal_service.py
│   ├── test_caldav_service.py
│   ├── test_ics_generator.py
│   └── test_export_service.py
├── integration/
│   └── test_caldav_sync.py
└── contract/
    └── test_caldav_protocol.py
requirements.txt       # Python dependencies
config.py              # Configuration and environment variables
vercel.json            # Vercel deployment configuration
.gitignore
README.md
```

**Structure Decision**: Monolithic Flask application structure per constitution requirement. Frontend content (HTML templates, CSS, JavaScript) is served directly from Flask's `templates/` and `static/` directories. No separate frontend build process or frontend server. All frontend assets are integrated into the Flask application structure. This simplifies deployment, reduces complexity, and eliminates the need for separate build processes while maintaining iOS-first UI/UX design through CSS and JavaScript.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| CalDAV server implementation | Required for bidirectional calendar sync with iPhone | Direct API integration rejected because iPhone Calendar requires CalDAV protocol for native integration |
| Multiple protocol support (CalDAV, HTTPS, URL schemes) | Required for iPhone native app integration | Single protocol rejected because different iPhone apps require different integration methods |
