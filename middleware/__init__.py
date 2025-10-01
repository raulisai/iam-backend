"""Middleware package for authentication and other middleware functions."""
from .auth_middleware import token_required

__all__ = ['token_required']
