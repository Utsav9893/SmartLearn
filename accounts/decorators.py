from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def role_required(allowed_roles):
    """
    Decorator to restrict access based on user role
    Usage: @role_required(['teacher', 'admin'])
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.error(request, 'Please login to access this page.')
                return redirect('accounts:login')
            
            # Check if user has a profile
            if not hasattr(request.user, 'profile'):
                messages.error(request, 'User profile not found.')
                return redirect('accounts:login')
            
            # Check if user role is in allowed roles
            user_role = request.user.profile.role
            if user_role not in allowed_roles:
                messages.error(request, 'You do not have permission to access this page.')
                return redirect('accounts:dashboard')
            
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


# Specific decorators for each role
def student_required(view_func):
    """Decorator to restrict access to students only"""
    return role_required(['student'])(view_func)


def teacher_required(view_func):
    """Decorator to restrict access to teachers only"""
    return role_required(['teacher'])(view_func)


def admin_required(view_func):
    """Decorator to restrict access to admins only"""
    return role_required(['admin'])(view_func)


def teacher_or_admin_required(view_func):
    """Decorator to restrict access to teachers and admins"""
    return role_required(['teacher', 'admin'])(view_func)

