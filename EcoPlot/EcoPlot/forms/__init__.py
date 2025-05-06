# EcoPlot/forms/__init__.py
from .auth import LoginForm, RegistrationForm
from .profile import ProfileForm

__all__ = ['LoginForm', 'RegistrationForm', 'ProfileForm', 'PasswordChangeForm']