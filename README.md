# Learning Tracker

A Django web app for keeping track of what I'm learning. You sign up, add
topics, mark each one *Not started*, *In progress* or *Done*, and save useful
links (tutorials, docs, videos) under each topic. The home page shows overall
progress and lets you filter topics by status.

I built it while learning Django, to practise the core pieces end to end:
models and migrations, the admin, function-based views, forms, user
accounts, template inheritance, static files and tests.

## Features

- **Accounts:** sign up, log in and log out. Each person only sees their own topics.
- **Topics:** create, view, edit and delete (with a confirmation step).
- **Resources:** add and remove links on each topic.
- **Progress:** a "3 of 5 done" summary with a progress bar.
- **Status filter:** All / Not started / In progress / Done, with counts.
- **Admin:** manage topics and resources at `/admin/`, with filters and search.
- **Design:** responsive layout, automatic dark mode, colour-coded status
  labels, visible keyboard focus and a skip-to-content link.
- **Tests:** 24 tests covering views, forms, permissions and accounts.

## Tech

- Python 3.9+
- Django 4.2 (LTS)
- SQLite (Django's default database)
- python-dotenv, to load settings from a `.env` file
- Plain HTML templates and CSS (no JavaScript, no CSS framework)

## Running it locally

```bash
# 1. Clone the repo and move into it
git clone <your-repo-url> learning_tracker
cd learning_tracker

# 2. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create your settings file, then put a real secret key in it
cp .env.example .env

# 5. Create the database tables
python manage.py migrate

# 6. (Optional) create an admin account for /admin/
python manage.py createsuperuser

# 7. Start the development server
python manage.py runserver
```

Then open http://127.0.0.1:8000/ and sign up.

## Running the tests

```bash
python manage.py test
```

The tests use a separate, temporary database, so they never touch your data.

## Project structure

```
learning_tracker/
├── learning_tracker/        # Project settings and top-level URLs
│   ├── settings.py          # Reads secrets from .env
│   └── urls.py
├── topics/                  # Main app
│   ├── models.py            # Topic and Resource
│   ├── forms.py             # TopicForm, ResourceForm
│   ├── views.py             # list, detail, create, edit, delete, resources
│   ├── urls.py
│   ├── admin.py
│   ├── tests.py
│   ├── migrations/
│   └── templates/topics/
├── accounts/                # Sign up (login/logout use Django's built-in views)
│   ├── views.py
│   ├── urls.py
│   ├── tests.py
│   └── templates/registration/
├── templates/
│   ├── base.html            # Shared layout: navbar, messages, footer
│   ├── 404.html
│   └── includes/form_fields.html
├── static/css/style.css
├── .env.example             # Template for your local .env (secrets)
├── manage.py
└── requirements.txt
```

## How a request works

Take `/topics/2/` as an example:

1. `learning_tracker/urls.py` hands the path to `topics/urls.py`.
2. `topics/urls.py` matches `topics/<int:topic_id>/` and calls `topic_detail(request, topic_id=2)`.
3. The view checks that you're logged in, then loads topic 2. It only finds
   the topic if you own it; otherwise the result is a 404.
4. `render()` fills in `topic_detail.html`, which extends `base.html`, and
   returns the finished HTML page.

## What I learned

- How a URL is matched to a view, and how a view hands data to a template
- Using `ModelForm` to validate input, and the GET-shows-form / POST-saves pattern
- Writing a data migration to fill in a new required field on existing rows
- Making sure users can only see and change their own data (`owner=request.user`)
- Keeping secrets out of git with environment variables
- Writing tests with Django's test client

## Ideas for next steps

- Deploy it (e.g. Render or PythonAnywhere)
- Notes or a learning log on each topic
- Search, and sorting by status or date
