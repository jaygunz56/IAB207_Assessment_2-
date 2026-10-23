# Triumph Motorevents

IAB207 Assignment 2, Group 30.

Triumph Motorevents is a site for finding and booking Australian motorsport events. Circuit racing,
drifting, drag racing, rally, motocross, track days and festivals are all in one place, so you don't
have to dig through club pages to find out what's on.

Live site: https://angusgillic.pythonanywhere.com

## Team

- Angus Gillic N11593636
- 
- 

## What it does

- Browse upcoming events on the home page, or filter them by category
- Keyword search, plus Smart Search, which uses sentence-transformers to find events by meaning
  (e.g. "dirt bikes" finds the motocross event even though those words aren't in it)
- Event pages with details, tickets, comments and an Acknowledgement of Country
- Register, log in and log out
- Book tickets and get a booking ID, then view past bookings under My Bookings
- Create events, and edit or cancel your own
- Events are marked Open, Sold Out, Cancelled or Inactive automatically
- A Traditional Custodians guide covering capital cities, common mistakes and research resources

## Running it locally

You'll need Python 3.10 or newer.

    pip install -r requirements.txt
    python seed.py
    python main.py

Then open http://127.0.0.1:5000

`seed.py` fills the database with sample events, bookings and comments. It only runs on an empty
database, so if you want a fresh start, delete `instance/triumph.sqlite` and run it again.

The first Smart Search downloads the AI model (about 90MB), so give it a minute. After that it's quick.

### Test accounts

| Email | Password | Notes |
| --- | --- | --- |
| demo@triumph.com | password123 | Created all the sample events |
| sarah@example.com | password123 | Has some bookings and comments |
| daniel@example.com | password123 | Has some bookings and comments |

## Secret key

The app reads its secret key from the `SECRET_KEY` environment variable. If it isn't set, a random
one is generated on startup, which is fine locally but logs everyone out whenever the app restarts.
Set it properly anywhere it's deployed.

## Deploying on PythonAnywhere

The free tier can't download from Hugging Face, so the Smart Search model has to be uploaded by hand:

1. On your own computer, save the model into the project:
   `python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2').save('models/all-MiniLM-L6-v2')"`
2. Zip the `models` folder, upload it to the project folder on PythonAnywhere and unzip it there.
3. In the WSGI file, set `SECRET_KEY` and import the app with `from triumph_motorevents import create_app`.

If the model can't load for any reason, Smart Search shows a notice and falls back to keyword search,
so the rest of the site keeps working.

`sentence-transformers` is pinned to 3.3.1 because newer versions need a newer PyTorch than
PythonAnywhere has installed.

## Project structure

    main.py                  starts the app
    seed.py                  sample data
    triumph_motorevents/
        __init__.py          app setup, login manager, error pages
        models.py            database tables
        forms.py             WTForms forms
        views.py             home page, search, Smart Search, bookings
        auth.py              register, login, logout
        events.py            event pages, create, edit, cancel, comments, booking
        ai_search.py         Smart Search ranking
        templates/           Jinja templates
        static/              CSS and images
