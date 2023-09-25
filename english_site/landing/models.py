from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    image = models.FileField(upload_to='book_images/')
    file = models.FileField(upload_to='book_files/')
    user = models.CharField(max_length=100)  # Максимальная длина может быть на ваше усмотрение

    def __str__(self):
        return self.title
