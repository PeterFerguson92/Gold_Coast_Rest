import uuid

from rest_framework import views, permissions, status
from rest_framework.response import Response
from .serializer import UserSerializer
from .models import User


class UserLogoutAllView(views.APIView):
    """
    Use this endpoint to log out all sessions for a given user.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        return User.objects.get(pk=pk)

    def post(self, request, *args, **kwargs):
        if 'userId' not in request.data:
            return Response("Missing user id", status=status.HTTP_400_BAD_REQUEST)
        user_id = request.data['userId'];
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response("User with id: " + user_id + " Not Found", status=status.HTTP_404_NOT_FOUND)
        user.jwt_secret = uuid.uuid4()
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserRetrieveAPIView(views.APIView):
    """
    Use this endpoint to retrieve a given user.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get(self,request,user_id,*args, **kwargs):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response("User with id: " + user_id + " Not Found", status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(instance=user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserChangeInfoAPIView(views.APIView):
    """
    Use this endpoint to update a given user.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self, pk):
        return User.objects.get(pk=pk)

    def patch(self, request, *args, **kwargs):
        if 'userId' not in request.data:
            return Response("Missing user id", status=status.HTTP_400_BAD_REQUEST)

        user_id = request.data['userId'];
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response("User with id: " + user_id + " Not Found", status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'userId': user.id
    }
