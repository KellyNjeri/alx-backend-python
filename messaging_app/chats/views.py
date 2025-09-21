from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from .models import Conversation, Message, User
from .serializers import (
    ConversationSerializer, MessageSerializer, 
    ConversationCreateSerializer, MessageCreateSerializer
)

class ConversationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Conversation.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ConversationCreateSerializer
        return ConversationSerializer
    
    def get_queryset(self):
        # Only show conversations where the current user is a participant
        return self.queryset.filter(participants=self.request.user).prefetch_related('participants', 'messages')
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Ensure the current user is included in participants
        participant_ids = serializer.validated_data['participant_ids']
        if request.user.user_id not in participant_ids:
            participant_ids.append(str(request.user.user_id))
        
        conversation = serializer.save()
        
        # Return the created conversation with full details
        response_serializer = ConversationSerializer(conversation)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def send_message(self, request, pk=None):
        conversation = self.get_object()
        
        # Check if user is a participant in the conversation
        if not conversation.participants.filter(user_id=request.user.user_id).exists():
            return Response(
                {"error": "You are not a participant in this conversation"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = MessageCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        message = serializer.save(
            conversation=conversation,
            sender=request.user
        )
        
        response_serializer = MessageSerializer(message)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        conversation = self.get_object()
        
        # Check if user is a participant in the conversation
        if not conversation.participants.filter(user_id=request.user.user_id).exists():
            return Response(
                {"error": "You are not a participant in this conversation"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        messages = conversation.messages.all().order_by('-sent_at')
        page = self.paginate_queryset(messages)
        
        if page is not None:
            serializer = MessageSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

class MessageViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['conversation']
    ordering_fields = ['sent_at']
    ordering = ['-sent_at']
    search_fields = ['message_body']
    
    def get_queryset(self):
        # Only show messages from conversations where the user is a participant
        return Message.objects.filter(conversation__participants=self.request.user).select_related('sender', 'conversation')