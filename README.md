# Personal Journal Web Application

A web-based personal journal management tool that allows users to create, edit, and manage journal entries with title, content, and date fields. The system provides bidirectional synchronization with iPhone Calendar via CalDAV protocol, one-click export to iPhone Notes via Shortcuts, and quick navigation to iPhone native apps.

## Features

- **Journal Management**: Create, edit, and delete journal entries with title, content, and date
- **Date-based Browsing**: Browse and view journal entries organized by date
- **Bidirectional Calendar Sync**: Sync journal entries with iPhone Calendar (web ↔ iPhone)
- **Export to Notes**: One-click export of single or multiple entries to iPhone Notes
- **Quick Access**: Jump to iPhone native apps (Calendar, Notes) from the web interface
- **iOS-First Design**: UI/UX follows iOS design patterns and Human Interface Guidelines

## Technology Stack

### Backend
- **Framework**: Flask (Python 3.11+)
- **Database**: SQLite
- **Calendar Protocol**: CalDAV (caldav-library)
- **Calendar Format**: iCalendar (ics library)
- **ORM**: Flask-SQLAlchemy
- **Authentication**: Flask-Login

### Frontend
- **Templates**: Jinja2 (Flask templates)
- **Styling**: CSS (iOS-style design)
- **Scripting**: Vanilla JavaScript (no build process)
- **Architecture**: Monolithic Flask structure (templates/ and static/ directories)

### Deployment
- **Platform**: Vercel (serverless)
- **HTTPS**: Automatic SSL/TLS encryption

## Project Structure

This is a **monolithic Flask application** where frontend assets are served directly from Flask's `static/` and `templates/` directories.

```
.
├── app.py                    # Flask application entry point
├── config.py                 # Configuration management
├── init_db.py                # Database initialization script
├── requirements.txt          # Python dependencies
├── pyproject.toml            # Python project metadata (used by Vercel)
├── runtime.txt               # Python version specification
├── vercel.json               # Vercel deployment configuration
├── templates/                # HTML templates (Jinja2)
│   ├── base.html            # Base template
│   ├── index.html           # Home page (journal list)
│   ├── login.html           # Login page
│   ├── entry_detail.html    # Entry detail/edit page
│   └── settings.html        # Settings page
├── static/                   # Static assets
│   ├── css/
│   │   └── main.css         # iOS-style stylesheet
│   ├── js/
│   │   ├── main.js          # Main JavaScript (API client, UI logic)
│   │   └── components/      # Component-specific JavaScript
│   └── images/              # Images and icons
├── models/                   # Database models
│   ├── __init__.py
│   ├── user.py              # User model
│   ├── journal_entry.py     # Journal entry model
│   └── calendar_event.py    # Calendar event model
├── services/                 # Business logic services
│   ├── journal_service.py   # Journal CRUD operations
│   ├── auth_service.py      # Authentication service
│   ├── caldav_service.py    # CalDAV sync service
│   ├── export_service.py    # Notes export service
│   ├── ics_generator.py     # iCalendar file generator
│   └── native_app_service.py # Native app URL schemes
├── api/                      # API route handlers
│   ├── __init__.py
│   ├── journal_routes.py    # Journal entry endpoints
│   ├── auth_routes.py       # Authentication endpoints
│   └── caldav_routes.py     # CalDAV sync endpoints
├── utils/                    # Utility functions
│   └── validation.py       # Input validation utilities
├── tests/                    # Test files
│   ├── unit/                # Unit tests (37 tests)
│   ├── integration/         # Integration tests (2 tests)
│   └── e2e/                 # End-to-end tests (Playwright, 7 tests)
└── specs/                   # Feature specifications and documentation
    └── 001-personal-journal-web/
```

## Setup Instructions

### Prerequisites

- Python 3.9+ (Python 3.12 recommended, with conda recommended)
- Git

**Note**: This is a monolithic Flask application. No separate frontend build process is required. Frontend assets (HTML, CSS, JavaScript) are served directly by Flask.

### Local Development Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd time-note-sync
   ```

2. **Activate conda environment** (if using conda):
   ```bash
   conda activate base
   ```

   Or create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables** (optional, defaults are provided):
   ```bash
   export FLASK_ENV=development
   export SECRET_KEY=dev-secret-key-change-in-production
   export DATABASE_URL=sqlite:///journal.db
   ```

   Or create a `.env` file:
   ```bash
   FLASK_ENV=development
   SECRET_KEY=dev-secret-key-change-in-production
   DATABASE_URL=sqlite:///journal.db
   ```

5. **Initialize the database**:
   ```bash
   python init_db.py
   ```

   This will create the database tables and optionally create a test user (username: `testuser`, password: `testpass`).

6. **Run the application**:
   ```bash
   python app.py
   ```

   The application will run on `http://localhost:5001` by default.

7. **Access the Application**:
   - Open `http://localhost:5001` in your browser
   - You will be redirected to the login page
   - Log in with your credentials (created via `init_db.py`)

## Development

### Code Quality

- **Formatting**: Black (Python) - configured in `pyproject.toml`
- **Linting**: flake8 (Python) - configured in `pyproject.toml`
- **Testing**: pytest (Python) for unit/integration tests, Playwright for E2E tests

Run code formatting:
```bash
conda activate base  # if using conda
black .
```

Run linting:
```bash
conda activate base  # if using conda
flake8 .
```

Run unit and integration tests:
```bash
conda activate base  # if using conda
pytest tests/ -v
```

Run tests with coverage:
```bash
conda activate base  # if using conda
pytest tests/ --cov=. --cov-report=html
```

Run Playwright E2E tests (local):
```bash
npx playwright test --reporter=list
```

Run Playwright E2E tests (against Vercel deployment):
```bash
VERCEL_URL=https://time-note-sync.vercel.app npx playwright test --reporter=list
```

### Test Status

- ✅ **Unit Tests**: 37/37 passing
- ✅ **Integration Tests**: 2/2 passing
- ✅ **E2E Tests**: 7/7 passing (local and Vercel deployment)

### Project Structure Details

- **Application Root**:
  - `app.py`: Flask application entry point (creates app instance for Vercel serverless)
  - `config.py`: Configuration management (development, production, testing)
  - `init_db.py`: Database initialization script

- **Models** (`models/`):
  - `user.py`: User model with authentication
  - `journal_entry.py`: Journal entry model with sync status
  - `calendar_event.py`: Calendar event model for CalDAV sync

- **Services** (`services/`):
  - `journal_service.py`: Journal CRUD operations
  - `auth_service.py`: Authentication and authorization
  - `caldav_service.py`: CalDAV bidirectional sync logic
  - `export_service.py`: Export to iPhone Notes via Shortcuts
  - `ics_generator.py`: iCalendar file generation
  - `native_app_service.py`: Native app URL scheme generation

- **API Routes** (`api/`):
  - `journal_routes.py`: Journal entry endpoints (CRUD, sync, export)
  - `auth_routes.py`: Authentication endpoints (login, logout, status)
  - `caldav_routes.py`: CalDAV sync endpoints

- **Frontend** (`templates/` and `static/`):
  - `templates/`: Jinja2 HTML templates (base, login, home, entry detail, settings)
  - `static/css/main.css`: iOS-style CSS following Human Interface Guidelines
  - `static/js/main.js`: Main JavaScript (API client, UI interactions)
  - `static/js/components/`: Component-specific JavaScript

- **Tests** (`tests/`):
  - `unit/`: Unit tests for services and utilities (37 tests)
  - `integration/`: Integration tests for API endpoints (2 tests)
  - `e2e/`: Playwright end-to-end tests (7 tests)

## Deployment

The application is configured for deployment on Vercel as a serverless Flask application. See `vercel.json` for deployment configuration.

### Current Deployment Status

- **Production URL**: https://time-note-sync.vercel.app
- **Status**: ✅ Deployed and operational
- **Region**: Hong Kong (hkg1) - optimized for users in China
- **Tests**: All tests passing (unit, integration, E2E)

### Vercel Deployment Steps

1. **Install Vercel CLI** (if not already installed):
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel**:
   ```bash
   vercel login
   ```

3. **Deploy to Production**:
   ```bash
   vercel --prod
   ```

   Or deploy to preview:
   ```bash
   vercel
   ```

4. **Set Environment Variables** in Vercel dashboard:
   - `SECRET_KEY`: A secure random string for Flask sessions (required)
   - `FLASK_ENV`: `production` (optional, defaults to production)
   - `DATABASE_URL`: Your production database URL (optional, defaults to SQLite)
   - `CALDAV_SERVER_URL`: Your CalDAV server URL (optional, for calendar sync)
   - `LOG_LEVEL`: Logging level (optional, defaults to INFO)

5. **Verify Deployment**:
   ```bash
   # Check deployment logs
   vercel inspect <deployment-url> --logs
   
   # Test health endpoint
   curl https://time-note-sync.vercel.app/health
   
   # Run E2E tests against deployment
   VERCEL_URL=https://time-note-sync.vercel.app npx playwright test
   ```

### Production Considerations

- **Database**: Currently using SQLite. For production with high traffic, consider PostgreSQL or another production-grade database
- **HTTPS**: Vercel automatically provides HTTPS/TLS encryption
- **Secret Key**: Use a strong, randomly generated secret key in production (set via environment variables)
- **Logging**: Configure appropriate log levels for production via `LOG_LEVEL` environment variable
- **CalDAV Server**: Configure CalDAV server URL in environment variables if using calendar sync
- **Dependencies**: `pyproject.toml` contains all required dependencies (Vercel uses this for Python dependency installation)
- **Python Version**: Specified in `runtime.txt` (Python 3.12) or `pyproject.toml` (`requires-python`)

### Deployment Checklist

✅ **Completed**:
- [x] All dependencies are listed in `pyproject.toml` (Vercel uses this for dependency installation)
- [x] `requirements.txt` is present and up-to-date (fallback for dependency installation)
- [x] `runtime.txt` specifies Python version (Python 3.12)
- [x] `app.py` exports app instance at module level (required for Vercel serverless)
- [x] All tests pass locally (37 unit tests, 2 integration tests, 7 E2E tests)
- [x] Build completes successfully (`vercel build`)
- [x] Health endpoint responds correctly (`/health`)
- [x] Application loads without errors
- [x] E2E tests pass against Vercel deployment

**Before deploying to production**, ensure:
- [ ] Environment variables are configured in Vercel dashboard
- [ ] Database is initialized (run `init_db.py` or configure external database)
- [ ] Secret key is set to a strong, random value

## Usage

### First-Time Setup

1. **Access the Application**:
   - Navigate to your deployed Vercel URL
   - You will be redirected to the login page

2. **Create an Account**:
   - If no users exist, you may need to create one via the database initialization script:
     ```bash
     python init_db.py
     ```
   - Or use the API to create a user (if implemented)

3. **Log In**:
   - Enter your username and password
   - You will be redirected to the home page

### Creating Journal Entries

1. Click "New Entry" button on the home page
2. Enter a title (optional - defaults to "Untitled" if empty)
3. Enter content
4. Select a date (defaults to today)
5. Click "Save"

### Browsing Entries by Date

1. Use the date picker to select a specific date
2. Navigate between dates using previous/next buttons
3. View entries for the selected date

### Calendar Sync

1. **Enable Sync**:
   - Go to Settings page
   - Enable "Auto Sync" or use manual sync
   - Configure CalDAV server URL (if required)

2. **Sync Entry**:
   - Create or edit a journal entry
   - If auto-sync is enabled, it will sync automatically
   - Or click "Sync" button to manually sync

3. **View in iPhone Calendar**:
   - Open iPhone Calendar app
   - Navigate to the entry date
   - The synced event should appear

### Export to iPhone Notes

1. **Single Entry Export**:
   - Open a journal entry
   - Click "Export to Notes" button
   - Confirm export
   - Open iPhone Notes app to view the exported note

2. **Batch Export**:
   - Select multiple entries using checkboxes
   - Click "Export Selected" button
   - All selected entries will be exported to Notes

### Quick Access to Native Apps

- **Open in Calendar**: Click "Open in Calendar" link on an entry detail page
- **Open in Notes**: Click "Open in Notes" link on an entry detail page

## Implementation Status

All planned features have been implemented and tested:

- ✅ **Phase 1**: Setup (7 tasks)
- ✅ **Phase 2**: Foundational (13 tasks)
- ✅ **Phase 3**: US1 - Create and Manage Entries (24 tasks)
- ✅ **Phase 4**: US2 - Browse by Date (8 tasks)
- ✅ **Phase 5**: US3 - Calendar Sync (30 tasks)
- ✅ **Phase 6**: US4 - Export to Notes (13 tasks)
- ✅ **Phase 7**: US5 - Native App Links (8 tasks)
- ✅ **Phase 8**: Polish & Cross-Cutting Concerns (9 tasks)

**Total**: 112/112 tasks completed

## Security & Privacy

- All data is encrypted in transit (HTTPS/TLS mandatory via Vercel)
- Owner-only access with authentication (Flask-Login)
- No third-party installations required
- Uses only native browser and iPhone system tools
- SQLite database with user isolation
- Session-based authentication with secure cookies

## Troubleshooting

### Common Issues

1. **Vercel Deployment Error**: "ModuleNotFoundError: No module named 'flask'"
   - **Solution**: Ensure `pyproject.toml` contains all dependencies in the `[project]` section

2. **500 Internal Server Error on Vercel**
   - **Solution**: Ensure `app.py` exports `app` instance at module level (not just in `if __name__ == "__main__"`)

3. **Database not initialized**
   - **Solution**: Run `python init_db.py` to create tables and test user

4. **Tests failing**
   - **Solution**: Ensure conda environment is activated: `conda activate base`

## License

See LICENSE file for details.
