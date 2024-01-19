from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
app_name = 'transactions'
from .views import (
    PurchaseListView,
    PurchaseDetailView,
    PurchaseCreateView,
    PurchaseUpdateView,
    PurchaseDeleteView,
    SaleListView,
    SaleDetailView,
    
    SaleUpdateView,  
)

urlpatterns = [
    path('purchases/', PurchaseListView.as_view(), name="purchaseslist"),
    path('purchase/<slug:slug>/', PurchaseDetailView.as_view(), name='purchase-detail'),
    path('new-purchase/', PurchaseCreateView.as_view(), name='purchase-create'),
    path('purchase/<int:pk>/update/', PurchaseUpdateView.as_view(), name='purchase-update'),
    path('purchase/<int:pk>/delete/', PurchaseDeleteView.as_view(), name='purchase-delete'),
    path('sales/',SaleListView.as_view(), name="saleslist"),
    path('sale/<int:pk>/',SaleDetailView.as_view(),name='sale-detail'),
    path('sale-delete/<int:pk>/',views.sale_delete,name='sale-delete'),
    path('sale/<slug:slug>/update/', SaleUpdateView.as_view(), name='sale-update'),
    path('billing_details/',views.billing_details,name='billing_details'),#sale
    path('add_item/<slug:slug>/',views.add_item,name='add_item'),
    path('new_bill/',views.new_bill,name='new_bill'),
    path('print_bill/',views.generate_bill,name='print_bill'),
    path('delete_bill_single/<int:pk>/',views.delete_bill_single,name='delete_bill_single')

]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)