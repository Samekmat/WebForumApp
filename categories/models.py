from django.db import models
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from rest_framework.exceptions import ValidationError


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def delete(self, *args, **kwargs):
        if self.name == "Default":
            raise ValidationError("The 'Default' category cannot be deleted.")
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.name


@receiver(post_migrate)
def create_default_category(sender, **kwargs):
    if sender.name == "categories":

        if not Category.objects.filter(name="Default").exists():
            Category.objects.create(name="Default")
