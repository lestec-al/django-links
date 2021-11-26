from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

class Links(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='links', blank=True, null=True)
    original = models.TextField()
    counter = models.IntegerField(default=0)
    slug = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('link', kwargs={'slug': self.slug})

    def __str__(self):
        return self.original