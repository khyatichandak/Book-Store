from django.urls import path
from myapp import views
from django.conf import settings
from django.views.static import serve
from django.conf.urls import url, include


app_name="myapp"

urlpatterns=[

    path(r'',views.Index.as_view(), name='index'),
    path('about/',views.about,name='about'),
    path(r'<int:book_id>/',views.Detail.as_view(), name='detail'),
    path(r'findbooks/',views.findbooks,name='findbooks'),
    path(r'place_order/',views.place_order,name='place_order'),
    path(r'review/',views.review,name='review'),
    path(r'user_login/',views.user_login,name='user_login'),
    path(r'user_logout/',views.user_logout,name='user_logout'),
    path(r'check_reviews/', views.chk_reviews, name='check_reviews'),
    path(r'check_reviews_done/<int:book_id>/',views.chk_reviews_done,name='check_reviews_done'),
    path(r'user_register/', views.user_register, name='user_register'),
    path(r'myorders/', views.myorders, name='myorders'),
    path(r'profile/',views.profile,name='profile'),
    path(r'media/',serve,{'document_root':settings.MEDIA_ROOT}),
    path('', include('django.contrib.auth.urls')),

    path('forgot_password/',views.forgot_password,name='forgot_password'),

    path('change_password/',views.change_password,name='change_password'),

]
