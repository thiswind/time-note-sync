# Research & Technology Decisions: Personal Journal Web Application

**Created**: 2025-11-17  
**Feature**: Personal Journal Web Application

## Technology Stack Decisions

### Backend Framework: Flask

**Decision**: Use Flask as the web framework for the backend.

**Rationale**: 
- Flask is a mature, lightweight Python web framework with extensive community support
- Minimal boilerplate, allowing rapid development
- Excellent documentation and ecosystem
- Well-suited for small to medium web applications
- Compatible with Vercel serverless deployment
- Supports both RESTful API and template rendering patterns needed for this application

**Alternatives considered**:
- **FastAPI**: More modern, but adds complexity for a single-user application. Better suited for API-only services.
- **Django**: Too heavyweight for this use case. Includes many features not needed.
- **Bottle**: Too minimal, lacks ecosystem support.

### Database: SQLite

**Decision**: Use SQLite for data storage.

**Rationale**:
- Lightweight, file-based database perfect for single-user applications
- No separate database server required, reducing deployment complexity
- Excellent Python support via SQLAlchemy
- Sufficient for expected scale (10-100 entries per month)
- Easy backup (just copy the database file)
- Works well with Vercel serverless functions (with proper file handling)

**Alternatives considered**:
- **PostgreSQL**: Overkill for single-user application. Requires separate database service.
- **JSON files**: Not suitable for concurrent access and complex queries.
- **Cloud databases (Firebase, Supabase)**: Adds external dependency and cost.

### CalDAV Implementation: caldav-library

**Decision**: Use caldav-library (Python) or Radicale as CalDAV server implementation.

**Rationale**:
- CalDAV is the industry-standard protocol for calendar synchronization
- Required for native iPhone Calendar integration
- caldav-library provides mature CalDAV server capabilities in Python
- Radicale is a standalone CalDAV server that can be integrated
- Both are well-maintained and widely used
- Supports bidirectional sync required by the specification

**Alternatives considered**:
- **Custom CalDAV implementation**: Too complex and error-prone. Industry standard exists.
- **iCloud Calendar API**: Requires Apple Developer account and doesn't support custom servers.
- **Google Calendar API**: Requires OAuth and doesn't support bidirectional sync from custom server.

### iCalendar Format: ics library

**Decision**: Use ics Python library for generating iCalendar (.ics) files.

**Rationale**:
- iCalendar (RFC 5545) is the standard format for calendar data exchange
- ics library is mature and well-maintained
- Simple API for creating and parsing calendar events
- Required for CalDAV protocol compliance
- Handles timezone and date formatting correctly

**Alternatives considered**:
- **Manual .ics file generation**: Error-prone and doesn't handle edge cases.
- **Other libraries**: ics is the most popular and well-maintained option.

### Frontend: Vue.js + Vant UI Framework

**Decision**: Use Vue.js as the frontend framework with Vant UI component library for building the mobile-first interface.

**Rationale**:
- Vue.js is a mature, progressive JavaScript framework with excellent mobile support
- Vant provides iOS-style mobile UI components out of the box, aligning with iOS-first design requirement
- Vant is specifically designed for mobile web applications with iOS-style components
- Vue.js offers reactive data binding and component-based architecture for maintainable code
- Vant components follow iOS Human Interface Guidelines, reducing custom styling effort
- Modern SPA architecture provides better user experience with smooth navigation
- Vant is a mature, mainstream library (constitution requirement)
- Build tools (Vite/Vue CLI) provide efficient development and production builds

**Alternatives considered**:
- **Server-side templates + Vanilla JavaScript**: Rejected because Vant provides ready-made iOS-style components that would require significant custom CSS work to replicate.
- **React + mobile UI library**: Vue.js has a gentler learning curve and Vant is specifically optimized for Vue.
- **Pure CSS iOS styling**: Would require extensive custom development to match iOS design patterns that Vant provides out of the box.

### Deployment: Vercel

**Decision**: Deploy Flask application to Vercel serverless platform.

**Rationale**:
- Vercel provides excellent Python/Flask support
- Automatic HTTPS/SSL certificates (constitution requirement)
- Free tier suitable for personal projects
- Easy CI/CD integration
- Serverless architecture scales automatically
- Good documentation and community support

**Alternatives considered**:
- **Netlify**: Similar to Vercel, but Vercel has better Python support.
- **Heroku**: Requires paid plan for HTTPS and has more complex setup.
- **Self-hosted**: Adds maintenance burden and infrastructure costs.

### Authentication: Flask-Login with Password

**Decision**: Implement simple password-based authentication using Flask-Login.

**Rationale**:
- Flask-Login is mature and well-integrated with Flask
- Password authentication is simple and sufficient for single-user application
- No external OAuth providers needed
- Secure password hashing via Werkzeug
- Session-based authentication works well for web applications

**Alternatives considered**:
- **OAuth2**: Unnecessary complexity for single-user application.
- **JWT tokens**: More complex, not needed for session-based web app.
- **No authentication**: Violates security requirements.

### iPhone Integration: URL Schemes + Shortcuts

**Decision**: Use iPhone URL schemes for app navigation and Shortcuts app for Notes export.

**Rationale**:
- URL schemes (calshow://, shortcuts://) are standard iOS mechanisms
- No third-party SDKs or installations required
- Shortcuts app is built into iOS, meeting "no additional software" requirement
- Allows one-click export to Notes via Shortcuts automation
- Native iOS integration patterns

**Alternatives considered**:
- **Custom iOS app**: Violates "no third-party installations" requirement.
- **Web Share API**: Limited functionality, doesn't support Notes app directly.
- **Email export**: Adds unnecessary steps for user.

## Protocol & Standard Decisions

### CalDAV Protocol

**Decision**: Implement CalDAV server for bidirectional calendar sync.

**Rationale**:
- CalDAV (RFC 4791) is the industry standard for calendar synchronization
- Required for native iPhone Calendar integration
- Supports bidirectional sync (web ↔ iPhone)
- Well-documented protocol with mature libraries
- Ensures long-term compatibility (constitution requirement)

### iCalendar Format (RFC 5545)

**Decision**: Use iCalendar format for calendar event representation.

**Rationale**:
- Standard format for calendar data exchange
- Required by CalDAV protocol
- Supported by all major calendar applications
- Handles timezones, recurring events, and metadata correctly

### HTTPS/TLS

**Decision**: Use HTTPS for all data transmission.

**Rationale**:
- Constitution requirement: mandatory encryption in transit
- Vercel provides automatic SSL certificates
- Required for secure authentication and data protection
- Industry standard for web applications

## Architecture Patterns

### RESTful API Design

**Decision**: Use RESTful API patterns for journal CRUD operations.

**Rationale**:
- Standard, well-understood pattern
- Easy to test and maintain
- Works well with Flask routing
- Supports future API expansion if needed

### Service Layer Pattern

**Decision**: Separate business logic into service layer (services/ directory).

**Rationale**:
- Clear separation of concerns
- Business logic independent of API routes
- Easier to test and maintain
- Supports code reuse

### Component-based Frontend (Vue.js SPA)

**Decision**: Use Vue.js Single Page Application (SPA) architecture with Vant components.

**Rationale**:
- Component-based architecture improves code reusability and maintainability
- Vant provides iOS-style components that match Human Interface Guidelines
- SPA provides smooth navigation and better user experience
- Vue.js reactive data binding simplifies state management
- Vant components handle iOS-specific interactions and styling automatically

## iOS UI/UX Considerations

### Design System: iOS Human Interface Guidelines

**Decision**: Follow iOS Human Interface Guidelines for UI design.

**Rationale**:
- Constitution requirement: iOS-first design
- Familiar interface for iPhone users
- Reduces learning curve
- Consistent with native iOS apps

**Key principles to implement**:
- SF Symbols or similar iconography
- iOS typography (San Francisco font family)
- iOS color palette and spacing
- Native iOS navigation patterns
- Touch-friendly interface elements

## Security Considerations

### Password Storage

**Decision**: Use Werkzeug's password hashing (PBKDF2) for secure password storage.

**Rationale**:
- Industry-standard password hashing
- Built into Flask ecosystem
- Protects against rainbow table attacks
- Sufficient for single-user application

### Session Security

**Decision**: Use Flask's secure session management with HTTP-only cookies.

**Rationale**:
- Prevents XSS attacks on session cookies
- Flask provides secure session handling
- Standard web security practice

### CalDAV Authentication

**Decision**: Use HTTP Basic Authentication for CalDAV endpoints.

**Rationale**:
- Standard CalDAV authentication method
- Compatible with iPhone Calendar configuration
- Simple to implement
- Secure over HTTPS

## Deployment Considerations

### Vercel Serverless Functions

**Decision**: Deploy Flask app as Vercel serverless functions.

**Rationale**:
- Vercel's recommended approach for Python apps
- Automatic scaling
- Cost-effective for low-traffic applications
- Easy deployment process

### Environment Variables

**Decision**: Store sensitive configuration in Vercel environment variables.

**Rationale**:
- Constitution requirement: no hardcoded secrets
- Secure configuration management
- Easy to update without code changes
- Vercel provides secure environment variable storage

### Database Persistence

**Decision**: Use Vercel's file system for SQLite database (with backup strategy).

**Rationale**:
- SQLite works with serverless file system
- Simple deployment model
- Consider backup strategy for data persistence
- May need to migrate to external storage if scaling

## Testing Strategy

### Unit Tests: pytest

**Decision**: Use pytest for unit and integration testing.

**Rationale**:
- Industry standard Python testing framework
- Excellent Flask integration
- Rich plugin ecosystem
- Easy to write and maintain tests

### Test Coverage

**Decision**: Target 80%+ test coverage for core functionality.

**Rationale**:
- Constitution requirement: unit tests for major features
- Ensures reliability and prevents regressions
- 80% is reasonable target for initial implementation

## Open Questions Resolved

### Q: How to handle CalDAV server implementation complexity?

**A**: Use mature library (caldav-library or Radicale) rather than custom implementation. This reduces complexity while maintaining standards compliance.

### Q: How to ensure long-term compatibility?

**A**: Use industry-standard protocols (CalDAV, HTTPS, iCalendar) that are well-established and unlikely to change. This ensures compatibility with future iOS versions and devices.

### Q: How to handle offline scenarios?

**A**: Implement sync queue mechanism. When offline, changes are queued locally and synced when connection is restored. This is handled by CalDAV protocol's built-in sync mechanisms.

### Q: How to handle calendar sync conflicts?

**A**: Implement last-write-wins strategy with conflict detection. When conflicts occur, provide user with clear options to resolve. This is a standard CalDAV conflict resolution pattern.

