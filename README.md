# Adeyemi Rukayat · Portfolio

Personal portfolio site built with Django 6.1, plain CSS and a little vanilla JavaScript.
Projects are managed in the Django admin, and contact messages are saved to the
database with an optional email notification.

- **Stack:** Django 6.1, PostgreSQL (Neon) in production, SQLite locally, WhiteNoise, Gunicorn
- **Apps:** `portfolio` (projects, home and detail pages) and `contact` (contact form)
- **Images:** served as static files from `static/img/`; there are no user uploads

## Local setup

Requires Python 3.12+.

```bash
python3.13 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt

cp .env.example .env          # then set SECRET_KEY to any long random string
python manage.py migrate      # also seeds the two featured projects
python manage.py createcachetable
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000 and the admin at http://127.0.0.1:8000/admin/.

`.env` is read automatically. With `DEBUG=True` and no `EMAIL_HOST`, contact
notifications print to the runserver console.

### Tests

```bash
pytest
```

## Editing content

| What | Where |
| --- | --- |
| Name, role, email, GitHub and LinkedIn links | `PROFILE` in `config/settings.py` |
| Hero intro and About paragraphs | `templates/portfolio/home.html` (marked `TODO`) |
| Skills list | `SKILLS` in `portfolio/views.py` |
| Projects | Django admin → Projects |
| Headshot | replace `static/img/headshot.webp` (about 640px wide; shown as a square, cropped from just above centre) |
| Project screenshots | replace `static/img/projects/*.webp` (1600px wide, landscape; cards crop to 16:9 from the top, detail pages show the full image) |

Images are static files, so after replacing one, commit it and redeploy. For a new
project, add the image under `static/img/projects/` and enter its path
(e.g. `img/projects/my-app.webp`) in the project's **Image path** field.

## Deploying to Render + Neon

### 1. Create the database (Neon)

1. Create a project at [neon.tech](https://neon.tech).
2. Copy the **direct** connection string (not the pooled one). It looks like
   `postgresql://user:password@ep-xxxx.region.aws.neon.tech/neondb?sslmode=require`.

### 2. Create the web service (Render)

**Option A: Blueprint.** Push the repo to GitHub, then in Render choose
**New → Blueprint** and select the repo. `render.yaml` creates the service and
generates `SECRET_KEY`. You'll be asked for the values marked `sync: false`:
paste the Neon string into `DATABASE_URL`, and leave the rest blank if you don't need them.

**Option B: Manual.** Choose **New → Web Service**, connect the repo, and set:

- **Runtime:** Python (the version comes from `.python-version`)
- **Build command:** `./build.sh`
- **Start command:** `gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --access-logfile -`
- **Environment variables:** `SECRET_KEY` (long random string), `DEBUG=False`, `DATABASE_URL`

`build.sh` installs dependencies, runs `collectstatic`, applies migrations and creates
the cache table. Render's `onrender.com` hostname is added to `ALLOWED_HOSTS` and
`CSRF_TRUSTED_ORIGINS` automatically.

### 3. Create an admin user

Render's free plan has no shell, so run this from your machine against the Neon database:

```bash
DATABASE_URL='postgresql://...neon.tech/neondb?sslmode=require' python manage.py createsuperuser
```

### 4. Optional settings

| Variable | Purpose |
| --- | --- |
| `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS` | Add a custom domain (`example.com` / `https://example.com`) |
| `CONTACT_RECIPIENT_EMAIL` | Where contact notifications go |
| `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `EMAIL_USE_TLS`, `DEFAULT_FROM_EMAIL` | SMTP settings for notifications |
| `ADMIN_URL` | Move the admin away from `/admin/`, e.g. `manage-7f3k/` |
| `SECURE_HSTS_PRELOAD` | Set to `True` only once you own a custom domain and want it on the HSTS preload list |

Without email settings, contact messages are still saved and can be read in the admin.
If sending fails, the message is saved and the error is logged.

### Checking the production config

```bash
SECRET_KEY=... DEBUG=False DATABASE_URL=... python manage.py check --deploy
```

The only expected warning is `security.W021` (HSTS preload), which is off on purpose.
