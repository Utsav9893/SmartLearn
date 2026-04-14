from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from courses.models import Course


class Exam(models.Model):
    """
    Exam model - Created by teachers for a course
    """
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='exams')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    duration_minutes = models.IntegerField(validators=[MinValueValidator(1)], help_text="Duration in minutes")
    total_marks = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exams_created')
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.course.title} - {self.title}"
    
    def get_question_count(self):
        """Get number of questions in the exam"""
        return self.questions.count()
    
    def calculate_total_marks(self):
        """Calculate total marks from questions"""
        return sum(question.marks for question in self.questions.all())


class Question(models.Model):
    """
    Question model - MCQ questions for an exam
    """
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    option1 = models.CharField(max_length=500)
    option2 = models.CharField(max_length=500)
    option3 = models.CharField(max_length=500)
    option4 = models.CharField(max_length=500)
    correct_answer = models.CharField(
        max_length=1,
        choices=[('1', 'Option 1'), ('2', 'Option 2'), ('3', 'Option 3'), ('4', 'Option 4')]
    )
    marks = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    order = models.IntegerField(default=0)  # For ordering questions
    
    class Meta:
        ordering = ['order', 'id']
    
    def __str__(self):
        return f"{self.exam.title} - Question {self.order + 1}"
    
    def get_correct_option_text(self):
        """Get the text of the correct option"""
        options = {
            '1': self.option1,
            '2': self.option2,
            '3': self.option3,
            '4': self.option4,
        }
        return options.get(self.correct_answer, '')


class ExamResult(models.Model):
    """
    ExamResult model - Stores student exam results
    """
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exam_results')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='results')
    score = models.IntegerField(default=0)
    total_marks = models.IntegerField(default=0)
    percentage = models.FloatField(default=0.0)
    started_at = models.DateTimeField(auto_now_add=True)
    submitted_at = models.DateTimeField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    time_taken_minutes = models.IntegerField(default=0, help_text="Time taken in minutes")
    # Tab switching violation tracking
    tab_switch_warnings = models.IntegerField(default=0, help_text="Number of tab switch warnings")
    is_failed_due_to_violation = models.BooleanField(default=False, help_text="Failed due to tab switching violation")
    
    class Meta:
        unique_together = ['student', 'exam']
        ordering = ['-submitted_at']
    
    def __str__(self):
        return f"{self.student.username} - {self.exam.title} - {self.percentage}%"
    
    def calculate_percentage(self):
        """Calculate percentage score"""
        if self.total_marks > 0:
            return round((self.score / self.total_marks) * 100, 2)
        return 0.0
    
    def save(self, *args, **kwargs):
        """Override save to calculate percentage"""
        self.percentage = self.calculate_percentage()
        super().save(*args, **kwargs)


class StudentAnswer(models.Model):
    """
    StudentAnswer model - Stores individual answers given by students
    """
    exam_result = models.ForeignKey(ExamResult, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='student_answers')
    selected_answer = models.CharField(
        max_length=1,
        choices=[('1', 'Option 1'), ('2', 'Option 2'), ('3', 'Option 3'), ('4', 'Option 4')],
        blank=True,
        null=True
    )
    is_correct = models.BooleanField(default=False)
    marks_obtained = models.IntegerField(default=0)
    
    class Meta:
        unique_together = ['exam_result', 'question']
    
    def __str__(self):
        return f"{self.exam_result.student.username} - {self.question.id} - {self.selected_answer}"
    
    def check_answer(self):
        """Check if the selected answer is correct"""
        if self.selected_answer == self.question.correct_answer:
            self.is_correct = True
            self.marks_obtained = self.question.marks
        else:
            self.is_correct = False
            self.marks_obtained = 0
        return self.is_correct
