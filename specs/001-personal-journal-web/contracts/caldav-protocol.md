# CalDAV Protocol Contract

**Created**: 2025-11-17  
**Feature**: Personal Journal Web Application

## Overview

The application implements a CalDAV server to enable bidirectional synchronization with iPhone Calendar. CalDAV (RFC 4791) is the standard protocol for calendar synchronization.

## CalDAV Endpoints

### Base URL

```
https://{domain}/caldav/
```

### Authentication

All CalDAV endpoints require HTTP Basic Authentication:
- Username: Configured CalDAV username
- Password: Configured CalDAV password

### Principal Discovery

**Endpoint**: `/.well-known/caldav`

**Method**: `PROPFIND`

**Description**: Discover CalDAV principal URL

**Response**: Returns principal URL for the user

### Calendar Collection

**Endpoint**: `/caldav/calendars/{username}/journal/`

**Method**: `PROPFIND`

**Description**: Discover calendar collection properties

**Response**: Returns calendar collection information

### Calendar Events

**Endpoint**: `/caldav/calendars/{username}/journal/{event-id}.ics`

**Methods**:
- `GET`: Retrieve calendar event in iCalendar format
- `PUT`: Create or update calendar event
- `DELETE`: Delete calendar event

**Request Format**: iCalendar (.ics) format (RFC 5545)

**Response Format**: iCalendar (.ics) format

### Calendar Query

**Endpoint**: `/caldav/calendars/{username}/journal/`

**Method**: `REPORT`

**Description**: Query calendar events (used by iPhone Calendar for sync)

**Request Body**: CalDAV calendar-query XML

**Response**: Multistatus XML with calendar events

## iCalendar Format

### Event Structure

Each journal entry is represented as a VEVENT in iCalendar format:

```
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Personal Journal//EN
BEGIN:VEVENT
UID:{unique-event-id}
DTSTART:{start-date-time}
DTEND:{end-date-time}
SUMMARY:{journal-entry-title}
DESCRIPTION:{journal-entry-content}
STATUS:CONFIRMED
END:VEVENT
END:VCALENDAR
```

### Field Mappings

| Journal Entry Field | iCalendar Field | Notes |
|---------------------|-----------------|-------|
| id | UID | Unique identifier for event |
| title | SUMMARY | Event title |
| content | DESCRIPTION | Event description |
| date | DTSTART | Event start date/time |
| date | DTEND | Event end date/time (same as start for all-day events) |
| sync_status | STATUS | CONFIRMED, CANCELLED, etc. |

### Completion Status Mapping

| iPhone Calendar Status | iCalendar STATUS | Journal Entry Sync |
|------------------------|------------------|-------------------|
| Not started | CONFIRMED | Default |
| Completed | COMPLETED | completion_status: 'completed' |
| Cancelled | CANCELLED | completion_status: 'cancelled' |

## Sync Operations

### Forward Sync (Web → iPhone)

1. Journal entry created/updated in web
2. Convert to iCalendar format
3. CalDAV PUT request to create/update event
4. iPhone Calendar syncs via CalDAV PROPFIND/REPORT
5. Event appears in iPhone Calendar

### Reverse Sync (iPhone → Web)

1. User modifies event in iPhone Calendar
2. iPhone sends CalDAV PUT request with updated event
3. CalDAV service receives update
4. Parse iCalendar format
5. Update corresponding journal entry in database
6. Set sync_direction to 'iphone_to_web'

### Conflict Detection

Conflicts detected when:
- Event modified in both web and iPhone between syncs
- Last modified timestamps differ
- Content differs between web and iPhone versions

Conflict resolution:
- Last-write-wins (default)
- User notification for manual resolution
- Conflict status stored in journal entry

## CalDAV Compliance

### Required Methods

- `PROPFIND`: Resource discovery
- `REPORT`: Calendar query
- `GET`: Retrieve calendar events
- `PUT`: Create/update calendar events
- `DELETE`: Delete calendar events
- `OPTIONS`: Method discovery

### Required Properties

- `DAV:displayname`: Calendar display name
- `CALDAV:calendar-description`: Calendar description
- `CALDAV:supported-calendar-component-set`: Supported components (VEVENT)
- `CALDAV:calendar-timezone`: Timezone information

### Response Codes

- `200 OK`: Success
- `201 Created`: Resource created
- `204 No Content`: Success (DELETE)
- `207 Multi-Status`: Multi-resource response (REPORT)
- `401 Unauthorized`: Authentication required
- `404 Not Found`: Resource not found
- `409 Conflict`: Conflict detected
- `412 Precondition Failed`: Sync token mismatch

## iPhone Calendar Configuration

### CalDAV Account Setup

1. iPhone Settings → Calendar → Accounts → Add Account
2. Select "Other" → "Add CalDAV Account"
3. Server: `https://{domain}/caldav/`
4. Username: CalDAV username
5. Password: CalDAV password
6. Description: "Personal Journal"

### Sync Behavior

- iPhone Calendar automatically syncs on:
  - App launch
  - Manual refresh
  - Periodic background sync
- Changes in iPhone Calendar sync back to web via CalDAV PUT requests

## Error Handling

### Authentication Errors

- `401 Unauthorized`: Invalid credentials
- Response includes `WWW-Authenticate` header

### Sync Errors

- `409 Conflict`: Sync conflict detected
- `412 Precondition Failed`: Sync token mismatch (retry sync)
- `500 Internal Server Error`: Server error (log and retry)

### Validation Errors

- Invalid iCalendar format: `400 Bad Request`
- Missing required fields: `400 Bad Request`
- Invalid date/time format: `400 Bad Request`

## Security Considerations

- All CalDAV endpoints require HTTPS (constitution requirement)
- HTTP Basic Authentication over HTTPS
- Rate limiting to prevent abuse
- Input validation for all iCalendar data
- SQL injection prevention for database queries

