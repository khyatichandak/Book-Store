from django.shortcuts import render,get_object_or_404
from .models import Book, Review, Order, Member
from django.http import HttpResponse, HttpResponseRedirect
from .forms import SearchForm, OrderForm, ReviewForm, RegisterForm, LoginForm, UserUpdateForm, ProfileUpdateForm, PasswordRequestForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
import random, datetime, string
from django.contrib import messages
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash


from django.core.mail import send_mail


class Index(View):

    def get(self, request):
        booklist=Book.objects.all().order_by('id')
        return render(request,'myapp/index.html',{'booklist':booklist})

    def post(self,request):
        booklist = Book.objects.all().order_by('id')
        return render(request,'myapp/index.html')


def about(request):
    cookie_value=request.COOKIES.get('lucky_num')
    response = HttpResponse()
    if cookie_value is None:
        mynum = random.randint(1, 100)
    else:
        mynum = request.COOKIES['lucky_num']
    response= render(request,'myapp/about.html',{'mynum':mynum})
    response.set_cookie('lucky_num', mynum, expires=300)
    return response


class Detail(View):
    # book=Book.objects.get(id=book_id)

    def get(self,request, book_id):
        book=get_object_or_404(Book,id=book_id)
        return render(request,'myapp/detail.html',{'book':book})

    def post(self,request):
        pass


def findbooks(request):
    if request.method == 'POST':
        form= SearchForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            category = form.cleaned_data['category']
            max_price = form.cleaned_data['max_price']
            if category:
                booklist = Book.objects.filter(category=category, price__lte=max_price)
            else:
                booklist=Book.objects.filter(price__lte=max_price)
            return render(request, 'myapp/results.html',{'booklist':booklist,'name':name,'category':category})
        else:
            return HttpResponse('Invalid data')
    else:
        form=SearchForm()
        return render(request,'myapp/findbooks.html',{'form':form})


def place_order(request):
    if request.method == 'POST':

        form = OrderForm(request.POST)
        if form.is_valid():
            books = form.cleaned_data['books']
            order = form.save()
            member = order.member
            type = order.order_type
            order.save()
            if type == 1:
                for b in order.books.all():
                    member.borrowed_books.add(b)

            return render(request, 'myapp/order_response.html', {'books': books, 'order': order})
        else:
            return render(request, 'myapp/placeorder.html', {'form': form})

    else:
        form=OrderForm()
        return render(request, 'myapp/placeorder.html', {'form':form})


@login_required
def review(request):
    username=request.user.username
    member_status = Member.objects.filter(username=username).values('status')
    if member_status[0]['status'] == 1 or member_status[0]['status'] == 2:
        # [{key:value}]
        if request.method=='POST':

            form=ReviewForm(request.POST)

            if form.is_valid():
                rating=form.cleaned_data['rating']
                review = form.save()
                book=review.book
                if rating in range(1,6):
                    review.save()
                    book_update=Book.objects.get(title=book)
                    book_update.num_reviews += 1
                    book_update.save()

                    booklist = Book.objects.all().order_by('id')
                    messages.success(request,'Your review is submitted!')
                    return render(request,'myapp/index.html',{'booklist':booklist})
                else:
                    form = ReviewForm()
                    return render(request, 'myapp/review.html', {'form':form, 'error': 'You must enter a rating between 1 and 5!'})
            else:
                return HttpResponse('Please enter all valid fields')

        else:
            form=ReviewForm()
            return render(request, 'myapp/review.html', {'form':form, 'error': ''})
    else:
        # form = ReviewForm()
        return render(request, 'myapp/review.html',
                      {'error': 'You are not able to submit the review!'})


def user_login(request):
    if request.method=='POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            # username = form.cleaned_data.get('username')
            messages.success(request, f'AYou are successfully Logged In!')
            # return HttpResponseRedirect(request.POST.get('next','/'))
            if 'next' in request.POST:
                return render(request.POST.get('next'))
            else:
                # return HttpResponseRedirect(reverse('myapp:index'))
                return render(request, 'myapp/index.html')
        else:
            # messages.error(request,f'Invalid data. Try again!')
            return render(request, 'myapp/login.html', {'form':form})
    else:
        form = LoginForm()
        return render(request,'myapp/login.html',{'form':form})

    # username=request.POST['username']
    # request.session['username']=username
    # password=request.POST['password']
    # user=authenticate(username=username,password=password)
    # if user:
    #     if user.is_active:
    #         # next=request.POST.get('next','/')
    #         login(request,user)
    #         now=datetime.datetime.now()
    #         request.session['last_login']=now.strftime("%d-%m-%Y %H:%M:%S")
    #         request.session.set_expiry(60)
    #         # return HttpResponseRedirect(reverse('myapp:index'))
    #         return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    #     else:
    #         return HttpResponse('Your account is disabled.')
    # else:
    #     return HttpResponse('Invalid login details.')


@login_required
def user_logout(request):
    logout(request)
    return render(request, 'myapp/logout.html')
    # del request.session['username']
    return HttpResponseRedirect(reverse('myapp:index'))


@login_required
def chk_reviews(request,book_id):

    member=Member.objects.filter(username=request.user)
    avg = 0
    if member:
        book=Review.objects.filter(book__id=book_id).values_list('rating',flat=True)

        if len(book)>0:
            avg=sum(book)/len(book)

        return render(request,'myapp/chk_reviews.html',{'avg':avg,'member':member})
    else:
        # return HttpResponse('You are not a registered member!')
        # return HttpResponseRedirect(request.POST.get('next', '/'))
        form = LoginForm()
        return render(request,'myapp/login.html',{'form':form})


def user_register(request):

    if request.method=='POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            # error, warning, info

            return render(request, 'myapp/index.html')
        # else:
        #     messages.error(request,UserCreationForm.error_messages['password_mismatch'])
        # username=request.POST['username']
        # password=request.POST['password']
        # if username and password:
        #     return render(request,'myapp/index.html')
        # else:
        #     return HttpResponse('Invalid details.')
    else:
        form = RegisterForm()
    return render(request, 'myapp/register.html', {'form': form})


@login_required
def myorders(request):
    username = request.user.username
    member = Member.objects.get(username=username)
    # print()
    if member:
        order_list=Member.objects.filter(borrowed_books__title__startswith='', username=username).values('borrowed_books__title')
        return render(request,'myapp/myorders.html',{'order_list':order_list})

    else:
        return HttpResponse('You are not a registered member!')


@login_required
def profile(request):
    if request.method=='POST':
        u_form=UserUpdateForm(request.POST,instance=request.user)
        p_form=ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()

            messages.success(request,'Your profile is updated successfully!')
            u_form = UserUpdateForm(instance=request.user)
            p_form = ProfileUpdateForm(instance=request.user.profile)
            context = {
                'u_form': u_form,
                'p_form': p_form
            }
            return render(request,'myapp/profile.html',context)

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

        context = {
            'u_form': u_form,
            'p_form': p_form
        }

        return render(request,'myapp/profile.html', context)


def forgot_password(request):
    if request.method=='POST':
        form=PasswordRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            last_name = form.cleaned_data['last_name']
            first_name = form.cleaned_data['first_name']

            lettersAndDigits = string.ascii_letters + string.digits
            random_pass = ''.join(random.choice(lettersAndDigits) for i in range(8))
            user=User.objects.get(last_name=last_name,first_name=first_name)
            user.set_password(random_pass)
            user.save()

            subject="Password Recovery"
            from_email="chandakk@uwindsor.ca"
            to_email=[email]
            msg1="This email is for password recovery. The new password is: "
            msg2=random_pass
            msg3=" You can Log In here: http://127.0.0.1:8000/myapp/user_login/"
            signup_message=msg1+msg2+msg3
            send_mail(subject=subject,from_email=from_email,recipient_list=to_email, message=signup_message, fail_silently=False)

            return render(request, 'myapp/forgot_password_done.html')
        else:
            return render(request, 'myapp/forgot_password.html', {'form': form})

    else:
        form=PasswordRequestForm()
        return render(request,'myapp/forgot_password.html',{'form':form})


@login_required
def change_password(request):
    if request.method=='POST':
        form=PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user=form.save()
            update_session_auth_hash(request, user)
            messages.success(request,'password changed successfully!')
            return render(request,'myapp/change_password.html')
        else:
            return render(request, 'myapp/change_password.html', {'form': form})
    else:
        form = PasswordChangeForm(request.user)
        return render(request,'myapp/change_password.html',{'form':form})