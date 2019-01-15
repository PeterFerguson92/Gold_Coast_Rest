import uuid

from rest_framework import views, permissions, status
from rest_framework.response import Response
from .serializer import UserSerializer
from .models import User


class SpaUserLogoutAllView(views.APIView):
    """
    Use this endpoint to log out all sessions for a given user.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        user.jwt_secret = uuid.uuid4()
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserRetrieveUpdateAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get(self,request,userId,*args, **kwargs):
        try:
            user = User.objects.get(id=userId)
        except User.DoesNotExist:

            return Response("User with id: " + userId + " Not Found", status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(instance=user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RetrieveUserByUsernameView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request,email):
        print(email)
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:

            return Response("User with username/email: " + email + " Not Found", status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(instance=user)
        return Response(serializer.data, status=status.HTTP_200_OK)


def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'userId': user.id
    }
