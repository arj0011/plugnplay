Celery + Redis + Django + Docker (Email Campaign System) – Setup & Commands Reference

1. Setup Overview
This setup includes:

Celery: For running asynchronous tasks (e.g. sending emails).

Redis: As the message broker.

Celery Beat: For running periodic tasks (e.g. daily campaign emails).

Flower: For monitoring task execution.

Docker: To containerize Django, Celery, Redis, and Flower services.

2. Folder Structure Assumptions
Key files:

plugnplay/
├── manage.py
├── plugnplay/
│   └── settings.py
├── myapp/
│   └── tasks.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env
├── create_superuser.py

3. Build and Start the Project
    docker-compose up --build

Builds and starts all services (web, celery, redis, beat, flower)

Run this after any code or dependency changes    

4. Restart Everything Cleanly

    docker-compose down -v
    docker-compose up --build

Removes all containers and volumes

Ensures a fresh start

5. Run Django Management Commands in Web Container

    docker-compose exec web python manage.py migrate
    docker-compose exec web python manage.py createsuperuser
    docker-compose exec web python manage.py shell

Use this to perform migrations, create users, or test tasks.

6. Test Celery Task Manually
    
    docker-compose exec web python manage.py shell

Inside shell:

    from myapp.tasks import send_campaign_email
    send_campaign_email.delay()

7. Check Celery Worker Logs
    
    docker-compose logs celery

Use this to debug failed tasks, see task outputs, etc.

8. Access Flower Dashboard

    http://localhost:5555

Visual dashboard for Celery tasks

See live task status, history, failures

9. Setup Periodic Tasks with Celery Beat (via Django Admin)
Visit:
    http://localhost:8000/admin/

Then:

Create an Interval or Crontab schedule

Create a Periodic Task

Task: myapp.tasks.send_campaign_email

Set schedule

Check “enabled”

10. Check Registered Tasks
    docker-compose exec celery celery -A plugnplay inspect registered

Make sure your custom tasks (e.g., send_campaign_email) are registered.

11. Restart Celery After Adding/Changing Tasks

    docker-compose restart celery

12. Common Troubleshooting

Issue	Fix
Task not showing in Flower	Restart Celery worker
Task fails	Check logs: docker-compose logs celery
Flower not opening	Check if port 5555 is mapped in docker-compose.yml
Periodic task not running	Ensure Beat container is up and Django admin task is "enabled"
ModuleNotFoundError	Ensure all dependencies are in requirements.txt and installed

13. Optional Utilities

Check Celery Status
    docker-compose exec web celery -A plugnplay status

Restart only Flower
    docker-compose restart flower

Run a one-off shell in web container
    docker-compose run --rm web sh