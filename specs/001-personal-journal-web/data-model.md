# Data Model: Personal Journal Web Application

**Created**: 2025-11-17  
**Feature**: Personal Journal Web Application

## Overview

The data model consists of three core entities: Journal Entry, Calendar Event, and User. The relationships between these entities support bidirectional calendar synchronization and user authentication.

## Entities

### Journal Entry

Represents a single journal entry created by the user in the web application.

**Attributes**:
- `id` (Integer, Primary Key): Unique identifier for the journal entry
- `title` (String, Required): Title of the journal entry
- `content` (Text, Required): Main content/body of the journal entry
- `date` (Date, Required): Date associated with the journal entry (defaults to current date if not provided)
- `created_at` (DateTime, Required): Timestamp when the entry was created
- `updated_at` (DateTime, Required): Timestamp when the entry was last modified
- `calendar_event_id` (String, Optional): External calendar event ID from iPhone Calendar (for bidirectional sync)
- `sync_status` (Enum, Required): Current sync status - values: 'not_synced', 'synced', 'sync_pending', 'sync_conflict'
- `completion_status` (Enum, Optional): Completion status synced from calendar - values: 'not_started', 'in_progress', 'completed', 'cancelled' (stored as metadata per FR-008)
- `user_id` (Integer, Foreign Key, Required): Reference to the user who owns this entry

**Relationships**:
- Belongs to one User (many-to-one)
- May have one associated Calendar Event (one-to-one, optional)

**Validation Rules**:
- Title must not be empty (minimum 1 character)
- Content must not be empty (minimum 1 character)
- Date must be a valid date
- Title maximum length: 200 characters
- Content maximum length: 10,000 characters

**State Transitions**:
- `not_synced` → `sync_pending`: When user enables sync or modifies entry
- `sync_pending` → `synced`: When sync to iPhone Calendar succeeds
- `synced` → `sync_pending`: When entry is modified after sync
- `synced` → `sync_conflict`: When conflict detected during bidirectional sync
- `sync_conflict` → `synced`: When conflict is resolved

**Indexes**:
- Primary key on `id`
- Index on `user_id` for efficient user queries
- Index on `date` for date-based browsing
- Index on `calendar_event_id` for sync lookups
- Index on `sync_status` for sync operations

---

### Calendar Event

Represents a calendar event synced from or to iPhone Calendar via CalDAV.

**Attributes**:
- `id` (Integer, Primary Key): Unique identifier for the calendar event record
- `external_event_id` (String, Unique, Required): Calendar event ID from iPhone Calendar (CalDAV UID)
- `title` (String, Required): Event title
- `start_datetime` (DateTime, Required): Event start date and time
- `end_datetime` (DateTime, Optional): Event end date and time
- `description` (Text, Optional): Event description/notes
- `completion_status` (Enum, Optional): Completion status - values: 'not_started', 'in_progress', 'completed', 'cancelled'
- `notes` (Text, Optional): Additional notes/remarks added in iPhone Calendar
- `journal_entry_id` (Integer, Foreign Key, Optional): Reference to associated journal entry (if created from journal)
- `last_synced_at` (DateTime, Required): Timestamp of last successful sync
- `sync_direction` (Enum, Required): Direction of last sync - values: 'web_to_iphone', 'iphone_to_web', 'bidirectional'
- `user_id` (Integer, Foreign Key, Required): Reference to the user who owns this event

**Relationships**:
- Belongs to one User (many-to-one)
- May be associated with one Journal Entry (one-to-one, optional)

**Validation Rules**:
- External event ID must be unique
- Title must not be empty (minimum 1 character)
- Start datetime must be valid
- End datetime must be after start datetime (if provided)
- Title maximum length: 200 characters
- Description maximum length: 10,000 characters
- Notes maximum length: 5,000 characters

**State Transitions**:
- Event created in web → `sync_direction: 'web_to_iphone'`
- Event modified in iPhone → `sync_direction: 'iphone_to_web'`
- Event modified in both → Conflict detection triggered

**Indexes**:
- Primary key on `id`
- Unique index on `external_event_id`
- Index on `journal_entry_id` for journal entry lookups
- Index on `user_id` for efficient user queries
- Index on `last_synced_at` for sync operations

---

### User

Represents the authenticated user/owner of the journal entries.

**Attributes**:
- `id` (Integer, Primary Key): Unique identifier for the user
- `username` (String, Unique, Required): Username for authentication
- `password_hash` (String, Required): Hashed password (using Werkzeug PBKDF2)
- `email` (String, Optional): Email address (for future use)
- `calendar_sync_enabled` (Boolean, Default: False): Whether calendar sync is enabled
- `calendar_sync_mode` (Enum, Default: 'manual'): Sync mode - values: 'automatic', 'manual'
- `caldav_username` (String, Optional): Username for CalDAV authentication
- `caldav_password_hash` (String, Optional): Hashed password for CalDAV authentication
- `created_at` (DateTime, Required): Timestamp when user account was created
- `last_login_at` (DateTime, Optional): Timestamp of last successful login

**Relationships**:
- Owns multiple Journal Entries (one-to-many)
- Owns multiple Calendar Events (one-to-many)

**Validation Rules**:
- Username must be unique
- Username minimum length: 3 characters
- Username maximum length: 50 characters
- Username must contain only alphanumeric characters and underscores
- Password must meet minimum security requirements (handled by authentication service)
- Email must be valid format (if provided)

**Indexes**:
- Primary key on `id`
- Unique index on `username`
- Index on `calendar_sync_enabled` for sync operations

---

## Database Schema

### Tables

```sql
-- Users table
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    calendar_sync_enabled BOOLEAN DEFAULT 0,
    calendar_sync_mode VARCHAR(20) DEFAULT 'manual',
    caldav_username VARCHAR(50),
    caldav_password_hash VARCHAR(255),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_login_at TIMESTAMP
);

-- Journal entries table
CREATE TABLE journal_entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    date DATE NOT NULL,
    calendar_event_id VARCHAR(255),
    sync_status VARCHAR(20) NOT NULL DEFAULT 'not_synced',
    completion_status VARCHAR(20),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_date (date),
    INDEX idx_calendar_event_id (calendar_event_id),
    INDEX idx_sync_status (sync_status)
);

-- Calendar events table
CREATE TABLE calendar_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    external_event_id VARCHAR(255) UNIQUE NOT NULL,
    journal_entry_id INTEGER,
    title VARCHAR(200) NOT NULL,
    start_datetime TIMESTAMP NOT NULL,
    end_datetime TIMESTAMP,
    description TEXT,
    completion_status VARCHAR(20),
    notes TEXT,
    sync_direction VARCHAR(20) NOT NULL,
    last_synced_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (journal_entry_id) REFERENCES journal_entries(id) ON DELETE SET NULL,
    INDEX idx_user_id (user_id),
    INDEX idx_journal_entry_id (journal_entry_id),
    INDEX idx_external_event_id (external_event_id),
    INDEX idx_last_synced_at (last_synced_at)
);
```

## Data Relationships Diagram

```
User (1) ──────< (many) Journal Entry
  │
  │ (1) ──────< (many) Calendar Event
  │
  └─── Calendar Event (optional) ────> (1) Journal Entry
```

## Data Flow

### Journal Entry Creation Flow

1. User creates journal entry via web form
2. Entry saved to database with `sync_status: 'not_synced'`
3. If calendar sync enabled:
   - Entry converted to iCalendar format
   - CalDAV service creates calendar event
   - Entry `sync_status` updated to `sync_pending`
   - iPhone Calendar syncs via CalDAV
   - Entry `sync_status` updated to `synced`
   - `calendar_event_id` stored in journal entry

### Bidirectional Sync Flow

**Web → iPhone**:
1. User modifies journal entry in web
2. Entry `sync_status` updated to `sync_pending`
3. CalDAV service updates corresponding calendar event
4. iPhone Calendar syncs changes
5. Entry `sync_status` updated to `synced`

**iPhone → Web**:
1. User modifies calendar event in iPhone Calendar
2. iPhone sends CalDAV update request
3. CalDAV service receives update
4. Calendar Event record updated in database
5. Associated Journal Entry updated (if linked)
6. `sync_direction` set to `'iphone_to_web'`

### Conflict Resolution

When both web and iPhone modify the same entry simultaneously:
1. Conflict detected during sync
2. Entry `sync_status` set to `sync_conflict`
3. User notified of conflict
4. User chooses resolution (keep web version, keep iPhone version, merge)
5. Resolution applied
6. Entry `sync_status` updated to `synced`

## Data Validation

### Journal Entry Validation

- **Title**: Required, 1-200 characters, not empty
- **Content**: Required, 1-10,000 characters, not empty
- **Date**: Required, valid date, defaults to current date if not provided

### Calendar Event Validation

- **External Event ID**: Required, unique, valid CalDAV UID format
- **Title**: Required, 1-200 characters, not empty
- **Start Datetime**: Required, valid datetime
- **End Datetime**: Optional, must be after start datetime if provided

### User Validation

- **Username**: Required, unique, 3-50 characters, alphanumeric and underscores only
- **Password**: Required, minimum 8 characters, validated by authentication service
- **Email**: Optional, valid email format if provided

## Data Migration Considerations

### Future Schema Changes

- Version tracking for schema migrations
- Backward compatibility for API contracts
- Data migration scripts for schema updates
- Backup strategy before migrations

### Backup Strategy

- Regular SQLite database backups
- Export to JSON format for portability
- Cloud storage backup (optional)
- Version history for journal entries (future enhancement)

