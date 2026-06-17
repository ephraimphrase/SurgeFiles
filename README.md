# SurgeFiles

SurgeFiles is a robust, self-hosted file management application built with Django. It provides a simple, fast, and secure way to upload, organize, and share your files from any device.

## Features

- **Folder Organization**: Group your files logically with a single-level folder structure.
- **Public File Sharing**: Generate unique, shareable URLs for files so anyone can download them without logging in. You can revoke access at any time.
- **Trash & Soft Delete**: Accidentally deleted a file? It stays in the Trash for 30 days before permanent deletion.
- **Drag & Drop Uploads**: Easily upload files using the drag-and-drop zone.
- **Smart Dashboard**: 
  - File type icons and human-readable sizes (e.g., PDF, Image, Video).
  - Advanced sorting (by Date, Name, or Size).
  - Pagination to handle hundreds of files smoothly.
  - Quick-search functionality across titles and descriptions.
- **User Profiles**: Manage your account details and password seamlessly.

## Tech Stack

- **Backend**: Django 4.2+, Python
- **Database**: SQLite (default) / PostgreSQL (production via `dj_database_url`)
- **Frontend**: Bootstrap 5.3 (CSS & JS), Bootstrap Icons

## Installation & Local Development

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd SurgeFiles
   ```

2. **Set up a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables:**
   Create a `.env` file in the root directory:
   ```env
   DEBUG=True
   ALLOWED_HOSTS=127.0.0.1,localhost
   SECRET_KEY=your-secret-key-here
   ```

5. **Run Migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Start the Development Server:**
   ```bash
   python manage.py runserver
   ```
   Visit `http://127.0.0.1:8000/` in your browser.

## Deployment

SurgeFiles is configured to be easily deployed on platforms like Railway, Render, or Heroku. It includes a `Procfile` and supports `dj_database_url` and `WhiteNoise` for static files out of the box.

- Set `DEBUG=False` in your production environment variables.
- Add your production URL to `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS`.
- `gunicorn` is configured as the WSGI server in the `Procfile`.
