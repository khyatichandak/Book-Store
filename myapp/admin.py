from django.contrib import admin
from .models import Publisher, Book, Member, Order, Review, Profile


def increase_price(modeladmin, request, queryset):
    for book in queryset:
        book.price+=10
        book.save()
    increase_price.short_description = 'Increase price by $10'


class BookAdmin(admin.ModelAdmin):
    fields=[('title','category','publisher'),('num_pages','price','num_reviews')]
    list_display = ('title','category','price')
    actions=[increase_price]


class OrderAdmin(admin.ModelAdmin):
    fields = [('books'),('member','order_type','order_date')]
    list_display = ('id','member','order_type','order_date', 'total_items')


class PublisherAdmin(admin.ModelAdmin):
    fields=[('name','website'),('city','country')]
    list_display = ('name','website','city')


class MemberAdmin(admin.ModelAdmin):
    list_display = ('username','first_name','last_name','status','get_borrowed_books')


# Register your models here.
admin.site.register(Publisher, PublisherAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Review)
admin.site.register(Profile)

