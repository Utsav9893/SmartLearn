from django.contrib.auth.models import User
from accounts.models import UserProfile
from courses.models import Course, Lesson
from exams.models import Exam, Question

# ---------- 1. Create Teacher Accounts ----------

# Teacher 1: Sarah Johnson
teacher1, created = User.objects.get_or_create(
    username='sarah_johnson',
    defaults={
        'email': 'sarah.johnson@elearning.com',
        'first_name': 'Sarah',
        'last_name': 'Johnson',
    },
)
if created:
    teacher1.set_password('Teacher@123')  # hashed properly
    teacher1.save()
    teacher1.profile.role = 'teacher'
    teacher1.profile.save()

# Teacher 2: Michael Chen
teacher2, created = User.objects.get_or_create(
    username='michael_chen',
    defaults={
        'email': 'michael.chen@elearning.com',
        'first_name': 'Michael',
        'last_name': 'Chen',
    },
)
if created:
    teacher2.set_password('Teacher@123')
    teacher2.save()
    teacher2.profile.role = 'teacher'
    teacher2.profile.save()

print("Teachers ready:")
print(" - sarah_johnson / Teacher@123")
print(" - michael_chen / Teacher@123")

# ---------- 2. Define Course Data ----------

courses_teacher1_data = [
    {
        "title": "Python Programming Fundamentals",
        "description": (
            "Comprehensive introduction to Python programming. Covers variables, "
            "data types, control flow, functions, modules, file handling, and an "
            "introduction to object-oriented programming. Ideal for beginners."
        ),
        "duration_minutes": 30 * 60,
        "price": 2999.00,
    },
    {
        "title": "Web Development with HTML, CSS & JavaScript",
        "description": (
            "Learn to build responsive, modern websites using HTML5, CSS3, and "
            "JavaScript. Includes DOM manipulation, events, forms, and basic "
            "front-end best practices."
        ),
        "duration_minutes": 40 * 60,
        "price": 3499.00,
    },
    {
        "title": "Django Web Framework Development",
        "description": (
            "Build full-stack web applications using Django. Covers models, views, "
            "templates, forms, authentication, static/media files, and deployment basics."
        ),
        "duration_minutes": 50 * 60,
        "price": 4499.00,
    },
]

courses_teacher2_data = [
    {
        "title": "Data Structures and Algorithms",
        "description": (
            "Covers core data structures (arrays, linked lists, stacks, queues, "
            "trees, graphs) and algorithms (sorting, searching, recursion, dynamic "
            "programming). Focus on problem solving and interview preparation."
        ),
        "duration_minutes": 60 * 60,
        "price": 3999.00,
    },
    {
        "title": "Database Management with MySQL",
        "description": (
            "Learn relational database design, SQL queries, joins, indexes, "
            "constraints, normalization, and transactions using MySQL."
        ),
        "duration_minutes": 30 * 60,
        "price": 2999.00,
    },
    {
        "title": "Cyber Security Basics",
        "description": (
            "Introduction to cyber security concepts: threats, vulnerabilities, "
            "encryption basics, network security, authentication, and best practices."
        ),
        "duration_minutes": 40 * 60,
        "price": 3799.00,
    },
]

# ---------- 3. Create Courses ----------

teacher1_courses = []
for data in courses_teacher1_data:
    course, _ = Course.objects.get_or_create(
        title=data["title"],
        teacher=teacher1,
        defaults={
            "description": data["description"],
            "duration_minutes": data["duration_minutes"],
            "price": data["price"],
            "is_published": True,
        },
    )
    teacher1_courses.append(course)

teacher2_courses = []
for data in courses_teacher2_data:
    course, _ = Course.objects.get_or_create(
        title=data["title"],
        teacher=teacher2,
        defaults={
            "description": data["description"],
            "duration_minutes": data["duration_minutes"],
            "price": data["price"],
            "is_published": True,
        },
    )
    teacher2_courses.append(course)

print(f"Created/ensured {len(teacher1_courses)} courses for Sarah Johnson")
print(f"Created/ensured {len(teacher2_courses)} courses for Michael Chen")

# ---------- 4. Create Lessons for Each Course ----------

def create_lessons_for_course(course, base_topic):
    """
    Creates 3 simple lessons per course:
      1. Introduction
      2. Core Concepts
      3. Hands-on Practice
    """
    Lesson.objects.get_or_create(
        course=course,
        order=1,
        defaults={
            "title": f"{base_topic} - Introduction",
            "description": f"Introduction to {base_topic}, course structure, prerequisites, and learning outcomes.",
            "lesson_type": "video",
        },
    )
    Lesson.objects.get_or_create(
        course=course,
        order=2,
        defaults={
            "title": f"{base_topic} - Core Concepts",
            "description": f"Detailed explanation of the core concepts of {base_topic} with examples.",
            "lesson_type": "pdf",
        },
    )
    Lesson.objects.get_or_create(
        course=course,
        order=3,
        defaults={
            "title": f"{base_topic} - Hands-on Practice",
            "description": f"Practical exercises and mini-projects to apply {base_topic} concepts.",
            "lesson_type": "video",
        },
    )

for c in teacher1_courses + teacher2_courses:
    create_lessons_for_course(c, c.title)

print("Lessons created for all courses.")

# ---------- 5. Exam Questions Data ----------

exam_questions = {
    "Python Programming Fundamentals": [
        {
            "question_text": "Which of the following is the correct way to declare a variable in Python?",
            "option1": "var x = 5",
            "option2": "x = 5",
            "option3": "int x = 5",
            "option4": "x := 5",
            "correct_answer": "2",
            "marks": 2,
        },
        {
            "question_text": "Which keyword is used to define a function in Python?",
            "option1": "function",
            "option2": "def",
            "option3": "func",
            "option4": "define",
            "correct_answer": "2",
            "marks": 2,
        },
    ],
    "Web Development with HTML, CSS & JavaScript": [
        {
            "question_text": "What does HTML stand for?",
            "option1": "HyperText Markup Language",
            "option2": "High-Level Text Markup Language",
            "option3": "Hyperlink and Text Markup Language",
            "option4": "Home Tool Markup Language",
            "correct_answer": "1",
            "marks": 2,
        },
        {
            "question_text": "Which CSS property changes the text color?",
            "option1": "font-color",
            "option2": "text-color",
            "option3": "color",
            "option4": "text-style",
            "correct_answer": "3",
            "marks": 2,
        },
    ],
    "Django Web Framework Development": [
        {
            "question_text": "What does MVT stand for in Django?",
            "option1": "Model-View-Template",
            "option2": "Model-View-Controller",
            "option3": "Multiple-View-Template",
            "option4": "Model-Variable-Template",
            "correct_answer": "1",
            "marks": 3,
        },
    ],
    "Data Structures and Algorithms": [
        {
            "question_text": "What is the time complexity of binary search?",
            "option1": "O(n)",
            "option2": "O(log n)",
            "option3": "O(n log n)",
            "option4": "O(1)",
            "correct_answer": "2",
            "marks": 3,
        },
    ],
    "Database Management with MySQL": [
        {
            "question_text": "What does SQL stand for?",
            "option1": "Structured Query Language",
            "option2": "Simple Query Language",
            "option3": "Standard Query Language",
            "option4": "Sequential Query Language",
            "correct_answer": "1",
            "marks": 2,
        },
    ],
    "Cyber Security Basics": [
        {
            "question_text": "What is a common secure method to store passwords?",
            "option1": "Storing in plain text",
            "option2": "Hashing with a salt",
            "option3": "Writing in a text file",
            "option4": "Sending by email",
            "correct_answer": "2",
            "marks": 3,
        },
    ],
}

# ---------- 6. Create Exams (1 per Course) with Questions ----------

def create_exam_for_course(course, creator):
    exam_title = f"{course.title} - Assessment"
    exam, _ = Exam.objects.get_or_create(
        title=exam_title,
        course=course,
        defaults={
            "description": f"Assessment exam for {course.title}",
            "duration_minutes": 60,
            "created_by": creator,
            "is_published": True,
        },
    )
    if exam.questions.exists():
        return exam  # already has questions

    q_data_list = exam_questions.get(course.title, [])
    for idx, q in enumerate(q_data_list):
        Question.objects.create(
            exam=exam,
            question_text=q["question_text"],
            option1=q["option1"],
            option2=q["option2"],
            option3=q["option3"],
            option4=q["option4"],
            correct_answer=q["correct_answer"],
            marks=q["marks"],
            order=idx,
        )
    exam.total_marks = exam.calculate_total_marks()
    exam.save()
    return exam

for c in teacher1_courses:
    create_exam_for_course(c, teacher1)

for c in teacher2_courses:
    create_exam_for_course(c, teacher2)

print("Exams with questions created for all courses.")
print("DONE.")