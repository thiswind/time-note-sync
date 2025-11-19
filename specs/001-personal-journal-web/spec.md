# Feature Specification: Personal Journal Web Application

**Feature Branch**: `001-personal-journal-web`  
**Created**: 2025-11-17  
**Status**: Draft  
**Input**: User description: "我要做一个网页工具，用来创建和管理个人日志，按日期查阅。日志可以与 iPhone 日历双向同步，并支持一键导出到 iPhone 备忘录，也能网页端一键跳转到 iPhone 原生应用。用户界面要求尽量接近 iOS 系统的风格和操作习惯，便于 iPhone 用户无障碍上手。所有数据仅本人可访问，传输需加密，无需安装其他软件。"

**Updated**: 2025-11-17 (with detailed requirements and clarifications), 2025-11-19 (edge case clarifications)

## Clarifications

### Session 2025-11-17

- Q: When a journal entry is modified simultaneously in both the web application and iPhone Calendar, how should the system handle the conflict? → A: Last-write-wins (no user notification) - Automatically keep the most recent change
- Q: When the user is offline and tries to sync with iPhone Calendar, how should the system handle this? → A: Disable sync functionality when offline (no queue) - Sync operations are disabled when offline, user must retry when connection is available
- Q: When a user deletes a calendar event in iPhone Calendar that was synced from a journal entry, what should happen to the journal entry? → A: Delete the journal entry from the web application automatically
- Q: When a user marks a calendar event as "completed" in iPhone Calendar, should this completion status sync back to the journal entry? → A: Yes, sync completion status back to journal entry (store as metadata or in content)
- Q: When sync fails due to network issues, should the system retry automatically or require manual retry? → A: Show error message and require manual retry
- Q: How should the system handle date/timezone differences between the web app and iPhone? → A: Store all dates/times in UTC, display in user's local timezone
- Q: How should the system handle very long journal entries (title or content) when syncing with Calendar or exporting to Notes? → A: Truncate with ellipsis for sync/export, preserve full content in database
- Q: How should the system handle special characters and formatting when syncing with Calendar or exporting to Notes? → A: Preserve text content, strip formatting, escape special characters
- Q: When a user has multiple journal entries on the same date and time, how should the system handle them for calendar sync? → A: Allow multiple entries, use sequential time offsets for calendar sync
- Q: How should the system handle journal entries with missing required fields (e.g., no title or no content)? → A: Auto-generate default values (e.g., "Untitled" for empty title)

### Session 2025-11-19

- Q: What happens when the user's iPhone Calendar is full or has permission restrictions? → A: Show error message explaining the issue, allow user to free calendar space or grant permissions, then retry sync
- Q: What happens when the user tries to export to Notes but the Notes app is not available? → A: Show error message indicating Notes app is unavailable, suggest user check Shortcuts app or retry later

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Create and Manage Personal Journal Entries (Priority: P1)

As a user, I want to create, edit, and delete personal journal entries with title, content, and date fields so that I can record and manage my daily thoughts and experiences in a structured way.

**Why this priority**: This is the core functionality of the application. Without the ability to create and manage journal entries, the application has no value. All other features depend on this foundation.

**Independent Test**: Can be fully tested by creating a new journal entry with title, content, and date, editing it, and deleting it. This delivers the basic journaling functionality that users expect.

**Acceptance Scenarios**:

1. **Given** I am on the journal creation page, **When** I enter a title, content, and date, then save, **Then** a new journal entry is created with all three fields and displayed in my journal list
2. **Given** I have an existing journal entry, **When** I edit the title, content, or date and save, **Then** the changes are persisted and displayed
3. **Given** I have an existing journal entry, **When** I delete it, **Then** the entry is removed from my journal list
4. **Given** I am creating a journal entry, **When** I view the interface, **Then** it follows iOS design patterns and feels familiar with a clean, simple web interface
5. **Given** I am creating a journal entry, **When** I do not provide a date, **Then** the system uses the current date as the default

---

### User Story 2 - Browse Journal Entries by Date (Priority: P2)

As a user, I want to browse and view my journal entries organized by date so that I can easily find entries from specific days.

**Why this priority**: Date-based organization is essential for journaling workflows. Users need to navigate their past entries efficiently. This feature makes the journal useful for reflection and review.

**Independent Test**: Can be fully tested by creating multiple entries on different dates and verifying they can be accessed through date-based navigation. This delivers the ability to review past entries.

**Acceptance Scenarios**:

1. **Given** I have journal entries on multiple dates, **When** I select a specific date, **Then** I see all entries for that date
2. **Given** I am viewing entries by date, **When** I navigate to a different date, **Then** the entries for that date are displayed
3. **Given** I have no entries for a date, **When** I select that date, **Then** I see an appropriate empty state message
4. **Given** I am browsing by date, **When** I view the date picker, **Then** it follows iOS calendar interface patterns

---

### User Story 3 - Bidirectional Sync with iPhone Calendar (Priority: P3)

As a user, I want my journal entries to sync bidirectionally with my iPhone Calendar automatically or manually so that I can see journal-related events in my calendar, and changes made in either location stay synchronized.

**Why this priority**: Calendar integration adds significant value by connecting journal entries with scheduled events and allowing users to create entries from calendar items. This enhances the journaling experience by providing context. Bidirectional sync ensures data consistency across platforms.

**Independent Test**: Can be fully tested by creating a journal entry, syncing it to iPhone Calendar (automatically or manually), verifying it appears in the calendar, then modifying it in the calendar (e.g., marking as complete, adding notes) and verifying the change syncs back to the web application. This delivers full calendar integration functionality.

**Acceptance Scenarios**:

1. **Given** I have created or modified a journal entry, **When** automatic sync is enabled, **Then** a corresponding event appears or updates in my iPhone Calendar automatically
2. **Given** I have created or modified a journal entry, **When** I manually trigger sync, **Then** a corresponding event appears or updates in my iPhone Calendar
3. **Given** I have a calendar event synced from a journal entry, **When** I modify the event in iPhone Calendar (e.g., mark as complete, add notes/remarks), **Then** the journal entry is updated accordingly in the web application
4. **Given** I have a calendar event in my iPhone Calendar, **When** I choose to create a journal entry from it, **Then** a new journal entry is created with the event details (title, date, description)
5. **Given** I disable calendar sync, **When** I view my journal entries, **Then** they remain accessible but no longer sync with the calendar
6. **Given** sync is enabled, **When** I create or modify multiple journal entries, **Then** the sync process minimizes manual steps and operates efficiently

---

### User Story 4 - Export to iPhone Notes (Priority: P4)

As a user, I want to export single or multiple journal entries to iPhone Notes with one click so that I can access them in the native Notes app for backup or alternative access.

**Why this priority**: Export functionality provides users with backup and alternative access to their journal entries. The one-click export makes it convenient to share entries with the native Notes app, supporting data portability and user convenience.

**Independent Test**: Can be fully tested by creating journal entries, selecting one or multiple entries, clicking the export button, and verifying the entries appear in iPhone Notes with all content preserved. This delivers export functionality.

**Acceptance Scenarios**:

1. **Given** I have a journal entry, **When** I click the one-click export to Notes button, **Then** the entry is created in my iPhone Notes app with title, content, and date preserved
2. **Given** I have multiple journal entries, **When** I select multiple entries and click export, **Then** all selected entries are created in iPhone Notes
3. **Given** I export an entry to Notes, **When** I view it in the Notes app, **Then** the title, content, and date information are preserved accurately
4. **Given** I have exported entries to Notes, **When** I view them in the Notes app, **Then** they are accessible using only the native Notes application without additional software

---

### User Story 5 - Quick Access to iPhone Native Apps (Priority: P5)

As a user, I want to quickly jump from the web application to iPhone native apps (Calendar, Notes) so that I can seamlessly switch between the web tool and native applications to view or edit corresponding content.

**Why this priority**: Quick access to native apps improves user experience by reducing friction when switching between the web app and iPhone system apps. This enhances the integration feel and allows users to leverage native app features.

**Independent Test**: Can be fully tested by clicking a link to open Calendar or Notes and verifying the native app opens correctly to the relevant content. This delivers quick navigation functionality.

**Acceptance Scenarios**:

1. **Given** I am viewing a journal entry that is synced to Calendar, **When** I click the "Open in Calendar" link, **Then** the iPhone Calendar app opens to the relevant date and event
2. **Given** I am viewing a journal entry that has been exported to Notes, **When** I click the "Open in Notes" link, **Then** the iPhone Notes app opens to the corresponding note
3. **Given** I am on any page, **When** I click a native app link, **Then** the appropriate iPhone app opens using standard URL schemes without requiring additional software
4. **Given** I click a native app link, **When** the corresponding app is not available, **Then** I receive an appropriate error message

---

### Edge Cases

- What happens when the user is offline and tries to sync with iPhone Calendar? → **Resolution**: Sync functionality is disabled when offline. The system shows an appropriate error message indicating that sync requires an internet connection. User must retry sync when connection is restored.
- How does the system handle calendar sync conflicts when an entry is modified in both places simultaneously? → **Resolution**: Last-write-wins strategy - the system automatically keeps the most recent change based on modification timestamp, with no user notification required.
- What happens when the user's iPhone Calendar is full or has permission restrictions? → **Resolution**: When calendar sync fails due to iPhone Calendar being full or lacking permissions, the system displays an error message explaining the issue (e.g., "Calendar is full" or "Calendar access denied"). The user can then free calendar space or grant permissions in iPhone Settings, and retry the sync operation. The journal entry remains in the web application with sync status marked as failed until sync succeeds.
- How does the system handle very long journal entries (title or content) when syncing with Calendar or exporting to Notes? → **Resolution**: The system preserves the full content in the database. When syncing to Calendar or exporting to Notes, if the content exceeds typical limits, it is truncated with ellipsis (...) to fit within the target system's constraints. The full content remains accessible in the web application.
- What happens when the user tries to export to Notes but the Notes app is not available? → **Resolution**: When export to Notes fails because the Notes app is unavailable or the Shortcuts action fails, the system displays an error message indicating that the Notes app is unavailable (e.g., "Notes app not available" or "Export failed"). The error message suggests the user check the Shortcuts app configuration or retry the export later. The journal entry remains in the web application and can be exported again when the Notes app becomes available.
- How does the system handle date/timezone differences between the web app and iPhone? → **Resolution**: All dates and times are stored in UTC in the database. The system displays dates/times in the user's local timezone (detected from browser/device). When syncing with iPhone Calendar, timezone information is preserved in iCalendar format, and iPhone Calendar handles timezone conversion automatically.
- What happens when the user has multiple journal entries on the same date and time? → **Resolution**: The system allows multiple journal entries on the same date and time. When syncing to Calendar, entries with the same date/time are assigned sequential time offsets (e.g., 10:00, 10:01, 10:02) to ensure each entry appears as a separate calendar event. The original date is preserved, and entries remain distinguishable in the calendar.
- How does the system handle special characters or formatting when syncing with Calendar or exporting to Notes? → **Resolution**: The system preserves all text content including emoji and special characters. Formatting (bold, lists, HTML tags, etc.) is stripped and converted to plain text. Special characters are properly escaped to ensure safe display in Calendar and Notes. The original formatted content remains in the web application database.
- What happens when a calendar event is deleted in iPhone Calendar - should the journal entry be deleted or just unlinked? → **Resolution**: When a calendar event is deleted in iPhone Calendar, the corresponding journal entry is automatically deleted from the web application during the next sync operation.
- How does the system handle calendar events that are marked as complete in iPhone Calendar - should this status sync back to the journal entry? → **Resolution**: Yes, completion status from iPhone Calendar syncs back to the journal entry. The completion status is stored as metadata in the journal entry and can be displayed in the web interface.
- What happens when sync fails due to network issues - should the system retry automatically or require manual retry? → **Resolution**: When sync fails due to network issues, the system displays an error message indicating the failure and requires the user to manually retry the sync operation. No automatic retry is performed.
- How does the system handle journal entries with missing required fields (e.g., no title or no content)? → **Resolution**: The system automatically generates default values for missing required fields. If title is empty, it uses "Untitled" as the default. If content is empty, it uses an empty string (content is still required but can be empty). The system allows saving entries with auto-generated defaults.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST allow users to create new journal entries with title, content, and date fields
- **FR-002**: System MUST allow users to edit existing journal entries (title, content, and date)
- **FR-003**: System MUST allow users to delete journal entries
- **FR-004**: System MUST display journal entries organized by date for "daily browsing"
- **FR-005**: System MUST provide date-based navigation to browse and archive entries by date
- **FR-006**: System MUST support bidirectional synchronization with iPhone Calendar (web to iPhone and iPhone to web)
- **FR-007**: System MUST support automatic or manual trigger for calendar synchronization
- **FR-008**: System MUST sync changes made in iPhone Calendar (e.g., completion status, notes/remarks) back to web journal entries. Completion status must be stored as metadata in the journal entry and displayed in the web interface.
- **FR-009**: System MUST allow users to create journal entries from iPhone Calendar events
- **FR-010**: System MUST allow users to export single or multiple journal entries to iPhone Notes with one click
- **FR-011**: System MUST provide quick links to open iPhone native apps (Calendar, Notes) to corresponding content
- **FR-012**: System MUST implement user authentication (e.g., password) to restrict access to the owner only
- **FR-013**: System MUST encrypt all data in transit using HTTPS/TLS
- **FR-014**: System MUST follow iOS design patterns and Human Interface Guidelines for UI/UX to ensure familiarity for iPhone users
- **FR-015**: System MUST work in native browsers without requiring third-party installations
- **FR-016**: System MUST only use iPhone system built-in tools (Calendar, Notes, Shortcuts) and native browser capabilities
- **FR-017**: System MUST persist journal entries securely
- **FR-018**: System MUST handle calendar sync conflicts using last-write-wins strategy (automatically keep the most recent change based on timestamp)
- **FR-019**: System MUST preserve title, content, and date data when exporting to Notes. Visual formatting is stripped per FR-027, but all text content including emoji and special characters is preserved.
- **FR-020**: System MUST provide appropriate error messages for sync and export failures. When sync fails due to network issues, the system must display an error message and require manual retry (no automatic retry).
- **FR-023**: System MUST disable sync functionality when offline and display an error message indicating that internet connection is required
- **FR-024**: System MUST automatically delete journal entries when their corresponding calendar events are deleted in iPhone Calendar during sync operations
- **FR-021**: System MUST minimize manual steps in synchronization processes to maximize automation
- **FR-022**: System MUST use industry-standard protocols to ensure long-term compatibility and portability
- **FR-025**: System MUST store all dates and times in UTC format and display them in the user's local timezone
- **FR-026**: System MUST preserve full journal entry content in the database. When syncing to Calendar or exporting to Notes, content exceeding target system limits must be truncated with ellipsis while maintaining full content accessibility in the web application.
- **FR-027**: System MUST preserve all text content (including emoji and special characters) when syncing or exporting. Formatting must be stripped and converted to plain text, and special characters must be properly escaped for safe display in Calendar and Notes.
- **FR-028**: System MUST allow multiple journal entries on the same date and time. When syncing to Calendar, entries with identical date/time must be assigned sequential time offsets to ensure each entry appears as a separate calendar event.
- **FR-029**: System MUST automatically generate default values for missing required fields. If title is empty, use "Untitled" as default. Content can be empty but must be explicitly provided (empty string is acceptable).

### Key Entities *(include if feature involves data)*

- **Journal Entry**: Represents a single journal entry created by the user. Key attributes include: unique identifier, title (text), content (text), date (stored in UTC), creation date/time (stored in UTC), last modified date/time (stored in UTC), associated calendar event ID (if synced), sync status, completion status (optional, synced from calendar), owner/user identifier. Relationships: belongs to one user, may have one associated calendar event.

- **Calendar Event**: Represents a calendar event synced from or to iPhone Calendar. Key attributes include: unique identifier, title, date/time (stored in UTC with timezone information), description, completion status, notes/remarks, journal entry ID (if created from journal), calendar event ID (external), last sync timestamp (stored in UTC). Relationships: may be associated with one journal entry.

- **User**: Represents the authenticated user/owner. Key attributes include: unique identifier, authentication credentials (e.g., password), calendar sync preferences (automatic/manual), export preferences, sync settings. Relationships: owns multiple journal entries.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can create a new journal entry in under 30 seconds from the main page
- **SC-002**: Users can browse and find a journal entry from a specific date in under 10 seconds
- **SC-003**: Calendar sync completes successfully for 95% of sync operations within 5 seconds
- **SC-004**: Export to iPhone Notes completes successfully for 98% of export operations within 3 seconds
- **SC-005**: 90% of users can complete their first journal entry creation without referring to documentation
- **SC-006**: The UI is recognizable as iOS-style by 85% of iPhone users in usability testing
- **SC-007**: All data transmission uses encrypted connections (HTTPS/TLS) with no unencrypted data transfer
- **SC-008**: Only authenticated users can access their own journal entries (100% access control compliance)
- **SC-009**: The application loads and is functional in Safari on iPhone without requiring any additional installations
- **SC-010**: Calendar sync conflicts are resolved automatically using last-write-wins strategy in 100% of conflict scenarios (no user intervention required)
- **SC-011**: Synchronization processes complete with minimal manual intervention (automated where possible, manual trigger available when needed)
- **SC-012**: The system maintains compatibility with future system upgrades and device changes through use of industry-standard protocols
- **SC-013**: Users can access all functionality using only native browser and iPhone built-in apps (Calendar, Notes, Shortcuts) without installing third-party software
