from django import forms
from .models import Feedback


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['feedback_text', 'rating']
        widgets = {
            'feedback_text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Share your learning experience...'
            }),
            'rating': forms.Select(
                choices=[('', 'Select rating (optional)')] + [(i, str(i)) for i in range(1, 6)],
                attrs={'class': 'form-control'}
            ),
        }
