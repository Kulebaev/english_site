from django.contrib import admin
from .models import Book, Subscriber, Image

admin.site.register(Book)
admin.site.register(Image)
admin.site.register(Subscriber)
