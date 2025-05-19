from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Note
from .serializers import NoteSerializer
from rest_framework.permissions import IsAuthenticated

class RegisterView(generics.CreateAPIView):
    def post(self, request):
        data = request.data
        if User.objects.filter(username=data.get('username')).exists():
            return Response({'error': 'Nazwa użytkownika istnieje'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.create_user(
            username=data['username'],
            password=data['password']
        )
        return Response({'status': 'Rejestracja udana'}, status=status.HTTP_201_CREATED)

class NoteList(generics.ListCreateAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class NoteDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)