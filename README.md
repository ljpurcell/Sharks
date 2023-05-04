# SharksApp

A small and simple web app for your local Sharks basketball team.

## Purpose

Provide a solution to the following user problems:

1. Ensuring all team members were notified of the game time for each week.
2. Confirm who was available to play.
3. Record the votes after each week for end of season MVP award, replacing Google Forms.

## Built using
- Python (with type annotations)
- Flask 
- Tailwind CSS
- A smidge of TypeScript


## Technical features
- Webscraper to collect the game details using the `beautifulsoup` package.
- Basic user authentication and session-management through `flask_login` as well as email and mobile verification with `itsdangerous`.
- Email and SMS notifications using `flask_mail` and `twilio` respectively.
- Scheduled tasks via `APScheduler`.
- Task queue using `redis` and `rq`.
