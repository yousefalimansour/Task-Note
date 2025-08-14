# backend/notes/views.py
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q
from .models import Note
from .serializers import NoteSerializer

class NoteListCreateView(generics.ListCreateAPIView):
    serializer_class = NoteSerializer
    
    def get_queryset(self):
        queryset = Note.objects.all()
        
        # Filter by status
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filter by priority
        priority_filter = self.request.query_params.get('priority', None)
        if priority_filter:
            queryset = queryset.filter(priority=priority_filter)
        
        # Search in title and content
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(content__icontains=search)
            )
        
        # Filter by tags
        tags = self.request.query_params.get('tags', None)
        if tags:
            queryset = queryset.filter(tags__icontains=tags)
        
        return queryset

class NoteDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

@api_view(['GET'])
def note_stats(request):
    """Get statistics about notes"""
    total_notes = Note.objects.count()
    completed_notes = Note.objects.filter(status='completed').count()
    in_progress_notes = Note.objects.filter(status='in_progress').count()
    todo_notes = Note.objects.filter(status='todo').count()
    
    # Priority breakdown
    high_priority = Note.objects.filter(priority='high').count()
    medium_priority = Note.objects.filter(priority='medium').count()
    low_priority = Note.objects.filter(priority='low').count()
    
    stats = {
        'total': total_notes,
        'completed': completed_notes,
        'in_progress': in_progress_notes,
        'todo': todo_notes,
        'high_priority': high_priority,
        'medium_priority': medium_priority,
        'low_priority': low_priority,
    }
    
    return Response(stats)

@api_view(['PATCH'])
def update_note_status(request, pk):
    """Quick status update endpoint"""
    try:
        note = Note.objects.get(pk=pk)
    except Note.DoesNotExist:
        return Response({'error': 'Note not found'}, status=status.HTTP_404_NOT_FOUND)
    
    new_status = request.data.get('status')
    if new_status not in ['todo', 'in_progress', 'completed']:
        return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
    
    note.status = new_status
    note.save()
    
    serializer = NoteSerializer(note)
    return Response(serializer.data)