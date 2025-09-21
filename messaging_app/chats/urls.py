from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConversationViewSet, MessageViewSet

# Create a router and register our viewsets
router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

# This demonstrates the DefaultRouter usage explicitly
urlpatterns = [
    path('', include(router.urls)),
]

# urlpatterns = router.urls