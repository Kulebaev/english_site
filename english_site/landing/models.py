from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    image = models.ManyToManyField('Image', blank=True)
    file = models.FileField(upload_to='book_files/')

    def __str__(self):
        return self.title
    
class Image(models.Model):
    file = models.FileField(upload_to='book_images/')


class Subscriber(models.Model):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email
