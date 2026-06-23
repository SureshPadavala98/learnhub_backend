from rest_framework.permissions import BasePermission

from core.utils.choice_fields import UserRole


class IsAdmin(BasePermission):
    """
    Allows access only to Admin users.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == UserRole.ADMIN
        )


class IsStudent(BasePermission):
    """
    Allows access only to Student users.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == UserRole.STUDENT
        )


class IsMentor(BasePermission):
    """
    Allows access only to Mentor users.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == UserRole.MENTOR
        )


class IsAdminOrMentor(BasePermission):
    """
    Allows access to Admin and Mentor users.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role in [
                UserRole.ADMIN,
                UserRole.MENTOR,
            ]
        )


class IsAdminOrStudent(BasePermission):
    """
    Allows access to Admin and Student users.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role in [
                UserRole.ADMIN,
                UserRole.STUDENT,
            ]
        )


class IsVerifiedUser(BasePermission):
    """
    Allows access only to verified users.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_email_verified
        )