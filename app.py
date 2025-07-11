"""from flask import Flask, render_template, request
import calendar

app = Flask(__name__)

def is_leap(year):
    return calendar.isleap(year)

def get_first_day(year):
    return calendar.weekday(year, 1, 1)

def find_matching_calendars(target_year):
    target_leap = is_leap(target_year)
    target_first_day = get_first_day(target_year)
    matches = []

    for y in range(1900, 2101):
        if y == target_year:
            continue
        if is_leap(y) == target_leap and get_first_day(y) == target_first_day:
            matches.append(y)

    return matches

@app.route('/', methods=['GET', 'POST'])
def index():
    matches = []
    year = None
    if request.method == 'POST':
        try:
            year = int(request.form['year'])
            matches = find_matching_calendars(year)
        except ValueError:
            matches = ['Invalid input! Please enter a valid year.']

    return render_template('index.html', matches=matches, year=year)

if __name__ == '__main__':
    app.run(debug=True)"""

from flask import Flask, render_template, request
import calendar
import wikipediaapi

def get_wikipedia_events(year):
    wiki = wikipediaapi.Wikipedia(
        language='en',
        user_agent='calendar-matcher/1.0 (your-email@example.com)'
    )

    # Try these in order
    page_titles = [
        f"{year}_in_natural_disasters",
        f"{year}_disasters",
        f"{year}_in_disasters",
        f"{year}_in_science",
        f"{year}_in_the_environment"
    ]

    for title in page_titles:
        page = wiki.page(title)
        if page.exists():
            return f"**{title.replace('_', ' ')}**\n\n{page.summary[:1000]}"

    return f"No disaster page found for {year}"

app = Flask(__name__)

def is_leap(year):
    return calendar.isleap(year)

def get_first_day(year):
    return calendar.weekday(year, 1, 1)

def find_matching_calendars(target_year):
    target_leap = is_leap(target_year)
    target_first_day = get_first_day(target_year)
    matches = []

    for y in range(1900, 2101):
        if y == target_year:
            continue
        if is_leap(y) == target_leap and get_first_day(y) == target_first_day:
            matches.append(y)

    return matches

def generate_year_calendar(year):
    cal = calendar.TextCalendar(calendar.SUNDAY)
    return cal.formatyear(year, 2, 1, 1, 3).replace('\n', '<br>')  # formatted for HTML

@app.route('/', methods=['GET', 'POST'])
def index():
    matches = []
    year = None
    if request.method == 'POST':
        try:
            year = int(request.form['year'])
            matches = find_matching_calendars(year)
        except:
            matches = ['Invalid year']
    return render_template('index.html', matches=matches, year=year)

@app.route('/compare', methods=['POST'])
def compare():
    selected_years = request.form.getlist('selected_years')
    if len(selected_years) < 2:
        return "Please select at least 2 or more years."

    year_cals = {}
    disaster_summary = {}

    for y in selected_years:
        y_int = int(y)
        year_cals[y_int] = generate_year_calendar(y_int)
        disaster_summary[y_int] = get_wikipedia_events(y_int)

    return render_template(
        'compare.html',
        calendars=year_cals,
        disaster_summary=disaster_summary
    )

if __name__ == '__main__':
    app.run(debug=True)

