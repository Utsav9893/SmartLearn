# E-Learning & Online Examination System

A comprehensive Django-based web application for e-learning and online examinations with role-based access control.

## Features

### 🔐 Authentication & Authorization
- User registration and login
- Role-based access control (Student, Teacher, Admin)
- Secure password handling
- User profile management


### 📚 E-Learning Module
- **Teachers can:**
  - Create and manage courses
  - Upload videos and PDF files (stored locally)
  - Edit and delete course content
  - Publish/unpublish courses

- **Students can:**
  - Browse available courses
  - Enroll in courses
  - View enrolled courses
  - Watch videos and download PDFs
  - Track learning progress

### 📝 Exam Management Module
- **Teachers can:**
  - Create MCQ-based exams for courses
  - Set time duration
  - Add multiple questions with options and correct answers
  - Publish/unpublish exams
  - View exam statistics

- **Students can:**
  - Attempt exams with real-time timer
  - Submit exams
  - View results with detailed feedback
  - See question-wise correct/incorrect answers

- **System features:**
  - Auto-evaluation of MCQs
  - Results storage
  - Score calculation and percentage display
  - Time tracking

### 👨‍💼 Admin Module
- Manage users (students, teachers)
- Manage courses and exams
- View overall system statistics
- Full Django admin panel access

## Tech Stack

- **Backend:** Django 4.2.7 (Python)
- **Frontend:** Django Templates (HTML, CSS, Bootstrap 5)
- **Database:** SQLite (local storage)
- **Authentication:** Django built-in auth system

## Project Structure

```
Final_Year_Project/
├── accounts/              # Authentication & user management
│   ├── models.py         # UserProfile model
│   ├── views.py          # Auth views & dashboards
│   ├── urls.py           # Account URLs
│   └── decorators.py     # Role-based access decorators
├── courses/              # Course management
│   ├── models.py         # Course, Lesson, Enrollment models
│   ├── views.py          # Course CRUD operations
│   └── urls.py           # Course URLs
├── exams/                # Exam management
│   ├── models.py         # Exam, Question, ExamResult models
│   ├── views.py          # Exam CRUD & taking exams
│   └── urls.py           # Exam URLs
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   ├── accounts/         # Auth templates
│   ├── courses/          # Course templates
│   └── exams/            # Exam templates
├── media/                # Uploaded files (videos, PDFs)
├── static/               # Static files (CSS, JS)
├── elearning_project/    # Main project settings
│   ├── settings.py       # Django settings
│   └── urls.py           # Main URL configuration
└── manage.py             # Django management script
```

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone or Download the Project

Navigate to the project directory:
```bash
cd Final_Year_Project
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Run Migrations

Create the database tables:
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 5: Create Superuser (Admin)

Create an admin account to access the Django admin panel:
```bash
python manage.py createsuperuser
```
Follow the prompts to create your admin account.

### Step 6: Run the Development Server

```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## Deploy on PythonAnywhere

1. Create a Python 3.12 virtual environment and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Set environment variables in your PythonAnywhere WSGI file before loading the app:
   ```python
   import os
   os.environ['DJANGO_DEBUG'] = 'False'
   os.environ['DJANGO_SECRET_KEY'] = 'your-strong-secret-key'
   os.environ['DJANGO_ALLOWED_HOSTS'] = 'yourusername.pythonanywhere.com'
   os.environ['DJANGO_CSRF_TRUSTED_ORIGINS'] = 'https://yourusername.pythonanywhere.com'
   # Optional email configuration
   os.environ['EMAIL_HOST_USER'] = 'your-email@example.com'
   os.environ['EMAIL_HOST_PASSWORD'] = 'your-app-password'
   ```
3. In PythonAnywhere Bash console:
   ```bash
   python manage.py migrate
   python manage.py collectstatic --noinput
   ```
4. In PythonAnywhere Web tab:
   - Set static files mapping: URL `/static/` -> directory `/home/yourusername/your-project/staticfiles`
   - Set media files mapping: URL `/media/` -> directory `/home/yourusername/your-project/media`
   - Reload the web app.

## Usage Guide

### Creating Users

#### Option 1: Registration (Students & Teachers)
1. Navigate to the registration page
2. Fill in the registration form
3. Select your role (Student or Teacher)
4. Click "Register"

#### Option 2: Django Admin Panel (All Roles)
1. Login to Django admin: `http://127.0.0.1:8000/admin/`
2. Go to "Users" section
3. Add a new user
4. After creating the user, go to "User Profiles" and set the role

### For Teachers

1. **Login** with your teacher account
2. **Create a Course:**
   - Go to "My Courses" → "Create New Course"
   - Fill in course details
   - Publish the course to make it visible to students

3. **Add Lessons:**
   - Open your course
   - Click "Add Lesson"
   - Choose lesson type (Video or PDF)
   - Upload the file
   - Set the order

4. **Create an Exam:**
   - Open your course
   - Click "Create Exam"
   - Set exam details (title, duration, etc.)
   - Add questions with options and correct answers
   - Publish the exam

### For Students

1. **Login** with your student account
2. **Browse Courses:**
   - Go to "Browse Courses"
   - View available courses
   - Click "Enroll Now" on desired courses

3. **View Course Content:**
   - Go to "My Enrolled Courses"
   - Click on a course
   - View lessons (watch videos or download PDFs)

4. **Take Exams:**
   - Open an enrolled course
   - Click "Start Exam" on available exams
   - Answer all questions
   - Submit before time runs out

5. **View Results:**
   - Check "Recent Exam Results" on dashboard
   - Or go to "My Results" for all results
   - View detailed feedback on each question

### For Admins

1. **Login** with admin account
2. Access the **Django Admin Panel** at `/admin/`
3. Manage:
   - Users and their roles
   - Courses and lessons
   - Exams and questions
   - Exam results

## Sample Data

To create sample data for testing, run the management command:

```bash
python manage.py create_sample_data
```

This will create:
- 2 teachers (teacher1, teacher2) with password: `password123`
- 2 students (student1, student2) with password: `password123`
- 2 courses with lessons
- 2 exams with sample questions

**Test Accounts:**
- Teacher 1: `username=teacher1`, `password=password123`
- Teacher 2: `username=teacher2`, `password=password123`
- Student 1: `username=student1`, `password=password123`
- Student 2: `username=student2`, `password=password123`

Alternatively, you can create users manually through the registration page or Django admin panel.

## File Upload Configuration

- **Videos:** Stored in `media/videos/`
- **PDFs:** Stored in `media/pdfs/`
- Files are served in development mode automatically
- For production, configure proper media file serving

## Database Models

### UserProfile
- Extends Django User with role (student, teacher, admin)
- Additional fields: phone, address

### Course
- Fields: title, description, teacher, students (many-to-many), is_published

### Lesson
- Fields: course, title, description, lesson_type (video/pdf), video_file, pdf_file, order

### Exam
- Fields: course, title, description, duration_minutes, total_marks, is_published

### Question
- Fields: exam, question_text, option1-4, correct_answer, marks, order

### ExamResult
- Fields: student, exam, score, total_marks, percentage, submitted_at, time_taken_minutes

## Security Features

- Password hashing using Django's built-in password validators
- CSRF protection on all forms
- Role-based access control using decorators
- Login required for protected views
- File upload validation

## Troubleshooting

### Issue: Media files not displaying
**Solution:** Make sure `MEDIA_ROOT` and `MEDIA_URL` are correctly configured in `settings.py`. In development, the URLs are automatically configured.

### Issue: Permission denied errors
**Solution:** Make sure you're logged in with the correct role. Check your user profile role in the admin panel.

### Issue: Exam timer not working
**Solution:** Make sure JavaScript is enabled in your browser. The timer uses client-side JavaScript.

## Future Enhancements

- Email notifications
- Discussion forums
- Assignment submissions
- Grade reports
- Certificate generation
- Multi-language support
- Advanced analytics

## License

This project is created for educational purposes.

## Support

For issues or questions, please check the Django documentation or create an issue in the repository.

---

**Developed with Django and Bootstrap** 🚀

