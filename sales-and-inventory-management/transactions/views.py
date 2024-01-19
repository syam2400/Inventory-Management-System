import random
from django.shortcuts import render , redirect
from datetime import timedelta
from datetime import datetime
from .models import *
from django.contrib.auth.models import User
from .filters import PurchaseFilter, SaleFilter
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import FormMixin
from django_tables2 import SingleTableView
import django_tables2 as tables
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django_tables2.export.views import ExportMixin
from django_tables2.export.export import TableExport
from .tables import PurchaseTable, SaleTable
from django.core.exceptions import ValidationError
from accounts.models import Profile
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from store.models import  Item
from accounts.models import  Profile
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Create your views here.
class PurchaseListView(ExportMixin, tables.SingleTableView):
    model = Purchase
    table_class = SaleTable
    template_name = 'transactions/purchases_list.html'
    context_object_name = 'purchases'
    paginate_by = 10
    SingleTableView.table_pagination = False

class PurchaseDetailView(FormMixin, DetailView):
    model = Purchase
    template_name = 'transactions/sale_detail.html'

    def get_success_url(self):
        return reverse('sale-detail', kwargs={'slug': self.object.slug})

class PurchaseCreateView(LoginRequiredMixin, CreateView):
    model = Purchase
    template_name = 'transactions/purchasescreate.html'
    fields = ['item', 'description', 'vendor', 'order_date', 'delivery_date', 'quantity', 'price', 'delivery_status']

    def form_valid(self, form):
        return super().form_valid(form)
    def get_success_url(self):
        return reverse('purchaseslist')

class PurchaseUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Purchase
    template_name = 'transactions/purchaseupdate.html'
    fields = ['item', 'description', 'vendor', 'order_date', 'delivery_date', 'quantity', 'price', 'delivery_status']

    def form_valid(self, form):
        return super().form_valid(form)
    def get_success_url(self):
        return reverse('purchase-update')
    def test_func(self):
        profiles = Profile.objects.all()
        if self.request.user.profile in profiles:
            return True
        else:
            return False
    def get_success_url(self):
            return reverse('purchaseslist')


class PurchaseDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Purchase
    template_name = 'transactions/purchasedelete.html'

    def test_func(self):
        profiles = Profile.objects.all()
        if self.request.user.profile in profiles:
            return True
        else:
            return False
    def get_success_url(self):
            return reverse('purchaseslist')

#Sales Order
class SaleListView(ExportMixin, tables.SingleTableView):
    model = Sale
    table_class = SaleTable
    template_name = 'transactions/sales_list.html'
    context_object_name = 'sales'
    paginate_by = 10
    SingleTableView.table_pagination = False




@login_required   
def billing_details(request):   
     if request.method == 'POST':       
            cus_name = request.POST['cus_name']
            item_slug = request.POST['selected_item'] 
            item = Item.objects.get(slug=item_slug)
            quantity = float(request.POST['quantity'])
            price = float(request.POST['price'])
            payment_method = request.POST.get('payment_method')
            user=request.user
            user = Profile.objects.get(user=user)
            create_order = Sale.objects.create(customer_name=cus_name,item=item,quantity=quantity,price=price, payment_method=payment_method,profile=user)
            create_order.save()
                   
            current_datetime = timezone.now()
            one_second_ago = current_datetime - timedelta(seconds=5)

            # Fetch the most recent Sale for a specific customer within the last minute
            biling_user = Sale.objects.filter(
                customer_name=cus_name,
                transaction_date__range=(one_second_ago , current_datetime)).order_by('-transaction_date').first()

            bill = Billing.objects.create(sale= biling_user)
            biling_detail = Billing.objects.all()

            item_quantity = create_order.quantity
            product = create_order.item.name
            item_in_db = Item.objects.get(name=product)
            item_in_db.quantity = item_in_db.quantity-item_quantity
            item_in_db.save()

            # items = Item.objects.all()
            # return render(request,'transactions/salescreate.html',{'biling_details': biling_detail ,'items':items,'bill':bill})
            return redirect('transactions:billing_details')
         
     try:
          items = Item.objects.all()
          biling_detail = Billing.objects.all()
          return render(request,'transactions/salescreate.html',{'items':items,'biling_details': biling_detail})
     except Billing.DoesNotExist:
          return redirect('transactions:billing_details')
   

@login_required
def add_item(request,slug):
     add = Item.objects.get(slug=slug)
     price = add.selling_price 
     item_name = add.name
     items = Item.objects.all()
     biling_detail = Billing.objects.all()
     return render(request,'transactions/salescreate.html',{'price':price,'item_name':item_name,'items':items,'biling_details': biling_detail})
    #  return redirect('transactions:billing_details')


def new_bill(request):
    remove_bill = Billing.objects.all()
    remove_bill.delete()    
    return redirect('transactions:billing_details')
    

# for deleting the selected added products in the bill
def delete_bill_single(request,pk):
    billing_instances_to_delete = Billing.objects.filter(id=pk)
    billing_instances_to_delete.delete()
    return redirect('transactions:billing_details')


#  generating bills that customer buys products        
def generate_bill(request):
    # Fetch the sale details using the provided sale_id
    bills = Billing.objects.all()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="bill_{random.randint(0, 99)}.pdf"'

    # Create PDF
    p = canvas.Canvas(response, pagesize=letter)

    # Set up fonts and sizes
    p.setFont("Helvetica-Bold", 12)

    # Define margins and table properties
    left_margin = 50
    top_margin = 750
    row_height = 20
    product_width = 250  # Adjust product column width
    quantity_width = 60
    price_width = 70
    total_bill = 0

    # Write bill details to the PDF
    p.drawString(left_margin + 200, top_margin, "Shop Name")
    p.setFont("Helvetica", 12)
    p.drawString(left_margin, top_margin - 30, "Address: Your Shop Address")
    p.drawString(left_margin, top_margin - 50, "Contact: Your Contact Details")
    p.setFont("Helvetica-Bold", 12)
    p.drawString(left_margin, top_margin - 100, "Bill Details")

    # Initialize variables for table drawing
    y_coordinate = top_margin - 120
    y_end = 100  # Adjust this value to determine where to end the table

    # Draw table headers
    p.drawString(left_margin, y_coordinate, "Product")
    p.drawString(left_margin + product_width, y_coordinate, "Qty")
    p.drawString(left_margin + product_width + quantity_width, y_coordinate, "Price")

    y_coordinate -= row_height  # Move to the next row

    # Draw table rows with properly aligned text and truncated product names
    p.setFont("Helvetica", 12)
    for data in bills:
        product_name = str(data.sale.item)[:40] + "..." if len(str(data.sale.item)) > 30 else data.sale.item
        p.drawString(left_margin, y_coordinate, f"{product_name}")
        p.drawString(left_margin + product_width, y_coordinate, f"{data.sale.quantity}")
        p.drawString(left_margin + product_width + quantity_width, y_coordinate, f"{data.sale.price}")

        y_coordinate -= row_height
        total_bill += data.sale.total_value
        if y_coordinate <= y_end:
            break  # Break loop if reaching the end of the page

    # Draw the total at the end of the table
    p.setFont("Helvetica-Bold", 12)
    p.drawString(left_margin, y_coordinate - 30, f"Total:{total_bill}")

    p.showPage()
    p.save()
    return response

class SaleDetailView(DetailView):
    model = Sale
    template_name = 'transactions/saledetail.html'


class SaleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Sale
    template_name = 'transactions/sale_update.html'
    fields = ['item', 'customer_name', 'payment_method', 'quantity', 'price', 'amount_received']

    def test_func(self):
        profiles = Profile.objects.all()
        if self.request.user.profile in profiles:
            return True
        else:
            return False

    def get_success_url(self):
        return reverse('saleslist')

    def form_valid(self, form):
        form.instance.profile = self.request.user.profile
        return super().form_valid(form)

# this is for deleting sales orders
def sale_delete(request,pk):
    delete_sale = Sale.objects.get(id=pk) 
    delete_sale.delete()
    return redirect('transactions:saleslist')


