from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from PIL import Image


class Publisher(models.Model):
    name = models.CharField(max_length=200)
    website = models.URLField()
    city = models.CharField(max_length=20, blank=True)
    country=models.CharField(max_length=200,default='USA')

    def __str__(self):
        return self.name


class Book(models.Model):
    CATEGORY_CHOICES = [
        ('S', 'Scinece&Tech'),
        ('F', 'Fiction'),
        ('B', 'Biography'),
        ('T', 'Travel'),
        ('O', 'Other')
    ]

    title = models.CharField(max_length=200)
    category = models.CharField(max_length=1, choices=CATEGORY_CHOICES, default='S')
    num_pages = models.PositiveIntegerField(default=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MaxValueValidator(1000), MinValueValidator(0)])
    publisher = models.ForeignKey(Publisher, related_name='books', on_delete=models.CASCADE)
    description=models.TextField(max_length=500, blank=True)
    num_reviews=models.PositiveIntegerField(default=0, validators=[MaxValueValidator(5), MinValueValidator(1)])

    def __str__(self):
        return self.title


class Member(User):
    STATUS_CHOICES = [
        (1, 'Regular member'),
        (2, 'Premium Member'),
        (3, 'Guest Member'),
    ]

    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    address = models.CharField(max_length=300, blank=True)
    city = models.CharField(max_length=20, default="Windsor")
    province=models.CharField(max_length=2, default='ON')
    last_renewal = models.DateField(default=timezone.now)
    auto_renew = models.BooleanField(default=True)
    borrowed_books = models.ManyToManyField(Book, blank=True)
    # image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return self.username

    def get_borrowed_books(self):
        return " , ".join([b.title for b in self.borrowed_books.all()])
    get_borrowed_books.short_description = 'Borrowed Books'


class Order(models.Model):
    STATUS_CHOICES =[
        (0,'Purchase'),
        (1, 'Borrow')
    ]
    # id = models.AutoField(primary_key=True)
    books=models.ManyToManyField(Book)
    member= models.ForeignKey(Member, related_name='order', on_delete=models.CASCADE)
    order_type=models.IntegerField(choices=STATUS_CHOICES,default=1)
    order_date=models.DateField(default=timezone.now)

    def __str__(self):
        return str(self.id)

    def total_items(self):
        # return str(self.books)
        num_orders=self.books.count()
        return num_orders

    def book_list(self):
        books=self.books.all()
        print(books)


class Review(models.Model):
    reviewer=models.EmailField()
    book=models.ForeignKey(Book, on_delete=models.CASCADE)
    rating=models.PositiveIntegerField()
    comments=models.TextField(null=True, blank=True)
    date=models.DateField(default=timezone.now)

    def __str__(self):
        return str(self.reviewer)


class Profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    image=models.ImageField(default='default.png', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self):
        super().save()
        img=Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size=(300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)





