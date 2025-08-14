from django.urls import path
from .views import (
    NoteListCreateView, 
    NoteDetailView, 
    note_stats, 
    update_note_status
)

urlpatterns = [
    path('notes/', NoteListCreateView.as_view(), name='note-list-create'),
    path('notes/<int:pk>/', NoteDetailView.as_view(), name='note-detail'),
    path('notes/<int:pk>/status/', update_note_status, name='note-status-update'),
    path('stats/', note_stats, name='note-stats'),
]