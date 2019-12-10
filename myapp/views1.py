from django.http import HttpResponse
from .models import Publisher, Book, Member, Order


# def index(request):
#     response = HttpResponse()
#     booklist = Book.objects.all().order_by('id')[:10]
#     heading = "<p>List of available Books</p>"
#     response.write(heading)
#     for book in booklist:
#         para = "<p>" + str(book.id) + " : " + str(book) +"</p>"
#         # + " : " + str(book.publisher.name) + " : " + str(
#             # book.publisher.city) +
#         response.write(para)
#
#     return response


def index(request):
    response = HttpResponse()
    book_list = Book.objects.all().order_by('id')[:10]
    publisher_list=Publisher.objects.all().order_by('city').reverse()
    heading = "<p>List of available Books</p>"
    response.write(heading)

    for book in book_list:
        book_details = "<p>" + str(book.id) + " : " + str(book) + "</p>"
        response.write(book_details)

    for publisher in publisher_list:
        publisher_details ="<p>"+str(publisher.name)+" : "+str(publisher.city)+"</p>"
        response.write(publisher_details)

    return response


def about(request):
    heading="This is an eBook APP"
    response=HttpResponse()
    response.write(heading)
    return response


def detail(request,book_id):
    booktitle=Book.objects.filter(id=book_id)
    response=HttpResponse()
    for book in booktitle:
        para="<p>"+str(book.title).upper()+" : "+"$"+str(book.price)+" : " + str(book.publisher.name) + "</p>"
        response.write(para)
    return response

