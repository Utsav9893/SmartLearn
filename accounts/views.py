from django.db.models import Count, Avg, Sum, Q
from django.db.models.functions import TruncMonth
from django.utils import timezone
from datetime import timedelta
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse
from django.http import HttpResponse
from django.db import transaction
from django.core.mail import send_mail
from django.conf import settings
from .models import UserProfile
from .decorators import role_required, admin_required, teacher_required, student_required
from .utils import generate_otp, send_otp_email
from courses.models import Course, Enrollment
from exams.models import Exam, ExamResult
from .reports import (
    # student-related
    build_student_enrollment_report,
    build_course_student_list_report,
    build_student_progress_report,
    build_student_exam_report,
    # teacher-related
    build_teacher_activity_report,
    build_teacher_performance_report,
    build_course_teacher_report,
    # course-related
    build_course_enrollment_report,
    build_course_completion_report,
    build_course_revenue_report,
    # exam-related
    build_exam_result_report,
    build_exam_pass_fail_report,
    build_exam_score_stats_report,
    # platform-level
    build_platform_summary_report,
    build_monthly_growth_report,
    build_most_popular_course_report,
    build_most_active_teacher_report,
    # helper
    save_workbook_to_buffer,
)

def home(request):
    from django.db.models import Count
    courses = Course.objects.annotate(
        total_enrollments=Count('enrollments')
    ).order_by('-total_enrollments')[:3]
    return render(request, 'accounts/home.html', {'courses': courses})

def register(request):
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        role = request.POST.get('role', 'student')

        # Validation
        if password != password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'accounts/register.html', {'role': role})

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'accounts/register.html', {'role': role})

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return render(request, 'accounts/register.html', {'role': role})

        try:
            # ✅ NO atomic block needed here
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                is_active=False
            )

            # Profile setup
            profile = user.profile
            profile.role = role
            otp = generate_otp()
            profile.otp = otp
            profile.save()

            # Send OTP
            send_otp_email(email, otp)

            # Store session
            request.session['verification_user_id'] = user.id

            messages.success(request, 'OTP sent to your email. Please verify.')
            return redirect('accounts:verify_otp')

        except Exception as e:
            print("REGISTER ERROR:", e)
            messages.error(request, 'Something went wrong. Please try again.')
            return render(request, 'accounts/register.html', {'role': role})

    return render(request, 'accounts/register.html')


def verify_otp(request):
    """
    OTP verification view
    """
    user_id = request.session.get('verification_user_id')
    if not user_id:
        messages.error(request, 'Verification session expired. Please register again.')
        return redirect('accounts:register')
        
    user = User.objects.get(id=user_id)
    profile = user.profile
    
    if request.method == 'POST':
        otp_entered = request.POST.get('otp')
        
        if profile.otp == otp_entered:
            user.is_active = True
            user.save()
            profile.is_verified = True
            profile.otp = None  # Clear OTP after use
            profile.save()
            
            # Clear session
            del request.session['verification_user_id']
            
            messages.success(request, 'Account activated successfully! You can now login.')
            return redirect('accounts:login')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')
            
    return render(request, 'accounts/verify_otp.html', {'email': user.email})

def resend_otp(request):
    """
    Resend OTP view
    """
    user_id = request.session.get('verification_user_id')
    if not user_id:
        messages.error(request, 'Verification session expired. Please register again.')
        return redirect('accounts:register')
        
    user = User.objects.get(id=user_id)
    profile = user.profile
    
    otp = generate_otp()
    profile.otp = otp
    profile.save()
    
    try:
        send_otp_email(user.email, otp)
        messages.success(request, 'New OTP has been sent to your email.')
    except Exception as e:
        messages.error(request, f'Failed to send email: {str(e)}. Please try again later.')
        
    return redirect('accounts:verify_otp')


def forgot_password(request):
    """
    Simple forgot password view:
    - User enters username
    - System checks if user exists
    - System fetches user's email and sends their password
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        
        # 1. Check if username is empty
        if not username:
            messages.error(request, 'Please enter your username.')
            return render(request, 'accounts/forgot_password.html')
        
        # 2. Validate if user exists
        try:
            user = User.objects.get(username=username)
            
            # 3. Fetch user's email and send password
            email = user.email
            if not email:
                messages.error(request, 'This user does not have an email address associated.')
                return render(request, 'accounts/forgot_password.html')
            
            # Note: For production, a reset link is preferred, but user requested password for simplicity.
            # However, Django's User model stores hashed passwords, so we can't send the plain text password.
            # I will generate a random temporary password or simply reset it and send the new one.
            # But the user asked for "either the user's password OR a reset link".
            # I will use a simple "Send temporary password" approach or similar if they insisted on "password".
            # Since I can't retrieve the old password, I'll reset it to a simple random string and send that.
            
            import random
            import string
            new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
            user.set_password(new_password)
            user.save()
            
            subject = 'Your New Password - E-Learn Platform'
            message = f'Hello {user.username},\n\nYour password has been reset as requested.\nYour new temporary password is: {new_password}\n\nPlease login and change your password immediately from your profile.'
            email_from = settings.DEFAULT_FROM_EMAIL
            recipient_list = [email]
            
            send_mail(subject, message, email_from, recipient_list)
            
            messages.success(request, f'A new temporary password has been sent to your registered email: {email[:3]}***{email[email.find("@"):]}')
            return redirect('accounts:login')
            
        except User.DoesNotExist:
            messages.error(request, 'Invalid username.')
            return render(request, 'accounts/forgot_password.html')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
            return render(request, 'accounts/forgot_password.html')

    return render(request, 'accounts/forgot_password.html')

def user_login(request):
    """
    User login view
    """
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if not user.is_active:
                messages.warning(request, 'Your account is not verified yet. Please check your email for OTP.')
                # Optionally store user ID in session to allow them to go back to verification page
                request.session['verification_user_id'] = user.id
                return redirect('accounts:verify_otp')
            
            login(request, user)
            messages.success(request, f'Welcome, {user.username}!')
            return redirect('accounts:dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'accounts/login.html')


@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('accounts:login')


@login_required
def dashboard(request):
    """
    Role-based dashboard view
    Redirects to appropriate dashboard based on user role
    """
    user_role = request.user.profile.role
    
    if user_role == 'student':
        return redirect('accounts:student_dashboard')
    elif user_role == 'teacher':
        return redirect('accounts:teacher_dashboard')
    elif user_role == 'admin':
        return redirect('accounts:admin_dashboard')
    else:
        messages.error(request, 'Invalid user role.')
        return redirect('accounts:login')


@login_required
@role_required(['student'])
def student_dashboard(request):
    """
    Student dashboard
    """
    student = request.user
    enrolled_courses = Course.objects.filter(students=student)
    exam_results = ExamResult.objects.filter(student=student, is_completed=True).order_by('-submitted_at')[:5]
    
    # Calculate progress for each enrolled course
    course_progress = []
    for course in enrolled_courses:
        enrollment = Enrollment.objects.filter(student=student, course=course).first()
        if enrollment:
            progress = enrollment.get_progress_percentage()
            course_progress.append({
                'course': course,
                'progress': progress
            })
        else:
            course_progress.append({
                'course': course,
                'progress': 0
            })
    
    context = {
        'enrolled_courses': enrolled_courses,
        'recent_results': exam_results,
        'course_progress': course_progress,
    }
    return render(request, 'accounts/student_dashboard.html', context)


@login_required
@role_required(['teacher'])
def teacher_dashboard(request):
    """
    Teacher dashboard
    """
    teacher = request.user
    courses = Course.objects.filter(teacher=teacher)
    exams = Exam.objects.filter(created_by=teacher)
    total_students = User.objects.filter(profile__role='student').count()
    
    context = {
        'courses': courses,
        'exams': exams,
        'total_students': total_students,
    }
    return render(request, 'accounts/teacher_dashboard.html', context)


@login_required
@role_required(['admin'])
def admin_dashboard(request):
    """
    Admin dashboard
    """
    total_students = User.objects.filter(profile__role='student').count()
    total_teachers = User.objects.filter(profile__role='teacher').count()
    total_courses = Course.objects.count()
    total_exams = Exam.objects.count()
    total_enrollments = Enrollment.objects.count()
    
    context = {
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_courses': total_courses,
        'total_exams': total_exams,
        'total_enrollments': total_enrollments,
    }
    return render(request, 'accounts/admin_dashboard.html', context)


@login_required
@admin_required
def admin_analytics_view(request):
    """
    Provides data for admin analytics dashboard charts.
    """
    try:
        # 1. Course Enrollment Distribution (Pie Chart)
        course_enrollment_data = Course.objects.annotate(
            num_students=Count('enrollments', distinct=True)
        ).values('title', 'num_students').order_by('-num_students')
        
        course_enrollment_labels = [d['title'] for d in course_enrollment_data]
        course_enrollment_values = [d['num_students'] for d in course_enrollment_data]

        # 2. Monthly Student Registration Growth (Line Chart)
        monthly_registrations = User.objects.filter(
            profile__role='student',
            date_joined__gte=timezone.now() - timedelta(days=365) # Last 12 months
        ).annotate(month=TruncMonth('date_joined')).values('month').annotate(count=Count('id')).order_by('month')

        monthly_reg_labels = [m['month'].strftime('%Y-%m') for m in monthly_registrations]
        monthly_reg_values = [m['count'] for m in monthly_registrations]

        # 3. Course Completion Rate (Bar Chart)
        course_completion_data = []
        for course in Course.objects.all():
            total_enrolls = Enrollment.objects.filter(course=course).count()
            completed_enrolls = Enrollment.objects.filter(course=course, completed=True).count()
            
            if total_enrolls > 0:
                course_completion_data.append({
                    'course_title': course.title,
                    'completed': completed_enrolls,
                    'not_completed': total_enrolls - completed_enrolls
                })
        
        course_completion_labels = [d['course_title'] for d in course_completion_data]
        course_completion_completed = [d['completed'] for d in course_completion_data]
        course_completion_not_completed = [d['not_completed'] for d in course_completion_data]

        # 4. Pass vs Fail Ratio (Doughnut Chart)
        total_exam_results = ExamResult.objects.filter(is_completed=True).count()
        passed_exams = ExamResult.objects.filter(is_completed=True, percentage__gte=50).count() # Assuming 50% is pass mark
        failed_exams = total_exam_results - passed_exams

        pass_fail_labels = ['Passed', 'Failed']
        pass_fail_values = [passed_exams, failed_exams]

        # 5. Score Distribution (Bar Chart)
        score_ranges = {
            '0-20': 0, '21-40': 0, '41-60': 0, '61-80': 0, '81-100': 0
        }
        for result in ExamResult.objects.filter(is_completed=True):
            if 0 <= result.percentage <= 20:
                score_ranges['0-20'] += 1
            elif 21 <= result.percentage <= 40:
                score_ranges['21-40'] += 1
            elif 41 <= result.percentage <= 60:
                score_ranges['41-60'] += 1
            elif 61 <= result.percentage <= 80:
                score_ranges['61-80'] += 1
            elif 81 <= result.percentage <= 100:
                score_ranges['81-100'] += 1
        
        score_dist_labels = list(score_ranges.keys())
        score_dist_values = list(score_ranges.values())

        # 6. Teacher Performance (Horizontal Bar Chart)
        teacher_performance_data = User.objects.filter(profile__role='teacher').annotate(
            avg_score=Avg('exams_created__results__percentage')
        ).values('username', 'avg_score').order_by('-avg_score')
        
        teacher_perf_labels = [d['username'] for d in teacher_performance_data if d['avg_score'] is not None]
        teacher_perf_values = [round(d['avg_score'], 2) for d in teacher_performance_data if d['avg_score'] is not None]

        # 7. Tab Switching Activity (Bar Chart)
        tab_switch_data = ExamResult.objects.filter(tab_switch_warnings__gt=0).values('exam__title').annotate(
            total_switches=Sum('tab_switch_warnings')
        ).order_by('-total_switches')[:10] # Top 10 exams with most tab switches
        
        tab_switch_labels = [d['exam__title'] for d in tab_switch_data]
        tab_switch_values = [d['total_switches'] for d in tab_switch_data]

        # 8. Top 5 Students (Bar Chart)
        top_students_data = User.objects.filter(profile__role='student').annotate(
            avg_exam_score=Avg('exam_results__percentage')
        ).values('username', 'avg_exam_score').order_by('-avg_exam_score')[:5]
        
        top_students_labels = [d['username'] for d in top_students_data if d['avg_exam_score'] is not None]
        top_students_values = [round(d['avg_exam_score'], 2) for d in top_students_data if d['avg_exam_score'] is not None]

        # 9. Most Engaged Courses (Bar Chart) - Using average progress calculation
        engaged_courses_labels = []
        engaged_courses_values = []
        for course in Course.objects.all()[:5]: # Limit to top 5 for simplicity in manual calc
            enrolls = Enrollment.objects.filter(course=course)
            if enrolls.exists():
                avg_progress = sum(e.get_progress_percentage() for e in enrolls) / enrolls.count()
                engaged_courses_labels.append(course.title)
                engaged_courses_values.append(round(avg_progress, 2))

        # 10. Active vs Inactive Users (Pie Chart)
        total_users = User.objects.count()
        active_users = User.objects.filter(is_active=True).count()
        inactive_users = total_users - active_users

        active_inactive_labels = ['Active Users', 'Inactive Users']
        active_inactive_values = [active_users, inactive_users]

        data = {
            'course_enrollment': {'labels': course_enrollment_labels, 'values': course_enrollment_values},
            'monthly_registrations': {'labels': monthly_reg_labels, 'values': monthly_reg_values},
            'course_completion': {
                'labels': course_completion_labels,
                'completed': course_completion_completed,
                'not_completed': course_completion_not_completed
            },
            'pass_fail_ratio': {'labels': pass_fail_labels, 'values': pass_fail_values},
            'score_distribution': {'labels': score_dist_labels, 'values': score_dist_values},
            'teacher_performance': {'labels': teacher_perf_labels, 'values': teacher_perf_values},
            'tab_switching_activity': {'labels': tab_switch_labels, 'values': tab_switch_values},
            'top_students': {'labels': top_students_labels, 'values': top_students_values},
            'engaged_courses': {'labels': engaged_courses_labels, 'values': engaged_courses_values},
            'active_inactive_users': {'labels': active_inactive_labels, 'values': active_inactive_values},
        }
        
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)



@login_required
def change_password(request):
    """
    Change password view
    """
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('accounts:profile')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
            return redirect('accounts:profile')
    return redirect('accounts:profile')


@login_required
def profile(request):
    """
    User profile view
    """
    user = request.user
    profile = user.profile
    
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        profile.phone = request.POST.get('phone', '')
        profile.address = request.POST.get('address', '')
        
        user.save()
        profile.save()
        
        messages.success(request, 'Profile updated successfully!')
        return redirect('accounts:profile')
    
    role = profile.role
    if role == 'student':
        back_url = reverse('accounts:student_dashboard')
    elif role == 'teacher':
        back_url = reverse('accounts:teacher_dashboard')
    elif role == 'admin':
        back_url = reverse('accounts:admin_dashboard')
    else:
        back_url = reverse('accounts:dashboard')
    context = {
        'user': user,
        'profile': profile,
        'back_url': back_url,
    }
    return render(request, 'accounts/profile.html', context)


# --- Admin Reports (Excel downloads, admin only) ---

@login_required
@admin_required
def report_course_enrollment(request):
    """Download Course Enrollment Summary as .xlsx"""
    wb = build_course_enrollment_report()
    data = save_workbook_to_buffer(wb)
    response = HttpResponse(data, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=course_enrollment_report.xlsx'
    return response


@login_required
@admin_required
def report_teacher_activity(request):
    """Download Teacher Activity Report as .xlsx"""
    wb = build_teacher_activity_report()
    data = save_workbook_to_buffer(wb)
    response = HttpResponse(data, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=teacher_activity_report.xlsx'
    return response


@login_required
@admin_required
def report_student_exam(request):
    """Download Student Exam Report as .xlsx"""
    wb = build_student_exam_report()
    data = save_workbook_to_buffer(wb)
    response = HttpResponse(data, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=student_exam_report.xlsx'
    return response


@login_required
@admin_required
def report_platform_summary(request):
    """Download Platform Summary Report as .xlsx"""
    wb = build_platform_summary_report()
    data = save_workbook_to_buffer(wb)
    response = HttpResponse(data, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=platform_summary_report.xlsx'
    return response


# --- Additional Admin Reports ---


@login_required
@admin_required
def report_student_enrollment(request):
    wb = build_student_enrollment_report()
    data = save_workbook_to_buffer(wb)
    response = HttpResponse(
        data,
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response["Content-Disposition"] = "attachment; filename=student_enrollment_report.xlsx"
    return response


@login_required
@admin_required
def report_course_student_list(request):
    wb = build_course_student_list_report()
    data = save_workbook_to_buffer(wb)
    response = HttpResponse(
        data,
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response[
        "Content-Disposition"
    ] = "attachment; filename=course_student_list_report.xlsx"
    return response


@login_required
@admin_required
def report_student_progress(request):
    wb = build_student_progress_report()
    data = save_workbook_to_buffer(wb)
    response = HttpResponse(
        data,
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response["Content-Disposition"] = "attachment; filename=student_progress_report.xlsx"
    return response


@login_required
@admin_required
def report_teacher_performance(request):
    wb = build_teacher_performance_report()
    data = save_workbook_to_buffer(wb)
    response = HttpResponse(
        data,
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response[
        "Content-Disposition"
    ] = "attachment; filename=teacher_performance_report.xlsx"
    return response


@login_required
@admin_required
def report_course_teacher(request):
    wb = build_course_teacher_report()
    data = save_workbook_to_buffer(wb)
    response = HttpResponse(
        data,
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response[
        "Content-Disposition"
    ] = "attachment; filename=course_teacher_report.xlsx"
    return response


@login_required
@admin_required
def report_course_completion(request):
    wb = build_course_completion_report()
    data = save_workbook_to_buffer(wb)
    response = HttpResponse(
        data,
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response[
        "Content-Disposition"
    ] = "attachment; filename=course_completion_report.xlsx"
    return response


@login_required
@admin_required
def report_course_revenue(request):
    wb = build_course_revenue_report()
    data = save_workbook_to_buffer(wb)
    response = HttpResponse(
        data,
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response["Content-Disposition"] = "attachment; filename=course_revenue_report.xlsx"
    return response


@login_required
@admin_required
def report_exam_results(request):
    wb = build_exam_result_report()
    data = save_workbook_to_buffer(wb)
    response = HttpResponse(
        data,
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response["Content-Disposition"] = "attachment; filename=exam_result_report.xlsx"
    return response


@login_required
@admin_required
def report_exam_pass_fail(request):
    wb = build_exam_pass_fail_report()
    data = save_workbook_to_buffer(wb)
    response = HttpResponse(
        data,
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response["Content-Disposition"] = "attachment; filename=exam_pass_fail_report.xlsx"
    return response


@login_required
@admin_required
def report_exam_score_stats(request):
    wb = build_exam_score_stats_report()
    data = save_workbook_to_buffer(wb)
    response = HttpResponse(
        data,
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response[
        "Content-Disposition"
    ] = "attachment; filename=exam_score_statistics_report.xlsx"
    return response


@login_required
@admin_required
def report_monthly_growth(request):
    wb = build_monthly_growth_report()
    data = save_workbook_to_buffer(wb)
    response = HttpResponse(
        data,
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response["Content-Disposition"] = "attachment; filename=monthly_growth_report.xlsx"
    return response


@login_required
@admin_required
def report_most_popular_course(request):
    wb = build_most_popular_course_report()
    data = save_workbook_to_buffer(wb)
    response = HttpResponse(
        data,
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response[
        "Content-Disposition"
    ] = "attachment; filename=most_popular_course_report.xlsx"
    return response


@login_required
@admin_required
def report_most_active_teacher(request):
    wb = build_most_active_teacher_report()
    data = save_workbook_to_buffer(wb)
    response = HttpResponse(
        data,
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response[
        "Content-Disposition"
    ] = "attachment; filename=most_active_teacher_report.xlsx"
    return response
