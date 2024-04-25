# SharksApp

> **_NOTE:_** Removed from production middle of 2024 as the team has disbanded.

A Python web app for your friendly neighbourhood Sharks basketball team. Built using the Flask framework, this project was designed to help manage players and the team. It includes features such as web scraping, user authentication, notifications, and security measures.

## Purpose

Provide a solution to the following user problems:

1. Ensuring all team members were notified of the game details each week.
2. Confirm who was available to play.
3. Record the votes after each week for end of season MVP award, replacing Google Forms.

## Screenshots
<img width="166" alt="Screenshot 2024-04-25 at 9 51 25 AM" src="https://github.com/ljpurcell/Sharks/assets/65317064/211f8d42-5705-4ded-b396-b14827a145c4">
<img width="166" alt="Screenshot 2024-04-25 at 9 51 44 AM" src="https://github.com/ljpurcell/Sharks/assets/65317064/a1ea6677-c73d-48e3-bdb2-78f2b0cb56f2">
<img width="182" alt="Screenshot 2024-04-25 at 10 24 34 AM" src="https://github.com/ljpurcell/Sharks/assets/65317064/827a8783-6861-4da8-bb78-22051711ab80">
<img width="182" alt="Screenshot 2024-04-25 at 10 23 00 AM" src="https://github.com/ljpurcell/Sharks/assets/65317064/ddee3769-54c5-487f-be06-b0e0bb0d3310">
<img width="182" alt="Screenshot 2024-04-25 at 10 26 33 AM" src="https://github.com/ljpurcell/Sharks/assets/65317064/ab6cea79-a04b-4821-8e03-aaf3f5b2c469">


## Built using
- Python (with type annotations)
- Flask 
- Tailwind CSS
- JavaScript/TypeScript
- PostgresSQL
- Redis
- Heroku for deployment (not currently active)


## Technical features
- Webscraper to collect the game details using the `beautifulsoup` package.
- Basic user authentication and session-management through `flask_login` as well as email and mobile verification with `itsdangerous`.
- Email and SMS notifications using `flask_mail` and `twilio` respectively.
- Scheduled tasks via `APScheduler`.
- Task queue using `redis` and `rq`.
- `SQLAlchemy` and `flask_sqlaclhemy` for database ORM, which made it easy to swap from SQLite (used for prototype) to Postgres (deployment).
