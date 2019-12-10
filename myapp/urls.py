from django.urls import path
from myapp import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.conf.urls import url, include
from django.urls import reverse_lazy

app_name="myapp"

urlpatterns=[

    path(r'',views.Index.as_view(), name='index'),
    path('about/',views.about,name='about'),
    path(r'<int:book_id>/',views.Detail.as_view(), name='detail'),
    path(r'findbooks/',views.findbooks,name='findbooks'),
    path(r'place_order/',views.place_order,name='place_order'),
    path(r'review/',views.review,name='review'),
    path('user_login/',auth_views.LoginView.as_view(),name='user_login'),
    path(r'user_logout/',views.user_logout,name='user_logout'),
    path(r'check_reviews/<int:book_id>/',views.chk_reviews,name='check_reviews'),
    path(r'user_register/', views.user_register, name='user_register'),
    path(r'myorders/', views.myorders, name='myorders'),
    path(r'profile/',views.profile,name='profile'),
    path(r'media/',serve,{'document_root':settings.MEDIA_ROOT}),
    path('', include('django.contrib.auth.urls')),

    path('forgot_password/',views.forgot_password,name='forgot_password'),

    path('change_password/',views.change_password,name='change_password'),

    # path(r'password-reset/', auth_views.PasswordResetView.as_view(template_name='myapp/password_reset.html'),
    #      name='password_reset'),
    # path(r'password-reset/done/',
    #      auth_views.PasswordResetDoneView.as_view(template_name='myapp/password_reset_done.html'),
    #         name='password_reset_done'),
    # path(r'password-reset-confirm/<uidb64>/<token>/',
    #      auth_views.PasswordResetConfirmView.as_view(template_name='myapp/password_reset_confirm.html'),
    #      name='password_reset_confirm'),
    # path(r'password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
    #      name='password_reset_complete'),
]


# if settings.DEBUG:
#     urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)