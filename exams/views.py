from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.urls import reverse
from datetime import timedelta
import random
from .models import Exam, Question, ExamResult, StudentAnswer
from courses.models import Course, Enrollment
from accounts.decorators import teacher_required, student_required, teacher_or_admin_required
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


@login_required
@teacher_required
def exam_list(request):
    """
    List all exams created by the teacher
    """
    exams = Exam.objects.filter(created_by=request.user)
    return render(request, 'exams/exam_list.html', {
        'exams': exams,
        'back_url': reverse('accounts:teacher_dashboard'),
    })


@login_required
@teacher_required
def exam_create(request, course_pk):
    """
    Create a new exam for a course
    """
    course = get_object_or_404(Course, pk=course_pk, teacher=request.user)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        duration_minutes = int(request.POST.get('duration_minutes', 60))
        is_published = request.POST.get('is_published') == 'on'
        
        exam = Exam.objects.create(
            course=course,
            title=title,
            description=description,
            duration_minutes=duration_minutes,
            is_published=is_published,
            created_by=request.user
        )
        messages.success(request, f'Exam "{exam.title}" created successfully! Add questions now.')
        return redirect('exams:exam_detail', pk=exam.pk)
    
    context = {
        'course': course,
        'action': 'Create'
    }
    return render(request, 'exams/exam_form.html', context)


@login_required
@teacher_or_admin_required
def exam_detail(request, pk):
    """
    Exam detail view - shows questions and allows editing
    """
    exam = get_object_or_404(Exam, pk=pk)
    
    # Check permission
    if not (exam.created_by == request.user or request.user.profile.is_admin()):
        messages.error(request, 'You do not have permission to view this exam.')
        return redirect('accounts:dashboard')
    
    questions = exam.questions.all()
    exam.total_marks = exam.calculate_total_marks()
    exam.save()
    
    context = {
        'exam': exam,
        'questions': questions,
        'back_url': reverse('courses:course_detail', args=[exam.course.pk]),
    }
    return render(request, 'exams/exam_detail.html', context)


@login_required
@teacher_required
def exam_edit(request, pk):
    """
    Edit exam
    """
    exam = get_object_or_404(Exam, pk=pk, created_by=request.user)
    
    if request.method == 'POST':
        exam.title = request.POST.get('title')
        exam.description = request.POST.get('description')
        exam.duration_minutes = int(request.POST.get('duration_minutes', 60))
        exam.is_published = request.POST.get('is_published') == 'on'
        exam.save()
        messages.success(request, 'Exam updated successfully!')
        return redirect('exams:exam_detail', pk=exam.pk)
    
    return render(request, 'exams/exam_form.html', {'exam': exam, 'action': 'Edit'})


@login_required
@teacher_required
def exam_delete(request, pk):
    """
    Delete exam
    """
    exam = get_object_or_404(Exam, pk=pk, created_by=request.user)
    
    if request.method == 'POST':
        exam_title = exam.title
        exam.delete()
        messages.success(request, f'Exam "{exam_title}" deleted successfully!')
        return redirect('exams:exam_list')
    
    return render(request, 'exams/exam_confirm_delete.html', {'exam': exam})


@login_required
@teacher_required
def question_create(request, exam_pk):
    """
    Create a new question for an exam
    """
    exam = get_object_or_404(Exam, pk=exam_pk, created_by=request.user)
    
    if request.method == 'POST':
        question_text = request.POST.get('question_text')
        option1 = request.POST.get('option1')
        option2 = request.POST.get('option2')
        option3 = request.POST.get('option3')
        option4 = request.POST.get('option4')
        correct_answer = request.POST.get('correct_answer')
        marks = int(request.POST.get('marks', 1))
        order = int(request.POST.get('order', exam.questions.count()))
        
        Question.objects.create(
            exam=exam,
            question_text=question_text,
            option1=option1,
            option2=option2,
            option3=option3,
            option4=option4,
            correct_answer=correct_answer,
            marks=marks,
            order=order
        )
        messages.success(request, 'Question added successfully!')
        return redirect('exams:exam_detail', pk=exam.pk)
    
    return render(request, 'exams/question_form.html', {
        'exam': exam,
        'action': 'Create',
        'back_url': reverse('exams:exam_detail', args=[exam.pk]),
    })


@login_required
@teacher_required
def question_edit(request, pk):
    """
    Edit question
    """
    question = get_object_or_404(Question, pk=pk)
    
    if question.exam.created_by != request.user:
        messages.error(request, 'You do not have permission to edit this question.')
        return redirect('accounts:dashboard')
    
    if request.method == 'POST':
        question.question_text = request.POST.get('question_text')
        question.option1 = request.POST.get('option1')
        question.option2 = request.POST.get('option2')
        question.option3 = request.POST.get('option3')
        question.option4 = request.POST.get('option4')
        question.correct_answer = request.POST.get('correct_answer')
        question.marks = int(request.POST.get('marks', 1))
        question.order = int(request.POST.get('order', 0))
        question.save()
        messages.success(request, 'Question updated successfully!')
        return redirect('exams:exam_detail', pk=question.exam.pk)
    
    return render(request, 'exams/question_form.html', {
        'question': question,
        'action': 'Edit',
        'back_url': reverse('exams:exam_detail', args=[question.exam.pk]),
    })


@login_required
@teacher_required
def question_delete(request, pk):
    """
    Delete question
    """
    question = get_object_or_404(Question, pk=pk)
    
    if question.exam.created_by != request.user:
        messages.error(request, 'You do not have permission to delete this question.')
        return redirect('accounts:dashboard')
    
    exam_pk = question.exam.pk
    if request.method == 'POST':
        question.delete()
        messages.success(request, 'Question deleted successfully!')
        return redirect('exams:exam_detail', pk=exam_pk)
    
    return render(request, 'exams/question_confirm_delete.html', {'question': question})


@login_required
@student_required
def exam_start(request, pk):
    """
    Start exam - Create ExamResult and show exam questions
    """
    exam = get_object_or_404(Exam, pk=pk, is_published=True)
    course = exam.course
    
    # Backend enrollment check using Enrollment model
    if not Enrollment.objects.filter(student=request.user, course=course).exists():
        messages.error(request, 'You are not enrolled in this course.')
        return redirect('courses:course_browse')
    
    # Check if already attempted
    exam_result, created = ExamResult.objects.get_or_create(
        student=request.user,
        exam=exam,
        defaults={'total_marks': exam.calculate_total_marks()}
    )
    
    if exam_result.is_completed:
        messages.info(request, 'You have already completed this exam.')
        return redirect('exams:exam_result', pk=exam_result.pk)
    
    questions = list(Question.objects.filter(exam=exam))
    random.shuffle(questions)
    for question in questions:
        options = [
            ('1', question.option1),
            ('2', question.option2),
            ('3', question.option3),
            ('4', question.option4),
        ]
        random.shuffle(options)
        question.shuffled_options = options
    
    context = {
        'exam': exam,
        'exam_result': exam_result,
        'questions': questions,
        'duration_seconds': exam.duration_minutes * 60,
    }
    return render(request, 'exams/exam_take.html', context)


@login_required
@student_required
@require_POST
def exam_tab_switch(request, pk):
    """
    API endpoint to track tab switching violations during exam.
    Strict Policy: Immediate fail on first violation.
    """
    exam_result = get_object_or_404(ExamResult, pk=pk, student=request.user)
    
    if exam_result.is_completed:
        return JsonResponse({'error': 'Exam already submitted'}, status=400)
    
    # Proctoring Rule: First violation = Immediate failure
    exam_result.tab_switch_warnings += 1
    
    exam = exam_result.exam
    total_marks = exam.calculate_total_marks()

    # Mark as failed due to violation: score = 0, percentage = 0%
    exam_result.score = 0
    exam_result.total_marks = total_marks
    exam_result.is_completed = True
    exam_result.is_failed_due_to_violation = True
    exam_result.submitted_at = timezone.now()
    
    # Calculate time taken
    if exam_result.started_at:
        time_diff = exam_result.submitted_at - exam_result.started_at
        exam_result.time_taken_minutes = int(time_diff.total_seconds() / 60)
    
    # Also save whatever answers they had so far
    for key, value in request.POST.items():
        if key.startswith('question_'):
            try:
                question_id = int(key.split('_')[1])
                question = Question.objects.get(pk=question_id)
                student_answer, _ = StudentAnswer.objects.get_or_create(
                    exam_result=exam_result,
                    question=question
                )
                student_answer.selected_answer = value
                student_answer.check_answer()
                student_answer.save()
            except (ValueError, Question.DoesNotExist):
                continue
    
    exam_result.save()
    
    return JsonResponse({
        'violation': True,
        'auto_submitted': True,
        'redirect_url': f'/exams/result/{exam_result.pk}/'
    })


@login_required
@student_required
def exam_submit(request, pk):
    """
    Submit exam and evaluate answers
    """
    exam_result = get_object_or_404(ExamResult, pk=pk, student=request.user)
    
    if exam_result.is_completed:
        messages.info(request, 'Exam already submitted.')
        return redirect('exams:exam_result', pk=exam_result.pk)
    
    exam = exam_result.exam
    questions = exam.questions.all()
    
    # Process answers
    score = 0
    for question in questions:
        selected_answer = request.POST.get(f'question_{question.id}')
        
        student_answer, created = StudentAnswer.objects.get_or_create(
            exam_result=exam_result,
            question=question
        )
        student_answer.selected_answer = selected_answer
        student_answer.check_answer()
        student_answer.save()
        
        if student_answer.is_correct:
            score += question.marks
    
    # Update exam result
    exam_result.score = score
    exam_result.total_marks = exam.calculate_total_marks()
    exam_result.is_completed = True
    exam_result.submitted_at = timezone.now()
    
    # Calculate time taken
    if exam_result.started_at:
        time_diff = exam_result.submitted_at - exam_result.started_at
        exam_result.time_taken_minutes = int(time_diff.total_seconds() / 60)
    
    exam_result.save()
    
    messages.success(request, 'Exam submitted successfully!')
    return redirect('exams:exam_result', pk=exam_result.pk)


@login_required
@student_required
def exam_result(request, pk):
    """
    View exam result
    """
    exam_result = get_object_or_404(ExamResult, pk=pk, student=request.user)
    student_answers = exam_result.answers.select_related('question').all()
    
    context = {
        'exam_result': exam_result,
        'student_answers': student_answers,
    }
    return render(request, 'exams/exam_result.html', context)


@login_required
@student_required
def exam_results_list(request):
    """
    List all exam results for the student
    """
    exam_results = ExamResult.objects.filter(student=request.user, is_completed=True).order_by('-submitted_at')
    return render(request, 'exams/exam_results_list.html', {'exam_results': exam_results})


@login_required
@student_required
def download_result_pdf(request, result_id):
    """
    Download a completed exam result as PDF for the owner student.
    """
    result = get_object_or_404(
        ExamResult.objects.select_related('student', 'exam', 'exam__course'),
        pk=result_id,
        student=request.user,
        is_completed=True
    )

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="exam_result_{result.pk}.pdf"'

    pdf = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    pdf.setTitle('Exam Result')
    pdf.setFont('Helvetica-Bold', 22)
    pdf.drawCentredString(width / 2, height - 80, 'Exam Result')

    y = height - 140
    details = [
        f'Student Name: {result.student.get_full_name() or result.student.username}',
        f'Exam Name: {result.exam.title}',
        f'Course Name: {result.exam.course.title}',
        f'Score: {result.score}',
        f'Total Marks: {result.total_marks}',
        f'Percentage: {result.percentage}%',
        f'Date: {result.submitted_at.strftime("%d %B %Y, %I:%M %p") if result.submitted_at else "N/A"}',
    ]
    pdf.setFont('Helvetica', 13)
    for line in details:
        pdf.drawString(72, y, line)
        y -= 28

    pdf.showPage()
    pdf.save()
    return response
