# Task Management Application

A simple task management application where users can create and manage multiple Work Boards. Each Work Board functions like a Kanban board with tasks that have statuses (ToDo, In Progress, Completed), and users can drag and drop tasks between statuses while assigning them to specific users.

## Table of Contents

- [Project Setup](#project-setup)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Running Tests](#running-tests)
- [Contributing](#contributing)
- [License](#license)

## Project Setup

Follow these steps to set up the project on your local machine.

### Requirements

- Python 3.x
- Django 4.x
- Django REST Framework
- PostgreSQL
- Redis
- Django Decouple

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/NityanandaBehera/Blooprint.git
   cd blooprint
2.**Activate the virtual environment:**  
 ```bash
python -m venv blooprint
cd blooprint
cd scripts
activate
cd ..
cd ..
```
3.**Install the required packages:**
```bash
pip install -r requirements.txt
```
4.**Set up your PostgreSQL database:**
#Create a new database in PostgreSQL.
#Update the .env file in the project root with your database credentials:
`DB_NAME=my_database_name
DB_USER=my_db_user
DB_PASSWORD=my_secure_password
DB_HOST=localhost
DB_PORT=5432
`
5.**Run migrations to set up the database:**
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```






