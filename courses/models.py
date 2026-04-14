from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Course(models.Model):
    """
    Course model - Created by teachers, students can enroll
    """
    title = models.CharField(max_length=200)
    description = models.TextField()
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses_taught')
    students = models.ManyToManyField(User, related_name='courses_enrolled', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    # Optional: display on course detail for non-enrolled students
    duration_minutes = models.IntegerField(blank=True, null=True, help_text='Estimated duration in minutes')
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text='Course price if applicable')
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def get_student_count(self):
        """Get number of enrolled students"""
        return self.students.count()
    
    def get_lesson_count(self):
        """Get number of lessons in the course"""
        return self.lessons.count()


class Lesson(models.Model):
    """
    Lesson model - Contains videos and PDFs for a course
    """
    LESSON_TYPE_CHOICES = [
        ('video', 'Video'),
        ('pdf', 'PDF'),
        ('both', 'Both (Video + PDF)'),
    ]
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    lesson_type = models.CharField(max_length=10, choices=LESSON_TYPE_CHOICES)
    video_file = models.FileField(upload_to='videos/', blank=True, null=True)
    pdf_file = models.FileField(upload_to='pdfs/', blank=True, null=True)
    order = models.IntegerField(default=0)  # For ordering lessons
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def clean(self):
        """
        Validate file requirements based on lesson_type
        """
        if self.lesson_type == 'video' and not self.video_file:
            raise ValidationError({'video_file': 'A video file is required for Video lessons.'})
        
        if self.lesson_type == 'pdf' and not self.pdf_file:
            raise ValidationError({'pdf_file': 'A PDF file is required for PDF lessons.'})
            
        if self.lesson_type == 'both':
            if not self.video_file and not self.pdf_file:
                raise ValidationError('Both video and PDF files are required for this lesson type.')
            if not self.video_file:
                raise ValidationError({'video_file': 'A video file is required for this lesson type.'})
            if not self.pdf_file:
                raise ValidationError({'pdf_file': 'A PDF file is required for this lesson type.'})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['order', 'created_at']
        unique_together = ['course', 'order']
    
    def __str__(self):
        return f"{self.course.title} - {self.title}"


class Enrollment(models.Model):
    """
    Enrollment model to track when students enrolled in courses
    """
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        unique_together = ['student', 'course']
        ordering = ['-enrolled_at']
    
    def __str__(self):
        return f"{self.student.username} enrolled in {self.course.title}"
    
    def get_progress_percentage(self):
        """Calculate course progress percentage for the enrolled student"""
        total_lessons = self.course.lessons.count()
        total_exams = self.course.exams.filter(is_published=True).count()
        
        # total items = lessons + exams
        total_items = total_lessons + total_exams
        
        if total_items == 0:
            return 0
            
        completed_lessons = LessonCompletion.objects.filter(
            student=self.student,
            lesson__course=self.course
        ).count()
        
        from exams.models import ExamResult
        completed_exams = ExamResult.objects.filter(
            student=self.student,
            exam__course=self.course,
            is_completed=True
        ).count()
        
        completed_items = completed_lessons + completed_exams
        
        return round((completed_items / total_items) * 100, 2)


class LessonCompletion(models.Model):
    """
    LessonCompletion model - Tracks which lessons a student has completed
    """
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lesson_completions')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='completions')
    completed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['student', 'lesson']
        ordering = ['-completed_at']
    
    def __str__(self):
        return f"{self.student.username} completed {self.lesson.title}"


class Feedback(models.Model):
    """
    Student feedback for a completed course.
    One feedback is allowed per student per course.
    """
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='course_feedbacks')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='feedbacks')
    feedback_text = models.TextField()
    rating = models.PositiveSmallIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['student', 'course']
        ordering = ['-created_at']

    def clean(self):
        if self.rating is not None and not 1 <= self.rating <= 5:
            raise ValidationError({'rating': 'Rating must be between 1 and 5.'})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Feedback by {self.student.username} for {self.course.title}"
