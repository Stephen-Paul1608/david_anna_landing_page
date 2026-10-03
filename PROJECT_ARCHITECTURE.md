# Project Architecture

This project is a Django-based ministry website for David Sudher Ministries. It contains the main site pages, a blog/news section, messages, testimonies, events, and contact/invite flows.

## 1. Root Project Files

- `manage.py`  
  Django management entry point used to run the project, apply migrations, start the server, and run commands.

- `db.sqlite3`  
  SQLite database file used for local development.

- `IMPLEMENTATION_GUIDE.md`  
  Project implementation notes and instructions for building or extending the site.

- `David_Anna/`  
  Django project package containing the main settings and routing configuration.

- `about_page.md`  
  Markdown draft content for the About page that was created for content authoring before final integration into the live templates.

- `PROJECT_ARCHITECTURE.md`  
  This file. It documents the overall structure of the project.

---

## 2. Django Project Package

### `David_Anna/__init__.py`
- Empty package initializer.

### `David_Anna/settings.py`
- Core Django settings.
- Contains database config, installed apps, static/media settings, templates, ALLOWED_HOSTS, timezone, security settings, and app configuration.

### `David_Anna/urls.py`
- Main URL configuration for the project.
- Routes the project-level paths and includes the app-level URLs from the `ministry` app.

### `David_Anna/asgi.py`
- ASGI configuration for async server deployment.

### `David_Anna/wsgi.py`
- WSGI configuration for deployment servers.

---

## 3. App: `ministry`

This is the main application that powers the website content.

### `ministry/__init__.py`
- App package initializer.

### `ministry/apps.py`
- App configuration.

### `ministry/models.py`
- Core database models for site content such as:
  - articles/blog posts
  - messages
  - events
  - testimonies
  - media or related website records

### `ministry/views.py`
- Handles page rendering logic for all site views.
- Includes homepage, about, ministry, messages, blog, testimonies, contact, invite, privacy, terms, etc.

### `ministry/forms.py`
- Django forms for contact/invite/newsletter or other user inputs.

### `ministry/urls.py`
- Route definitions for all pages inside the ministry app.
- Typical routes include `/`, `/about/`, `/ministry/`, `/messages/`, `/blog/`, `/contact/`, `/invite/`, and others.

### `ministry/admin.py`
- Admin configuration for managing content through Django admin.

### `ministry/tests.py`
- App-level tests for functionality and regressions.

### `ministry/context_processors.py`
- Extra context data passed into templates globally, such as reusable site data or settings.

### `ministry/migrations/`
- Database migration files used to evolve the schema over time.
- `0001_initial.py` is the initial migration.

### `ministry/management/commands/`
- Custom Django management commands used for data seeding and maintenance.
- Examples:
  - `seed_content.py` - populates initial content
  - `clean_event_slugs.py` - cleans slug data for events

---

## 4. Templates

The project uses Django templates under `templates/ministry/`.

### Main templates
- `base.html`  
  Shared site layout, styles, scripts, nav, footer, and common page structure.

- `home.html`  
  Homepage with hero banner, ministry overview, cards, and call-to-action sections.

- `about.html`  
  About page for David Sudher's story and ministry background.

- `ministry.html`  
  Page explaining the ministry vision and mission.

- `messages.html`  
  List of messages and sermon content.

- `message_detail.html`  
  Detailed view for a single message.

- `blog.html`  
  Blog/article listing page.

- `article_detail.html`  
  Detailed blog article view.

- `testimonies.html`  
  Testimony collection page.

- `events.html`  
  Listing page for upcoming or past events.

- `event_detail.html`  
  Single event detail page.

- `contact.html`  
  Contact form and ministry contact details.

- `invite.html`  
  Invitation page for speaking or booking David.

- `media.html`  
  Media and video listing page.

- `todays_word.html`  
  Daily devotional/word page.

- `privacy.html`  
  Privacy policy page.

- `terms.html`  
  Terms and conditions page.

---

## 5. Static Files

The project stores frontend assets in `static/ministry/`.

### `static/ministry/css/`
- `main.css`  
  Main stylesheet for the entire website design, layout, sections, banners, buttons, typography, and responsive behavior.

### `static/ministry/js/`
- `main.js`  
  JavaScript for site interactions such as menu toggling, animations, or page behavior.

### `static/ministry/images/`
- Site image assets such as portraits, ministry photos, prayer shots, and banner imagery.

---

## 6. Media Files

- `media/`  
  Stores uploaded media content from the CMS/admin side for user-generated or uploaded assets.

---

## 7. Data Flow Overview

1. User requests a URL.
2. Django matches the URL in `ministry/urls.py`.
3. A view in `ministry/views.py` loads data from models.
4. The view renders a Django template from `templates/ministry/`.
5. The template uses CSS/JS assets from `static/ministry/`.
6. Images/media may come from `static/ministry/images/` or `media/`.
7. Data is persisted in SQLite locally via `db.sqlite3`.

---

## 8. Typical Site Structure Summary

- `David_Anna/` → project configuration
- `ministry/` → main business logic and content app
- `templates/ministry/` → front-end page templates
- `static/ministry/` → CSS, JS, images
- `media/` → uploaded media files
- `db.sqlite3` → local database

---

## 9. Notes

This project is a classic Django app structure with a single content-focused app (`ministry`) powering the entire site. It follows a clean separation between:

- business logic (`views.py`, `models.py`, `forms.py`)
- URL routing (`urls.py`)
- page rendering (`templates/`)
- design and frontend assets (`static/`)
- database (`db.sqlite3` / migrations)

This structure is easy to extend for additional pages, content types, or admin-managed features.
