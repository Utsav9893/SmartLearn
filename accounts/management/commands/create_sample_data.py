"""
Django management command to create sample data for testing
Usage: python manage.py create_sample_data
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import UserProfile
from courses.models import Course, Lesson
from exams.models import Exam, Question


class Command(BaseCommand):
    help = 'Creates sample data for testing (teachers, students, courses, exams)'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creating sample data...'))

        # Create teachers
        teacher1, created = User.objects.get_or_create(
            username='teacher1',
            defaults={
                'email': 'teacher1@example.com',
                'first_name': 'John',
                'last_name': 'Teacher'
            }
        )
        if created:
            teacher1.set_password('password123')
            teacher1.save()
            teacher1.profile.role = 'teacher'
            teacher1.profile.save()
            self.stdout.write(self.style.SUCCESS(f'Created teacher: {teacher1.username}'))

        teacher2, created = User.objects.get_or_create(
            username='teacher2',
            defaults={
                'email': 'teacher2@example.com',
                'first_name': 'Jane',
                'last_name': 'Instructor'
            }
        )
        if created:
            teacher2.set_password('password123')
            teacher2.save()
            teacher2.profile.role = 'teacher'
            teacher2.profile.save()
            self.stdout.write(self.style.SUCCESS(f'Created teacher: {teacher2.username}'))

        # Create students
        student1, created = User.objects.get_or_create(
            username='student1',
            defaults={
                'email': 'student1@example.com',
                'first_name': 'Alice',
                'last_name': 'Student'
            }
        )
        if created:
            student1.set_password('password123')
            student1.save()
            student1.profile.role = 'student'
            student1.profile.save()
            self.stdout.write(self.style.SUCCESS(f'Created student: {student1.username}'))

        student2, created = User.objects.get_or_create(
            username='student2',
            defaults={
                'email': 'student2@example.com',
                'first_name': 'Bob',
                'last_name': 'Learner'
            }
        )
        if created:
            student2.set_password('password123')
            student2.save()
            student2.profile.role = 'student'
            student2.profile.save()
            self.stdout.write(self.style.SUCCESS(f'Created student: {student2.username}'))

        # Create courses
        course1, created = Course.objects.get_or_create(
            title='Python Programming Basics',
            defaults={
                'description': 'Learn Python programming from scratch. This course covers variables, loops, functions, and object-oriented programming.',
                'teacher': teacher1,
                'is_published': True
            }
        )
        if created:
            course1.students.add(student1, student2)
            self.stdout.write(self.style.SUCCESS(f'Created course: {course1.title}'))

        course2, created = Course.objects.get_or_create(
            title='Web Development with Django',
            defaults={
                'description': 'Build web applications using Django framework. Learn about models, views, templates, and deployment.',
                'teacher': teacher2,
                'is_published': True
            }
        )
        if created:
            course2.students.add(student1)
            self.stdout.write(self.style.SUCCESS(f'Created course: {course2.title}'))

        # Create exams
        exam1, created = Exam.objects.get_or_create(
            title='Python Basics Quiz',
            defaults={
                'course': course1,
                'description': 'Test your knowledge of Python basics',
                'duration_minutes': 30,
                'created_by': teacher1,
                'is_published': True
            }
        )
        if created:
            # Add questions to exam1
            Question.objects.get_or_create(
                exam=exam1,
                question_text='What is the correct way to declare a variable in Python?',
                defaults={
                    'option1': 'var x = 5',
                    'option2': 'x = 5',
                    'option3': 'int x = 5',
                    'option4': 'x := 5',
                    'correct_answer': '2',
                    'marks': 1,
                    'order': 0
                }
            )
            Question.objects.get_or_create(
                exam=exam1,
                question_text='Which keyword is used to define a function in Python?',
                defaults={
                    'option1': 'function',
                    'option2': 'def',
                    'option3': 'func',
                    'option4': 'define',
                    'correct_answer': '2',
                    'marks': 1,
                    'order': 1
                }
            )
            Question.objects.get_or_create(
                exam=exam1,
                question_text='What is the output of: print(2 ** 3)?',
                defaults={
                    'option1': '6',
                    'option2': '8',
                    'option3': '9',
                    'option4': '5',
                    'correct_answer': '2',
                    'marks': 1,
                    'order': 2
                }
            )
            exam1.total_marks = exam1.calculate_total_marks()
            exam1.save()
            self.stdout.write(self.style.SUCCESS(f'Created exam: {exam1.title} with 3 questions'))

        exam2, created = Exam.objects.get_or_create(
            title='Django Fundamentals Test',
            defaults={
                'course': course2,
                'description': 'Assessment on Django basics',
                'duration_minutes': 45,
                'created_by': teacher2,
                'is_published': True
            }
        )
        if created:
            Question.objects.get_or_create(
                exam=exam2,
                question_text='What does MVT stand for in Django?',
                defaults={
                    'option1': 'Model-View-Template',
                    'option2': 'Model-View-Controller',
                    'option3': 'Multiple-View-Template',
                    'option4': 'Model-Variable-Template',
                    'correct_answer': '1',
                    'marks': 2,
                    'order': 0
                }
            )
            exam2.total_marks = exam2.calculate_total_marks()
            exam2.save()
            self.stdout.write(self.style.SUCCESS(f'Created exam: {exam2.title} with 1 question'))

        self.stdout.write(self.style.SUCCESS('\nSample data created successfully!'))
        self.stdout.write(self.style.SUCCESS('\nTest Accounts:'))
        self.stdout.write(self.style.SUCCESS('Teacher 1: username=teacher1, password=password123'))
        self.stdout.write(self.style.SUCCESS('Teacher 2: username=teacher2, password=password123'))
        self.stdout.write(self.style.SUCCESS('Student 1: username=student1, password=password123'))
        self.stdout.write(self.style.SUCCESS('Student 2: username=student2, password=password123'))

