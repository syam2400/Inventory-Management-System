from django.urls import path
from store import views
from django.conf.urls.static import static
from django.conf import settings
from .views import (
    ProductListView,
    ProductDetailView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    ItemSearchListView,
    DeliveryListView,
    DeliveryDetailView,
    DeliveryCreateView,
    DeliveryUpdateView,
    DeliveryDeleteView,


)
from store import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('products/',ProductListView.as_view(), name="productslist"),
    path('product/<slug:slug>/', ProductDetailView.as_view(), name='product-detail'),
    path('new-product/', ProductCreateView.as_view(), name='product-create'),
    path('product/<slug:slug>/update/', ProductUpdateView.as_view(), name='product-update'),
    path('product/<slug:slug>/delete/', ProductDeleteView.as_view(), name='product-delete'),
    path('search/',ItemSearchListView.as_view(), name="item_search_list_view"),

    path('notify_close_to_expiry/', views.notify_close_to_expiry, name='notify_close_to_expiry'),
    path('discount',views.discount,name='discount'),
    path('deliveries/',DeliveryListView.as_view(), name="deliveries"),
    path('delivery/<slug:slug>/', DeliveryDetailView.as_view(), name='delivery-detail'),
    path('new-delivery/', DeliveryCreateView.as_view(), name='delivery-create'),
    path('delivery/<int:pk>/update/', DeliveryUpdateView.as_view(), name='delivery-update'),
    path('delivery/<int:pk>/delete/', DeliveryDeleteView.as_view(), name='delivery-delete'),
    path('generate_qr_code/<int:item_id>/', views.generate_qr_code, name='generate_qr_code'),
    path('category_selling_percentage',views.category_selling_percentage,name='category_selling_percentage'),
    path('scan_qrcode',views.scan_qrcode,name='scan_qrcode')
    

]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)