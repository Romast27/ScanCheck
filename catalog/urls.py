from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload_photo/', views.upload_photo, name='upload_photo'),
    path('barcode/<int:barcode>/', views.barcode_detail, name='barcode_detail'),
    path("signup/", views.sign_up, name="signup"),
]
