from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .models import Conversation, Message
from .serializers import (
    ConversationSerializer,
    MessageSerializer,
    ConversationCreateSerializer,
    MessageCreateSerializer,
)
from .permissions import IsParticipantOfConversation
from .pagination import MessagePagination
from .filters import MessageFilter


class ConversationViewSet(viewsets.ModelViewSet):
    """
    Handles creating conversations, listing them, and managing messages inside.
    """
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    queryset = Conversation.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'create':
            return ConversationCreateSerializer
        return ConversationSerializer

    def get_queryset(self):
        # Only return conversations where the user is a participant
        return self.queryset.filter(participants=self.request.user).prefetch_related(
            'participants', 'messages'
        )

    def create(self, request, *args, **kwargs):
        """
        Create a new conversation. Ensures the requesting user is added as a participant.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        conversation = serializer.save()
        # Always add the current user to the conversation participants
        conversation.participants.add(request.user)

        response_serializer = ConversationSerializer(conversation)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def send_message(self, request, pk=None):
        """
        Send a message in an existing conversation.
        """
        conversation = self.get_object()

        # Ensure the user is a participant
        if not conversation.participants.filter(id=request.user.id).exists():
            return Response(
                {"error": "You are not a participant in this conversation"},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = MessageCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        message = serializer.save(
            conversation=conversation,
            sender=request.user,
        )

        response_serializer = MessageSerializer(message)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        """
        List messages in a conversation.
        """
        conversation = self.get_object()

        if not conversation.participants.filter(id=request.user.id).exists():
            return Response(
                {"error": "You are not a participant in this conversation"},
                status=status.HTTP_403_FORBIDDEN,
            )

        messages = conversation.messages.all().order_by('-sent_at')
        page = self.paginate_queryset(messages)

        if page is not None:
            serializer = MessageSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)


class MessageViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only endpoint for messages.
    Users can only see messages in conversations they are part of.
    """
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    serializer_class = MessageSerializer
    pagination_class = MessagePagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = MessageFilter
    ordering_fields = ['sent_at']
    ordering = ['-sent_at']
    search_fields = ['message_body']

    def get_queryset(self):
        return Message.objects.filter(
            conversation__participants=self.request.user
        ).select_related('sender', 'conversation')
