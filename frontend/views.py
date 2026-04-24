from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def index(request):
     if request.user.is_authenticated:
           return render(request, "frontend/index.html")
     return render(request, "frontend/login.html")


def register(request):
     return render(request, "frontend/register.html")


def login(request):
     return render(request, "frontend/login.html")


def figma(request):
    return render(request, "frontend/Figma.html")

def sale(request):
    return render(request, "frontend/new_sale.html")


def product(request):
    return render(request, "frontend/new_product.html")

def product_table(request):
    return render(request, "frontend/products_table.html")

def expiry_medicine_table(request):
    return render(request, "frontend/expiry_medicine.html")

def settings_table(request):
    return render(request, "frontend/settings.html")

def report_table(request):
    return render(request, "frontend/report_pharma.html")
def product_in_out(request):
    return render(request, "frontend/in_and_out.html")
