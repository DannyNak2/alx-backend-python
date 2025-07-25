from rest_framework_nested.routers import NestedDefaultRouter  # ✅ keyword required
from django.urls import path, include
from .views import ConversationViewSet, MessageViewSet

# ✅ main router
router = NestedDefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversations')
router.register(r'messages', MessageViewSet, basename='messages')

urlpatterns = [
    path('', include(router.urls)),
]
