from django.db import models


class Note(models.Model):
    title = models.CharField(max_length=250)
    content = models.TextField(max_length=1000, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return self.title