from rest_framework import serializers
from .models import Note

class NoteSerializer(serializers.ModelSerializer):
    tags_list = serializers.ReadOnlyField(source='get_list_tags')

    class Meta:
        model = Note
        fields = {
            'id', 'title', 'content', 'priority', 'status',
            'created_at', 'updated_at', 'due_date', 'tags', 'tags_list',
        }

    def validate_tags(self,value):
        """
        Validates the tags field.
        """
        if value:
            tags = [tag.strip() for tag in value.split(',')]
            return ', '.join(tags)
        return value

