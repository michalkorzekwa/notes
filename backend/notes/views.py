from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Note
from .serializers import NoteSerializer
from rest_framework.permissions import IsAuthenticated

class RegisterView(generics.CreateAPIView):
    def post(self, request):
        data = request.data
        errors = {}
        
        if not data.get('username'):
            errors['username'] = ['Pole wymagane']
        if not data.get('password'):
            errors['password'] = ['Pole wymagane']
            
        if User.objects.filter(username=data.get('username', '')).exists():
            errors['username'] = ['Nazwa użytkownika jest już zajęta']
            
        if errors:
            return Response(
                {'errors': errors},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        try:
            User.objects.create_user(
                username=data['username'],
                password=data['password']
            )
            return Response(
                {'detail': 'Rejestracja zakończona pomyślnie'},
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {'detail': 'Wewnętrzny błąd serwera'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

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
    

