from django.urls import path
from . import views
app_name = 'sales'
urlpatterns = [
    path('', views.sale_list, name='sale_list'),
    path('sale/<int:pk>/', views.sale_detail, name='sale_detail'),
    path('sale/new/', views.sale_create, name='sale_create'),
    path('sale/<int:pk>/edit/', views.sale_update, name='sale_update'),
    path('sale/<int:pk>/delete/', views.sale_delete, name='sale_delete'),
    path('<int:pk>/edit/', views.edit_sale, name='edit_sale'),
]