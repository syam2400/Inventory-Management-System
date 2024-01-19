import qrcode
from autoslug.utils import generate_unique_slug
from django.http import HttpResponse
from django.shortcuts import render

from .forms import InvoiceForm
from .models import *
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django_tables2 import SingleTableView
import django_tables2 as tables
from django_tables2.export.views import ExportMixin
from django_tables2.export.export import TableExport
from .tables import InvoiceTable
# import cv2
from django.shortcuts import render, redirect
from .models import Invoice

from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)


class InvoiceListView(LoginRequiredMixin, ExportMixin, tables.SingleTableView):
    model = Invoice
    table_class = InvoiceTable
    template_name = 'invoice/invoicelist.html'
    context_object_name = 'invoices'
    paginate_by = 10
    SingleTableView.table_pagination = False

class InvoiceDetailView(DetailView):
    model = Invoice
    template_name = 'invoice/invoicedetail.html'

    def get_success_url(self):
        return reverse('invoice-detail',  kwargs={'slug': self.object.pk})



class InvoiceCreateView(LoginRequiredMixin,CreateView):
    model = Invoice
    template_name = 'invoice/invoicecreate.html'
    fields = ['customer_name','contact_number','item','price_per_item','quantity', 'shipping','Qr_code']

    def form_valid(self, form):
        return super().form_valid(form)
    def get_success_url(self):
        return reverse('invoicelist')





def scan_qr_code(request):
    if request.method == 'POST':
        form = InvoiceForm(request.POST, request.FILES)
        if form.is_valid():
            qr_code = request.FILES.get('Qr_code')
            qr_data = decode_qr_code(qr_code)

            if qr_data:
                invoice = form.save(commit=False)
                invoice.slug = generate_unique_slug()
                # Set item and price_per_item from decoded data
                invoice.item = qr_data.get('Item ID')  # Assuming 'item' is a field in the decoded data
                invoice.price_per_item = qr_data.get(
                    'selling_price')  # Assuming 'price_per_item' is a field in the decoded data

                # Set other fields from the form
                invoice.date = form.cleaned_data['date']
                invoice.customer_name = form.cleaned_data['customer_name']
                invoice.contact_number = form.cleaned_data['contact_number']
                invoice.quantity = form.cleaned_data['quantity']
                invoice.shipping = form.cleaned_data['shipping']
                invoice.total = form.cleaned_data['total']
                invoice.grand_total = form.cleaned_data['grand_total']

                invoice.save()
                return redirect('success_page')
            else:
                return render(request, 'error_page.html')
    else:
        form = InvoiceForm()

    return render(request, 'scan_qr_code.html', {'form': form})


def decode_qr_code(qr_code):
    # Use OpenCV to read the QR code and return the decoded data
    qr_code_path = qr_code.temporary_file_path()
    image = cv2.imread(qr_code_path)
    detector = cv2.QRCodeDetector()
    retval, decoded_info, points, straight_qrcode = detector.detectAndDecodeMulti(image)
    return decoded_info


class InvoiceUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Invoice
    template_name = 'invoice/invoiceupdate.html'
    fields = ['customer_name','contact_number','item','price_per_item','quantity','shipping',]

    def get_success_url(self):
        return reverse('invoicelist')

    def form_valid(self, form):
        return super().form_valid(form)

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        else:
            return False


class InvoiceDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Invoice
    template_name = 'invoice/invoicedelete.html'
    success_url = '/products'

    def get_success_url(self):
        return reverse('invoicelist')

    def test_func(self):
        item = self.get_object()
        if self.request.user.is_superuser:
            return True
        else:
            return False


def scan_qr_code(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['qr_code']
        img = qrcode.imread(uploaded_file)

        # Assuming the QR code encodes the item ID as text
        try:
            decoded_data = img[0][0]  # Assuming the ID is stored at the first position
            item_id = decoded_data.decode('utf-8')  # Decode bytes to string
            # Now you have the item ID, you can use it to associate with the entry

            return HttpResponse(f"QR code scanned successfully. Item ID: {item_id}")
        except Exception as e:
            return HttpResponse(f"Error decoding QR code: {e}")

    return render(request, 'scan_qr_code.html')