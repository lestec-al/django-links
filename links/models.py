from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save

class Link(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="link", blank=True, null=True)
    original = models.URLField()
    counter = models.IntegerField(default=0)
    slug = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse("link", kwargs={"slug": self.slug})

    def __str__(self):
        return self.original

def create_slug_from_id(instance, created, *args, **kwargs):
    if created:
        id = instance.id
        map = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        shortURL = ""
        while(int(id) > 0):
            shortURL += map[id % 62]
            id //= 62
        instance.slug = shortURL[len(shortURL): : -1]
        instance.save()

post_save.connect(receiver=create_slug_from_id, sender=Link)