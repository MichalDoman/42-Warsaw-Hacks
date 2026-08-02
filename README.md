# API Research Doc

To access the 42 API, create a new v2 application in the API section of the 42 intra. After saving it, 
the application page provides a unique Client ID and Client Secret, which are used to request an OAuth2 access token. 
These credentials are stored securely in environment variables and never committed to the repository.

The token is then included in each API request using the Authorization: Bearer ACCESS_TOKEN header.

### API endpoints
1. POST oauth/token:
	Using client credentials, we access the access token for the API, that is cached and reused until its expiration.
	Many requests use the same token.

2. GET /v2/campus/:campus_id/users:
	This endpoint is used to extract users data, filtered by the campus. User data is saved into python dataclasses.
	Following attributes are used: user id, login, name, wallet (altarians), intra image and inforamation about whether
	the user is active or not. For this request, two filtering parameters are used. Parameter 'kind' for filtering non students,
	and parameter 'staff?' for filtering bocal agents.

3. GET /v2/coalitions/:id:
	This end point is used for three request, one for each coalition, with corresponding coalitions ids. From this endpoint,
	we extract following data: coalition name, coalition logo url, main coalition color and total score.

4. GET /v2/coalitions/:coalition_id/coalitions_users:
	This end point provides inforamtion about scores of coalition members as well as who belongs to which coalition. Since the
	endpoint for extracting detailed user information does not tell what coalition the user is in, The data had to be mapped by user_id
	To do that we create a set of ids of all users to more efficiently iterate over it.


5. GET /v2/campus/:campus_id/locations:
	This endpoint provides students sessions on computers in the campus. This data is saved into python dataclass, and users
	following parameters: user id, location which is the station number in 42 Warsaw clusters and datetime at which a user
	logged in. This date is used to determine who was logged in today.

6. GET /v2/projects_users:
	This endpoint provides information about projects. The information consist of: user id, project name, final mark, 
	date when the project was finished if it was, status of the project, and whether it was validated. From this data we calculate
	how many projects were finished and in what period of time. Basing on this we also measure the streak for the whole campus of
	how many projects were successfully evaluated in a row.

### Data refreshing 

Data refreshes on two levels.Data from the 42 API is re-fetched no more often than once every 2 minutes within that window, 
the cached copy is shown. Automatic page reloads once every 1 hour.

There's also the "↻ Refresh" button, which triggers window.location.reload() immediately on click.
But since the backend cache lasts 2 minutes, you'll only actually get fresh data if more than 2 minutes have passed since 
the last fetch, otherwise it is the same cached copy.

### Rate-limit

The default 42 API limit is: 2 requests per second and 1,200 requests per hour.
These limits apply to the entire application, not to each endpoint.
There is impolemented a delay between consecutive requests, so that the application never exceeds two requests per second.

### Anonymous or hidden data

The dashboard follows these rules:
If a student has no visible name or login, the dashboard does not display them.
Missing profile images are replaced with a default avatar.
Private fields such as email addresses and phone numbers are never displayed.
Anonymous records may be included in aggregate statistics, such as the total number of evaluations.
Anonymous records are excluded from personal rankings, because they cannot be safely assigned to a particular student.

THIS IS THE ONLY AND LATEST VERSION OF OUR PROJECT!!!

### Error Handling

The following errors are handled:
	- imeout, when 42 API response timeout occurs.
	- HTTPError, when there is an HTTP Error. Response status code is shown.
	- RequestException, when there is an error connection to API.
	- Diffrent errors connected with invalid configuration.

Dashboard sections are updated independently where possible. to avoid partial updated crash.

# Technical solution

### What is it?

The solution is a web dashboard for 42 Warsaw. The dashboard presents following statistics:
Left column — Campus Signals:

Leading Coalition — the coalition with the most students logged in today, plus the total number of "explorers" for the day
The First Star — the first student to log in on campus today (login, avatar, time, location)
Mission Streak — the current campus-wide streak of consecutively validated projects
The First Sunray — the first student to log in after 05:30 (separate from the overall "first" login)
Rocket Fuel — combined wallet balance of all unique students who logged in today

Center column:

Projects completed this week — the 5 most recent completed/graded projects (avatar, login, project name)
Peak Orbit — the hour of the day with the highest login activity today, plus an hourly activity chart
Coalition Presence — distribution of today's active students across coalitions (Orionis, Lunaria, Uniterrax) as progress bars
Rotating Campus Leaderboard — a card that cycles through three rankings:
	Top 3 richest students (wallet)
	Coalition leaders (mock data — placeholder for the demo)
	Top evaluators (mock data — placeholder for the demo)

Right column — Orbital Intelligence:

Coalition statistics — per-coalition cards: active students, average score, top-3/top-10 scores, total coalition score
The dashboard gets data from the 42 API, processes it in Python and displays it in a browser.

### How to use it?

The user starts the application with:

```
uv run main.py
```

Then the dashboard is available in the browser at:

```text
http://localhost:5000
```

The page can refresh automatically or with a refresh button.

### JSON Dashboard data

The processed dashboard data is also available as JSON at:

```text
http://localhost:5000/api/dashboard
```

This endpoint returns the same data that is used to build the dashboard, including coalition statistics, 
recent projects, login activity and student rankings.
It can be used for testing, debugging or connecting another frontend to the application.


### Deployment target

The application can run on a computer or mini PC connected to the TV.

The device only needs:

* Python
* internet access
* access to the 42 API
* a web browser

### Display on TV

The computer is connected to the TV with HDMI.

The dashboard is opened in a browser in full-screen mode. This allows the TV to display the dashboard continuously without 
browser menus.

### Technology stack

* Python — data processing
* Flask — backend server
* Jinja — generating the web page
* HTML and CSS — dashboard layout
* JavaScript — refresh and simple animations
* Chart.js — charts
* 42 API — source of data

This stack is simple, lightweight and easy to deploy.

### Architecture and data flow

The application is divided into a few simple parts:

* **API client** — downloads data from the 42 API.
* **Python Dataclasses** — store data in a clear structure (`User`, `Location`, `Project` and `Coalition`).
* **Services** — filter the data and calculate dashboard statistics.
* **Flask backend** — sends prepared data to the dashboard and JSON API.
* **Browser** — displays the dashboard on the TV screen.

The data flow is:

```text
42 API → API client → Dataclasses → Services → Flask → TV dashboard
```

First, the application gets an access token and downloads data from the 42 API.

The raw API data is converted into dataclass objects. This makes the data easier to use and ensures 
that every object has a clear structure.

The service layer then filters and processes the data. Flask passes the final results to the dashboard, 
 which is displayed in a browser on the TV.

# What's not done

1. Updating mock data statistic with actual API data.
2. Several statistic ideas that require extra permissions for specific requests. these include:
- Evaluation number per evaluator distribution
- Top evaluators
- Who is coming back from freeze soon.
- Altarian wealth distribution

3. Connect the project with actual database.
4. Cleanify html and css files. 
5. App deployment.
6. Make the layout fully responsive for different TV resolutions.