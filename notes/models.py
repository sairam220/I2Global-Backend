from django.db import models
from uuid import uuid4
from datetime import datetime

class Note(models.Model):
    note_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    note_title = models.CharField(max_length=255)
    note_content = models.TextField()
    user = models.ForeignKey('authentication.User', related_name='notes', on_delete=models.CASCADE)
    created_on = models.DateTimeField(default=datetime.utcnow)
    last_update = models.DateTimeField(default=datetime.utcnow)

    def __str__(self):
        return self.note_title

    # Override the save method to update 'last_update' field on each update
    def save(self, *args, **kwargs):
        if not self.pk:  # If the object is being created (not updated)
            self.created_on = datetime.utcnow()
        self.last_update = datetime.utcnow()  # Update the last_update time on save
        super().save(*args, **kwargs)  # Call the parent save method to save the instance
    