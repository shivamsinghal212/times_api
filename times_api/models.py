from django.db import models

# Create your models here.


class Category(models.Model):

    name = models.CharField(max_length=100)
    parent = models.CharField(max_length=100, blank=True)
    is_featured = models.BooleanField(default=False)
    image = models.ImageField(blank=True, upload_to='images/')
    is_active = models.BooleanField(default=False)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    # class Meta:
    #     unique_together = ('name', 'parent')
