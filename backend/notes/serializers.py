from rest_framework import serializers
from .models import Note

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['id', 'title', 'content', 'color', 'position']
        extra_kwargs = {
            'user': {'read_only': True},
            'position': {'required': False},
            'color': {'required': False, 'default': '#ffeb3b'}
        }

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)