from rest_framework.permissions import BasePermission
from .models import Conversation, Message


class IsParticipantOfConversation(BasePermission):
    """
    Custom permission:
    - User must be authenticated
    - User must be a participant in the conversation
    """

    def has_permission(self, request, view):
        # User must be logged in
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # If checking a Conversation object
        if isinstance(obj, Conversation):
            return request.user in obj.participants.all()

        # If checking a Message object
        if isinstance(obj, Message):
            return request.user in obj.conversation.participants.all()

        return False
