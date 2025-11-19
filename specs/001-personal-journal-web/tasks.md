# Tasks: Personal Journal Web Application

**Input**: Design documents from `/specs/001-personal-journal-web/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., [US1], [US2], [US3])
- Include exact file paths in descriptions

## Path Conventions

- **Web app (Flask monolithic)**: `templates/`, `static/`, `models/`, `services/`, `api/`, `tests/` at repository root
- All frontend assets in `templates/` and `static/` directories (no separate frontend build process)

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project structure per implementation plan (app.py, templates/, static/, models/, services/, api/, tests/ directories)
- [x] T002 Initialize Python project with Flask dependencies in requirements.txt
- [x] T003 [P] Configure Black formatting tool in pyproject.toml (constitution requirement)
- [x] T004 [P] Configure lint checks in pyproject.toml (constitution requirement)
- [x] T005 [P] Create Vercel deployment configuration in vercel.json
- [x] T006 [P] Create .gitignore file for Python project
- [x] T007 [P] Create README.md with project overview and setup instructions

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T008 Setup SQLite database schema and migrations framework in models/__init__.py
- [x] T009 [P] Create User model in models/user.py (authentication, owner-only access per constitution)
- [x] T010 [P] Create Journal Entry model in models/journal_entry.py (per data-model.md)
- [x] T011 [P] Create Calendar Event model in models/calendar_event.py (per data-model.md)
- [x] T012 [P] Implement authentication/authorization framework in services/auth_service.py (owner-only access, prevent unauthorized access per constitution)
- [x] T013 [P] Setup Flask-Login session management in app.py
- [x] T014 [P] Setup API routing and middleware structure in api/__init__.py
- [x] T015 Create base Flask application structure in app.py
- [x] T016 [P] Configure error handling and logging infrastructure in config.py (important operations must have logging per constitution)
- [x] T017 [P] Setup environment configuration management in config.py
- [x] T018 [P] Configure HTTPS/TLS for all data transmission (constitution requirement - Vercel automatic SSL)
- [x] T019 [P] Verify mature, mainstream libraries and standard protocols are selected (constitution requirement) - document in requirements.txt
- [x] T020 [P] Setup database connection and SQLAlchemy initialization in app.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Create and Manage Personal Journal Entries (Priority: P1)

**Goal**: Users can create, edit, and delete journal entries with title, content, and date fields

**Independent Test**: Create a new journal entry with title, content, and date, edit it, and delete it. This delivers the basic journaling functionality that users expect.

- [x] T021 [US1] Implement JournalService CRUD operations in services/journal_service.py
- [x] T022 [US1] Implement POST /api/journal/entries endpoint in api/journal_routes.py (create entry)
- [x] T023 [US1] Implement GET /api/journal/entries endpoint in api/journal_routes.py (list entries)
- [x] T024 [US1] Implement GET /api/journal/entries/{entryId} endpoint in api/journal_routes.py (get entry)
- [x] T025 [US1] Implement PUT /api/journal/entries/{entryId} endpoint in api/journal_routes.py (update entry)
- [x] T026 [US1] Implement DELETE /api/journal/entries/{entryId} endpoint in api/journal_routes.py (delete entry)
- [x] T027 [US1] Add validation for journal entry fields (title, content, date) in services/journal_service.py (FR-029: auto-generate "Untitled" for empty title)
- [x] T028 [US1] Add error handling for journal operations in api/journal_routes.py
- [x] T029 [US1] Add logging for journal CRUD operations in services/journal_service.py (constitution requirement)
- [x] T030 [US1] Create base HTML template in templates/base.html (iOS-style base layout)
- [x] T031 [US1] Create login page template in templates/login.html (iOS-style login UI)
- [x] T032 [US1] Create home page template in templates/index.html (journal list with iOS-style UI)
- [x] T033 [US1] Create entry detail/edit page template in templates/entry_detail.html (entry detail/edit with iOS-style UI)
- [x] T034 [US1] Create main CSS stylesheet in static/css/main.css (iOS Human Interface Guidelines styling)
- [x] T035 [US1] Create main JavaScript file in static/js/main.js (journal CRUD operations, AJAX calls)
- [x] T036 [US1] Implement API client functions in static/js/main.js (journal CRUD operations using Fetch API)
- [x] T037 [US1] Implement journal list display functionality in static/js/main.js
- [x] T038 [US1] Implement journal entry creation form in static/js/main.js
- [x] T039 [US1] Implement journal entry edit form in static/js/main.js
- [x] T040 [US1] Implement journal entry deletion functionality in static/js/main.js
- [x] T041 [US1] Design UI/UX following iOS system style and operation habits in templates/ and static/css/main.css (constitution requirement)
- [x] T042 [US1] Verify UI aligns with iOS Human Interface Guidelines in templates/ and static/css/main.css (constitution requirement)
- [x] T043 [US1] Implement UTC storage and local timezone display in services/journal_service.py (FR-025)
- [ ] T044 [US1] Code review before merge (constitution requirement)

---

## Phase 4: User Story 2 - Browse Journal Entries by Date (Priority: P2)

**Goal**: Users can browse and view journal entries organized by date

**Independent Test**: Create multiple entries on different dates and verify they can be accessed through date-based navigation. This delivers the ability to review past entries.

- [ ] T045 [US2] Add date filtering to GET /api/journal/entries endpoint in api/journal_routes.py (query parameter: date)
- [ ] T046 [US2] Implement date-based query logic in services/journal_service.py (filter by date, support date range)
- [ ] T047 [US2] Add date picker UI component in templates/index.html (iOS calendar interface patterns)
- [ ] T048 [US2] Implement date navigation in static/js/main.js (previous/next date, date selection)
- [ ] T049 [US2] Add empty state message for dates with no entries in templates/index.html
- [ ] T050 [US2] Add logging for date-based browsing operations in services/journal_service.py
- [ ] T051 [US2] Implement date-based entry filtering in static/js/main.js
- [ ] T052 [US2] Code review before merge (constitution requirement)

---

## Phase 5: User Story 3 - Bidirectional Sync with iPhone Calendar (Priority: P3)

**Goal**: Journal entries sync bidirectionally with iPhone Calendar automatically or manually

**Independent Test**: Create a journal entry, sync it to iPhone Calendar (automatically or manually), verify it appears in the calendar, then modify it in the calendar (e.g., marking as complete, adding notes) and verify the change syncs back to the web application.

- [ ] T053 [P] [US3] Install and configure caldav-library in requirements.txt
- [ ] T054 [P] [US3] Install and configure ics library in requirements.txt
- [ ] T055 [US3] Implement CalDAV service in services/caldav_service.py (CalDAV server functionality)
- [ ] T056 [US3] Implement iCalendar generator in services/ics_generator.py (generate .ics files from journal entries)
- [ ] T057 [US3] Implement calendar sync logic (web to iPhone) in services/caldav_service.py
- [ ] T058 [US3] Implement calendar sync logic (iPhone to web) in services/caldav_service.py
- [ ] T059 [US3] Implement conflict detection and last-write-wins resolution in services/caldav_service.py (FR-018)
- [ ] T060 [US3] Implement completion status sync from calendar to journal entry in services/caldav_service.py (FR-008)
- [ ] T061 [US3] Implement automatic deletion of journal entries when calendar events are deleted in services/caldav_service.py (FR-024)
- [ ] T062 [US3] Implement UTC storage and local timezone display for calendar sync in services/caldav_service.py (FR-025)
- [ ] T063 [US3] Implement sequential time offsets for multiple entries on same date/time in services/caldav_service.py (FR-028)
- [ ] T064 [US3] Implement content truncation with ellipsis for calendar sync in services/ics_generator.py (FR-026)
- [ ] T065 [US3] Implement text content preservation and formatting stripping for calendar sync in services/ics_generator.py (FR-027)
- [ ] T066 [US3] Implement offline detection and sync disable in services/caldav_service.py (FR-023)
- [ ] T067 [US3] Implement error handling and manual retry for sync failures in services/caldav_service.py (FR-020)
- [ ] T068 [US3] Implement error handling for calendar full/permission restrictions in services/caldav_service.py (edge case resolution)
- [ ] T069 [US3] Implement POST /api/journal/entries/{entryId}/sync endpoint in api/journal_routes.py
- [ ] T070 [US3] Implement POST /api/calendar/sync endpoint in api/caldav_routes.py (manual sync trigger)
- [ ] T071 [US3] Implement GET /api/calendar/events endpoint in api/caldav_routes.py
- [ ] T072 [US3] Implement CalDAV protocol endpoints in api/caldav_routes.py (PROPFIND, GET, PUT, DELETE)
- [ ] T073 [US3] Implement POST /api/calendar/events/{eventId}/create-entry endpoint in api/caldav_routes.py (create journal entry from calendar event, FR-009)
- [ ] T074 [US3] Implement service method to create journal entry from calendar event in services/journal_service.py (FR-009)
- [ ] T075 [US3] Update Journal Entry model to include sync_status, calendar_event_id, and completion_status in models/journal_entry.py
- [ ] T076 [US3] Update User model to include calendar sync preferences in models/user.py
- [ ] T077 [US3] Create calendar sync settings page template in templates/settings.html
- [ ] T078 [US3] Implement sync service in static/js/main.js (sync API calls)
- [ ] T079 [US3] Add sync status indicators in templates/index.html
- [ ] T080 [US3] Add sync control UI in templates/settings.html (enable/disable auto sync, manual sync button)
- [ ] T081 [US3] Add logging for calendar sync operations in services/caldav_service.py (constitution requirement)
- [ ] T082 [US3] Code review before merge (constitution requirement)

---

## Phase 6: User Story 4 - Export to iPhone Notes (Priority: P4)

**Goal**: Users can export single or multiple journal entries to iPhone Notes with one click

**Independent Test**: Create journal entries, select one or multiple entries, click the export button, and verify the entries appear in iPhone Notes with all content preserved.

- [ ] T083 [US4] Implement export service for single entry in services/export_service.py (generate Shortcuts URL)
- [ ] T084 [US4] Implement export service for multiple entries in services/export_service.py (batch export)
- [ ] T085 [US4] Implement content truncation with ellipsis for Notes export in services/export_service.py (FR-026)
- [ ] T086 [US4] Implement text content preservation and formatting stripping for Notes export in services/export_service.py (FR-027)
- [ ] T087 [US4] Implement POST /api/journal/entries/{entryId}/export endpoint in api/journal_routes.py
- [ ] T088 [US4] Implement POST /api/journal/entries/batch-export endpoint in api/journal_routes.py
- [ ] T089 [US4] Add export functionality to static/js/main.js (export API calls)
- [ ] T090 [US4] Add export button to entry detail page in templates/entry_detail.html
- [ ] T091 [US4] Add batch export selection UI in templates/index.html (multi-select interface)
- [ ] T092 [US4] Implement Shortcuts URL scheme handling in static/js/main.js (shortcuts://run-shortcut)
- [ ] T093 [US4] Add error handling for export failures in static/js/main.js (FR-020, edge case: Notes app unavailable)
- [ ] T094 [US4] Add logging for export operations in services/export_service.py (constitution requirement)
- [ ] T095 [US4] Code review before merge (constitution requirement)

---

## Phase 7: User Story 5 - Quick Access to iPhone Native Apps (Priority: P5)

**Goal**: Users can quickly jump from the web application to iPhone native apps (Calendar, Notes)

**Independent Test**: Click a link to open Calendar or Notes and verify the native app opens correctly to the relevant content.

- [ ] T096 [US5] Implement native app URL scheme service in services/native_app_service.py (calshow://, shortcuts://)
- [ ] T097 [US5] Implement GET /api/journal/entries/{entryId}/open-calendar endpoint in api/journal_routes.py
- [ ] T098 [US5] Implement GET /api/journal/entries/{entryId}/open-notes endpoint in api/journal_routes.py
- [ ] T099 [US5] Add "Open in Calendar" link to entry detail page in templates/entry_detail.html
- [ ] T100 [US5] Add "Open in Notes" link to entry detail page in templates/entry_detail.html
- [ ] T101 [US5] Implement native app link handlers in static/js/main.js (URL scheme navigation)
- [ ] T102 [US5] Add error handling for unavailable native apps in static/js/main.js (FR-020)
- [ ] T103 [US5] Code review before merge (constitution requirement)

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Final polish, testing, and cross-cutting improvements

- [ ] T104 [P] Add comprehensive error handling across all API endpoints in api/
- [ ] T105 [P] Add input validation utilities in utils/validation.py
- [ ] T106 [P] Implement comprehensive logging across all services (constitution requirement)
- [ ] T107 [P] Add performance optimizations (database indexes, query optimization)
- [ ] T108 [P] Verify all success criteria from spec.md are met
- [ ] T109 [P] Run quickstart.md validation (test all user scenarios)
- [ ] T110 [P] Final code review before production deployment
- [ ] T111 [P] Update README.md with deployment and usage instructions
- [ ] T112 [P] Create deployment checklist

---

## Dependencies & Story Completion Order

**Story Dependencies**:
- **US1** (P1) must complete first - core functionality required by all other stories
- **US2** (P2) depends on US1 - requires journal entries to browse
- **US3** (P3) depends on US1 - requires journal entries to sync
- **US4** (P4) depends on US1 - requires journal entries to export
- **US5** (P5) depends on US1, US3, US4 - requires synced entries and exported entries for native app links

**Execution Order**:
1. Phase 1: Setup (shared infrastructure)
2. Phase 2: Foundational (blocking prerequisites)
3. Phase 3: US1 - Create and Manage Entries (P1) - **MVP SCOPE**
4. Phase 4: US2 - Browse by Date (P2)
5. Phase 5: US3 - Calendar Sync (P3)
6. Phase 6: US4 - Export to Notes (P4)
7. Phase 7: US5 - Native App Links (P5)
8. Phase 8: Polish & Cross-Cutting Concerns

## Parallel Execution Examples

**Within US1**:
- T021-T029 (backend services/API) can run in parallel with T030-T042 (frontend templates/CSS)
- T034-T035 (CSS/JS setup) can run in parallel with T036-T040 (JS functionality)

**Within US3**:
- T053-T054 (dependency installation) can run in parallel
- T055-T068 (backend sync logic) can run in parallel with T077-T080 (frontend UI)

**Cross-Phase**:
- Phase 8 polish tasks (T104-T112) marked [P] can run in parallel after user stories complete

## Implementation Strategy

**MVP Scope**: Phase 1 + Phase 2 + Phase 3 (US1 only)
- Delivers core journaling functionality
- Independently testable and deployable
- Provides foundation for all other features

**Incremental Delivery**:
- Each user story phase is independently testable
- Can be deployed incrementally after MVP
- Each phase adds value without breaking existing functionality

**Testing Strategy**:
- Each user story has independent test criteria
- Manual testing via quickstart.md scenarios
- Unit tests for services (if requested)
- Integration tests for API endpoints (if requested)
