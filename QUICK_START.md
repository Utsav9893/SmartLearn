# Quick Start Guide

## Getting Started in 5 Minutes

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Create Admin User
```bash
python manage.py createsuperuser
```

### 4. (Optional) Create Sample Data
```bash
python manage.py create_sample_data
```

### 5. Run Server
```bash
python manage.py runserver
```

### 6. Access the Application
- Main Application: http://127.0.0.1:8000/
- Admin Panel: http://127.0.0.1:8000/admin/

## Quick Test Accounts (after running create_sample_data)

**Login as Teacher:**
- Username: `teacher1`
- Password: `password123`

**Login as Student:**
- Username: `student1`
- Password: `password123`

## What You Can Do

### As a Teacher:
1. Login → Go to "My Courses" → Create Course
2. Add lessons (upload videos/PDFs)
3. Create exams with questions
4. Publish courses and exams

### As a Student:
1. Login → Browse Courses → Enroll
2. View course lessons (watch videos/download PDFs)
3. Take exams with timer
4. View results with detailed feedback

### As Admin:
1. Login → Access Admin Panel
2. Manage all users, courses, and exams
3. View system statistics

## Common Tasks

**Create a new user:**
- Use registration page or Django admin

**Upload files:**
- Files are stored in `media/videos/` and `media/pdfs/`

**Reset database:**
```bash
# Delete db.sqlite3
python manage.py migrate
python manage.py create_sample_data
```

Happy Learning! 🚀

