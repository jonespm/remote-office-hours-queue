from django.contrib.auth.models import User
from rest_framework import permissions
from .models import Queue, Meeting, Profile


class IsCurrentUser(permissions.BasePermission):
    '''
    Custom permission to only allow users to view themselves.
    '''

    def has_object_permission(self, request, view, obj: User):
        return obj == request.user


class IsCurrentProfile(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: Profile):
        return obj.user == request.user


def is_host(user: User, queue: Queue):
    return (
        user.is_superuser
        or user in queue.hosts.all()
    )


def is_attendee(user: User, meeting: Meeting):
    return any(
        a.user == user
        for a in meeting.attendee_set.all()
    )


class IsHostOrReadOnly(permissions.BasePermission):
    '''
    Custom permission to only allow hosts to edit queues
    '''

    def has_object_permission(self, request, view, obj: Queue):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return is_host(request.user, obj)


class IsHostOrAttendee(permissions.BasePermission):
    '''
    Custom permission to only allow meeting owners or
    hosts of the meeting's queue to edit the meeting.
    '''

    def has_object_permission(self, request, view, obj: Meeting):
        return (
            is_attendee(request.user, obj)
            or (hasattr(obj, 'queue') and is_host(request.user, obj.queue))
        )
