from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from notes.views import RegisterView, NoteList, NoteDetail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/register/', RegisterView.as_view()),
    path('api/login/', TokenObtainPairView.as_view()),
    path('api/notes/', NoteList.as_view()),
    path('api/notes/<int:pk>/', NoteDetail.as_view()),
]