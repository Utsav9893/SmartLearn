import random
from django.core.mail import send_mail
from django.conf import settings

def generate_otp():
    """Generate a 6-digit numeric OTP"""
    return str(random.randint(100000, 999999))

def send_otp_email(email, otp):
    """Send OTP to user email"""
    subject = 'OTP Verification'
    message = f'Your OTP for registration is: {otp}. It is valid for a limited time.'
    email_from = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
