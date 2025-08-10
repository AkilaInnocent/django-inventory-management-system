from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    # Admin URLs
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/product/add/', views.add_product, name='add_product'),
    path('admin/product/update/<int:pk>/', views.update_product, name='update_product'),
    path('admin/product/delete/<int:pk>/', views.delete_product, name='delete_product'),
    path('admin/analysis/', views.analysis, name='analysis'),
    path('admin/consumption/', views.admin_consumption, name='admin_consumption'),
    path('admin/consumption/add/', views.add_consumption, name='add_consumption'),
    path('admin/consumption/update/<int:pk>/', views.update_consumption, name='update_consumption'),
    path('admin/consumption/delete/<int:pk>/', views.delete_consumption, name='delete_consumption'),

    # Non-admin URLs
    path('sales/', views.sales, name='sales'),
    path('sales/add/', views.add_sale, name='add_sale'),
    path('sales/update/<int:pk>/', views.update_sale, name='update_sale'),
    path('sales/delete/<int:pk>/', views.delete_sale, name='delete_sale'),
    path('consumption/', views.user_consumption, name='user_consumption'),
    path('consumption/add/', views.add_user_consumption, name='add_user_consumption'),
    path('consumption/update/<int:pk>/', views.update_user_consumption, name='update_user_consumption'),
    path('consumption/delete/<int:pk>/', views.delete_user_consumption, name='delete_user_consumption'),

    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout'),
]