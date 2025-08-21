# 🗂️ Django Trello Clone

A modular Trello-like task management system built with **Django + Django REST Framework**.  
Supports **workspaces, boards, tasks, labels, JWT authentication, reports, PostgreSQL, Docker, and Swagger docs**.

---

## 🚀 Features
- 🔑 **Authentication** with JWT (register, login, refresh token)
- 👥 **Workspaces** with member roles (Owner, Admin, Member)
- 📌 **Boards** inside each workspace
- ✅ **Tasks** with status (To Do, Doing, Done, Suspend)
- 🏷️ **Labels** for task categorization (Bug Fix, R&D, Feature, etc.)
- 📊 **Reports** (tasks by status & labels)
- 📝 **Swagger API Docs** with drf-spectacular
- 🐘 **PostgreSQL** as database
- 🐳 **Dockerized** for easy deployment
- 🧪 **Tests** with pytest

---

## 🛠️ Installation (Local)

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/trello-clone.git
   cd trello-clone

2. Create Conda environment & install dependencies:
conda create -n trello-clone python=3.11 -y
                conda activate trello-clone
            pip install -r requirements.txt

3. Create .env file:
POSTGRES_DB=trello_db
POSTGRES_USER=trello_user
POSTGRES_PASSWORD=trello_pass
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

4. Run migrations:
python manage.py makemigrations
python manage.py migrate

5. Create superuser:
python manage.py createsuperuser

6. Run server:
python manage.py runserver

#Run with Docker
1. Build & start containers:
docker-compose build
docker-compose up

2. Access:
.Django → http://localhost:8000
.Swagger Docs → http://localhost:8000/api/docs/swagger/
.Redoc Docs → http://localhost:8000/api/docs/redoc/

#Authentication
.Register: POST /api/accounts/register/
.Login: POST /api/accounts/login/
.Refresh: POST /api/accounts/refresh/

All protected endpoints require:
Authorization: Bearer <access_token>

#Reports
.Board Reports: GET /api/boards/{id}/reports/
Returns tasks grouped by status and labels.

#Running Tests
Run all tests with:
pytest -v

#Project Structure
trello_clone/
│── accounts/        # User & Auth
│── workspaces/      # Workspace & Members
│── boards/          # Boards inside workspaces
│── tasks/           # Tasks & Labels
│── config/          # Project settings
│── tests/           # Pytest test cases

#API Documentation
.Swagger UI → /api/docs/swagger/
.Redoc UI → /api/docs/redoc/

#Tech Stack
.Backend: Django, DRF
.Database: PostgreSQL
.Auth: JWT (SimpleJWT)
.Docs: drf-spectacular
.Containerization: Docker & Docker Compose
.Testing: Pytest
.Env Manager: Conda

---


