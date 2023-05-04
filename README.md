# SharksApp

A small and simple web app for your friendly neighbourhood Sharks basketball team.

https://sharks-team-app.herokuapp.com

## Purpose

Provide a solution to the following user problems:

1. Ensuring all team members were notified of the game details each week.
2. Confirm who was available to play.
3. Record the votes after each week for end of season MVP award, replacing Google Forms.


## Screenshots


## Built using
- Python (with type annotations)
- Flask 
- Tailwind CSS
- A smidge of vanilla JavaScript compiled from TypeScript
- PostgresSQL and Redis
- Heroku for deployment


## Technical features
- Webscraper to collect the game details using the `beautifulsoup` package.
- Basic user authentication and session-management through `flask_login` as well as email and mobile verification with `itsdangerous`.
- Email and SMS notifications using `flask_mail` and `twilio` respectively.
- Scheduled tasks via `APScheduler`.
- Task queue using `redis` and `rq`.
- `SQLAlchemy` and `flask_sqlaclhemy` for database ORM, which made it easy to swap from SQLite (used for prototype) to Postgres (deployment).
