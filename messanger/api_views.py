from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.db.models import Q
from minus_lviv.models import MessagesMessage
from django.contrib.auth.models import User
from .serializers import MessagesSerializer
from user.serializers import UserSerializer


class ListMessages(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        messages = MessagesMessage.objects.filter(
            Q(
                Q(recipient_id=request.user.id) |
                Q(sender_id=request.user.id)
            ) &
            Q(parent_msg_id=None)
        )
        for message in messages:
            message.recipient = UserSerializer(User.objects.get(id=message.recipient_id)).data
            message.sender = UserSerializer(User.objects.get(id=message.sender_id)).data
        serialized = MessagesSerializer(messages, many=True).data
        return Response(serialized)
