from django.db import models
from django.contrib.auth.models import User

class Client(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    company = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    # Add other fields if needed

    def __str__(self):
        return self.name

class Note(models.Model):
    client = models.ForeignKey(Client, related_name='notes', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Note for {self.client.name} by {self.author}" if self.author else f"Note for {self.client.name}"

class ClientHistory(models.Model):
    client = models.ForeignKey(Client, related_name='history', on_delete=models.CASCADE)
    action = models.CharField(max_length=100)
    performed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.TextField(blank=True)

    def __str__(self):
        return f"{self.client.name} - {self.action} at {self.timestamp}"