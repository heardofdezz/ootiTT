from django.db import models

class Todo(models.Model):
    
    class Status(models.TextChoices):
        PENDING = 'pending', 'EN ATTENTE'
        IN_PROGRESS = 'in_progress', 'EN COURS'
        DONE = 'done', 'Finit'
    
    title = models.CharField(max_length=250)
    description = models.TextField(max_length=1000, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    note = models.ForeignKey('notes.Note', related_name='todos', on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title