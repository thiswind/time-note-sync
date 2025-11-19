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

```
.
├── app.py               # Flask application entry point
├── templates/           # HTML templates (Jinja2)
│   ├── base.html       # Base template
│   ├── index.html      # Home page
│   ├── login.html      # Login page
│   ├── entry_detail.html # Entry detail/edit page
│   └── settings.html   # Settings page
├── static/              # Static assets
│   ├── css/            # Stylesheets
│   ├── js/             # JavaScript files
│   └── images/         # Images and icons
├── models/              # Database models
├── services/            # Business logic services
├── api/                 # API routes
├── utils/               # Utility functions
├── tests/               # Test files
├── config.py            # Configuration
└── requirements.txt     # Python dependencies
├── tests/               # Test files
│   ├── unit/            # Unit tests
│   ├── integration/     # Integration tests
│   └── contract/        # Contract tests
└── specs/               # Feature specifications and documentation
```

## Setup Instructions

### Prerequisites

- Python 3.11+ (with conda recommended)
- Node.js 18+
- npm or yarn
- Git

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Activate conda environment (if using conda):
   ```bash
   conda activate base
   ```

   Or create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables (create `.env` file in backend directory):
   ```bash
   FLASK_APP=app.py
   FLASK_ENV=development
   SECRET_KEY=your-secret-key-here-change-in-production
   DATABASE_URL=sqlite:///journal.db
   ```

5. Initialize the database:
   ```bash
   python init_db.py
   ```

   This will create the database tables and optionally create a test user.

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start development server:
   ```bash
   npm run dev
   ```

   The frontend will run on `http://localhost:5173` (or another port if 5173 is occupied).

### Running the Application

1. **Start Backend** (in `backend/` directory):
   ```bash
   conda activate base  # if using conda
   python app.py
   ```
   Backend runs on `http://localhost:5001` by default.

2. **Start Frontend** (in `frontend/` directory):
   ```bash
   npm run dev
   ```
   Frontend runs on `http://localhost:5173` by default.

3. **Access the Application**:
   - Open `http://localhost:5173` in your browser
   - Log in with your credentials (created via `init_db.py`)

## Development

### Code Quality

- **Formatting**: Black (Python)
- **Linting**: flake8 (Python)
- **Testing**: pytest (Python)

Run code formatting:
```bash
cd backend
black .
```

Run linting:
```bash
cd backend
flake8 .
```

Run tests:
```bash
cd backend
conda activate base  # if using conda
pytest ../tests/ -v
```

Run tests with coverage:
```bash
cd backend
pytest ../tests/ --cov=. --cov-report=html
```

### Project Structure Details

- **Backend** (`backend/`):
  - `app.py`: Flask application entry point
  - `config.py`: Configuration management
  - `models/`: Database models (User, JournalEntry, CalendarEvent)
  - `services/`: Business logic services (journal, auth, caldav, export, etc.)
  - `api/`: API route handlers (journal, auth, caldav)
  - `init_db.py`: Database initialization script

- **Frontend** (`frontend/`):
  - `src/components/`: Reusable Vue components (JournalList, JournalEntry, DatePicker, CalendarSync)
  - `src/views/`: Page components (Home, EntryDetail, Settings, Login)
  - `src/services/`: API client services (api, auth, sync, native_app)
  - `src/router/`: Vue Router configuration

- **Tests** (`tests/`):
  - `unit/`: Unit tests for services and utilities
  - `integration/`: Integration tests for API endpoints and workflows

## Deployment

The application is configured for deployment on Vercel. See `vercel.json` for deployment configuration.

### Vercel Deployment Steps

1. **Install Vercel CLI** (if not already installed):
   ```bash
   npm install -g vercel
   ```

2. **Deploy to Production**:
   ```bash
   vercel --prod
   ```

   Or deploy to preview:
   ```bash
   vercel
   ```

3. **Set Environment Variables** in Vercel dashboard:
   - `SECRET_KEY`: A secure random string for Flask sessions
   - `FLASK_ENV`: `production`
   - `DATABASE_URL`: Your production database URL (if using external database)
   - `CALDAV_SERVER_URL`: Your CalDAV server URL (optional, for calendar sync)

4. **Verify Deployment**:
   - Check deployment logs: `vercel inspect <deployment-url> --logs`
   - Test health endpoint: `curl https://your-app.vercel.app/health`
   - Verify dependencies are installed correctly

### Production Considerations

- **Database**: For production, consider using PostgreSQL or another production-grade database instead of SQLite
- **HTTPS**: Vercel automatically provides HTTPS/TLS encryption
- **Secret Key**: Use a strong, randomly generated secret key in production
- **Logging**: Configure appropriate log levels for production
- **CalDAV Server**: Configure CalDAV server URL in environment variables
- **Dependencies**: Ensure `pyproject.toml` contains all required dependencies (Vercel uses this for Python dependency installation)

### Deployment Checklist

Before deploying to production, ensure:

- [ ] All dependencies are listed in `pyproject.toml` (Vercel uses this for dependency installation)
- [ ] `requirements.txt` is present and up-to-date (fallback for dependency installation)
- [ ] `runtime.txt` specifies Python version (optional, defaults to latest)
- [ ] Environment variables are configured in Vercel dashboard
- [ ] Database is initialized (run `init_db.py` or configure external database)
- [ ] All tests pass locally
- [ ] Build completes successfully (`vercel build`)
- [ ] Health endpoint responds correctly (`/health`)
- [ ] Application loads without errors

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

## Security & Privacy

- All data is encrypted in transit (HTTPS/TLS mandatory)
- Owner-only access with authentication
- No third-party installations required
- Uses only native browser and iPhone system tools

## License

See LICENSE file for details.
