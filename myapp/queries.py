import django
from myapp.models import Book

print(Book.objects.all())