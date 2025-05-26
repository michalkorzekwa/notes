from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

def validate_hex_color(value):
    if not value.startswith('#') or len(value) not in [4, 7]:
        raise ValidationError('Nieprawidłowy format koloru HEX')

class Note(models.Model):
    STATUS_CHOICES = [
        ('todo', 'Do zrobienia'),
        ('in_progress', 'W trakcie'),
        ('done', 'Zrobione'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, default='', blank=True)
    content = models.TextField(default='', blank=True)
    color = models.CharField(
        max_length=7,
        default='#ffffff',
        validators=[validate_hex_color]
    )
    position = models.JSONField(default=dict, blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='todo'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def clean(self):
        if not self.position.get('x') or not self.position.get('y'):
            self.position = {'x': 100, 'y': 100}