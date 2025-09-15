from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import Note
from .serializers import NoteSerializer
from django.shortcuts import get_object_or_404

# List notes (GET)
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_notes(request):
    notes = Note.objects.filter(user=request.user)
    serializer = NoteSerializer(notes, many=True)
    return Response(serializer.data)

# Create note (POST)
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_note(request):
    serializer = NoteSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)  # Associate note with logged-in user
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Edit note (PUT)
@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def update_note(request, note_id):
    note = get_object_or_404(Note, note_id=note_id, user=request.user)
    serializer = NoteSerializer(note, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Delete note (DELETE)
@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def delete_note(request, note_id):
    note = get_object_or_404(Note, note_id=note_id, user=request.user)
    note.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
