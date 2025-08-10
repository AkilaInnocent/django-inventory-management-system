from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from .models import Product, Sale, Consumption
from django.db.models import Sum, Count
from django.contrib import messages

def is_admin(user):
    return user.is_staff

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    products = Product.objects.all()
    return render(request, 'inventory/admin_dashboard.html', {'products': products})

@login_required
@user_passes_test(is_admin)
def add_product(request):
    if request.method == 'POST':
        name = request.POST['name']
        quantity = request.POST['quantity']
        total_invested = request.POST['total_invested']
        description = request.POST.get('description', '')
        Product.objects.create(
            name=name,
            quantity=quantity,
            total_invested=total_invested,
            description=description,
            created_by=request.user
        )
        messages.success(request, 'Product added successfully')
        return redirect('inventory:admin_dashboard')
    return render(request, 'inventory/add_product.html')

@login_required
@user_passes_test(is_admin)
def update_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.name = request.POST['name']
        product.quantity = request.POST['quantity']
        product.total_invested = request.POST['total_invested']
        product.description = request.POST.get('description', '')
        product.save()
        messages.success(request, 'Product updated successfully')
        return redirect('inventory:admin_dashboard')
    return render(request, 'inventory/update_product.html', {'product': product})

@login_required
@user_passes_test(is_admin)
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully')
        return redirect('inventory:admin_dashboard')
    return JsonResponse({'success': True})

@login_required
def sales(request):
    if request.user.is_staff:
        return redirect('inventory:admin_dashboard')
    products = Product.objects.all()
    sales = Sale.objects.filter(created_by=request.user)
    total_sales = sales.aggregate(Sum('amount'))['amount__sum'] or 0
    return render(request, 'inventory/sales.html', {
        'products': products,
        'sales': sales,
        'total_sales': total_sales
    })

@login_required
def add_sale(request):
    if request.user.is_staff:
        return redirect('inventory:admin_dashboard')
    if request.method == 'POST':
        product_id = request.POST['product']
        quantity_sold = request.POST['quantity_sold']
        amount = request.POST['amount']
        description = request.POST.get('description', '')
        product = get_object_or_404(Product, pk=product_id)
        Sale.objects.create(
            product=product,
            quantity_sold=quantity_sold,
            amount=amount,
            description=description,
            created_by=request.user
        )
        messages.success(request, 'Sale recorded successfully')
        return redirect('inventory:sales')
    return render(request, 'inventory/add_sale.html', {'products': Product.objects.all()})

@login_required
def update_sale(request, pk):
    if request.user.is_staff:
        return redirect('inventory:admin_dashboard')
    sale = get_object_or_404(Sale, pk=pk, created_by=request.user)
    if request.method == 'POST':
        sale.product = get_object_or_404(Product, pk=request.POST['product'])
        sale.quantity_sold = request.POST['quantity_sold']
        sale.amount = request.POST['amount']
        sale.description = request.POST.get('description', '')
        sale.save()
        messages.success(request, 'Sale updated successfully')
        return redirect('inventory:sales')
    return render(request, 'inventory/update_sale.html', {'sale': sale, 'products': Product.objects.all()})

@login_required
def delete_sale(request, pk):
    if request.user.is_staff:
        return redirect('inventory:admin_dashboard')
    sale = get_object_or_404(Sale, pk=pk, created_by=request.user)
    if request.method == 'POST':
        sale.delete()
        messages.success(request, 'Sale deleted successfully')
        return redirect('inventory:sales')
    return JsonResponse({'success': True})

@login_required
def user_consumption(request):
    if request.user.is_staff:
        return redirect('inventory:admin_dashboard')
    consumptions = Consumption.objects.filter(created_by=request.user)
    total_consumption = consumptions.aggregate(Sum('amount_used'))['amount_used__sum'] or 0
    return render(request, 'inventory/user_consumption.html', {
        'consumptions': consumptions,
        'total_consumption': total_consumption,
        'products': Product.objects.all()
    })

@login_required
def add_user_consumption(request):
    if request.user.is_staff:
        return redirect('inventory:admin_dashboard')
    if request.method == 'POST':
        product_id = request.POST['product']
        amount_used = request.POST['amount_used']
        description = request.POST.get('description', '')
        product = get_object_or_404(Product, pk=product_id)
        Consumption.objects.create(
            product=product,
            amount_used=amount_used,
            description=description,
            created_by=request.user
        )
        messages.success(request, 'Consumption recorded successfully')
        return redirect('inventory:user_consumption')
    return render(request, 'inventory/add_user_consumption.html', {'products': Product.objects.all()})

@login_required
def update_user_consumption(request, pk):
    if request.user.is_staff:
        return redirect('inventory:admin_dashboard')
    consumption = get_object_or_404(Consumption, pk=pk, created_by=request.user)
    if request.method == 'POST':
        consumption.product = get_object_or_404(Product, pk=request.POST['product'])
        consumption.amount_used = request.POST['amount_used']
        consumption.description = request.POST.get('description', '')
        consumption.save()
        messages.success(request, 'Consumption updated successfully')
        return redirect('inventory:user_consumption')
    return render(request, 'inventory/update_user_consumption.html', {'consumption': consumption, 'products': Product.objects.all()})

@login_required
def delete_user_consumption(request, pk):
    if request.user.is_staff:
        return redirect('inventory:admin_dashboard')
    consumption = get_object_or_404(Consumption, pk=pk, created_by=request.user)
    if request.method == 'POST':
        consumption.delete()
        messages.success(request, 'Consumption deleted successfully')
        return redirect('inventory:user_consumption')
    return JsonResponse({'success': True})

@login_required
@user_passes_test(is_admin)
def admin_consumption(request):
    admin_consumptions = Consumption.objects.filter(created_by__is_staff=True)
    user_consumptions = Consumption.objects.filter(created_by__is_staff=False)
    total_admin = admin_consumptions.aggregate(Sum('amount_used'))['amount_used__sum'] or 0
    total_user = user_consumptions.aggregate(Sum('amount_used'))['amount_used__sum'] or 0
    total_consumption = total_admin + total_user
    return render(request, 'inventory/admin_consumption.html', {
        'admin_consumptions': admin_consumptions,
        'user_consumptions': user_consumptions,
        'total_admin': total_admin,
        'total_user': total_user,
        'total_consumption': total_consumption,
        'products': Product.objects.all()
    })

@login_required
@user_passes_test(is_admin)
def add_consumption(request):
    if request.method == 'POST':
        product_id = request.POST['product']
        amount_used = request.POST['amount_used']
        description = request.POST.get('description', '')
        product = get_object_or_404(Product, pk=product_id)
        Consumption.objects.create(
            product=product,
            amount_used=amount_used,
            description=description,
            created_by=request.user
        )
        messages.success(request, 'Consumption recorded successfully')
        return redirect('inventory:admin_consumption')
    return render(request, 'inventory/add_admin_consumption.html', {'products': Product.objects.all()})

@login_required
@user_passes_test(is_admin)
def update_consumption(request, pk):
    consumption = get_object_or_404(Consumption, pk=pk)
    if request.method == 'POST':
        consumption.product = get_object_or_404(Product, pk=request.POST['product'])
        consumption.amount_used = request.POST['amount_used']
        consumption.description = request.POST.get('description', '')
        consumption.save()
        messages.success(request, 'Consumption updated successfully')
        return redirect('inventory:admin_consumption')
    return render(request, 'inventory/update_admin_consumption.html', {'consumption': consumption, 'products': Product.objects.all()})

@login_required
@user_passes_test(is_admin)
def delete_consumption(request, pk):
    consumption = get_object_or_404(Consumption, pk=pk)
    if request.method == 'POST':
        consumption.delete()
        messages.success(request, 'Consumption deleted successfully')
        return redirect('inventory:admin_consumption')
    return JsonResponse({'success': True})

@login_required
@user_passes_test(is_admin)
def analysis(request):
    products = Product.objects.all()
    sales = Sale.objects.all()
    total_sales = sales.aggregate(Sum('amount'))['amount__sum'] or 0
    total_invested = products.aggregate(Sum('total_invested'))['total_invested__sum'] or 0
    profit = total_sales - total_invested

    product_analysis = []
    for product in products:
        product_sales = Sale.objects.filter(product=product)
        total_product_sales = product_sales.aggregate(Sum('amount'))['amount__sum'] or 0
        total_quantity_sold = product_sales.aggregate(Sum('quantity_sold'))['quantity_sold__sum'] or 0
        remaining_quantity = product.quantity - total_quantity_sold if total_quantity_sold else product.quantity
        product_profit = total_product_sales - product.total_invested
        product_analysis.append({
            'product': product,
            'total_sales': total_product_sales,
            'quantity_sold': total_quantity_sold,
            'remaining_quantity': remaining_quantity,
            'profit': product_profit
        })

    admin_consumptions = Consumption.objects.filter(created_by__is_staff=True)
    user_consumptions = Consumption.objects.filter(created_by__is_staff=False)
    total_admin_consumption = admin_consumptions.aggregate(Sum('amount_used'))['amount_used__sum'] or 0
    total_user_consumption = user_consumptions.aggregate(Sum('amount_used'))['amount_used__sum'] or 0
    total_consumption = total_admin_consumption + total_user_consumption

    return render(request, 'inventory/analysis.html', {
        'product_analysis': product_analysis,
        'total_sales': total_sales,
        'total_invested': total_invested,
        'profit': profit,
        'total_admin_consumption': total_admin_consumption,
        'total_user_consumption': total_user_consumption,
        'total_consumption': total_consumption,
        'sales': sales
    })





from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def signup(request):
    if request.user.is_authenticated:
        return redirect('inventory:admin_dashboard' if request.user.is_staff else 'inventory:sales')
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('inventory:admin_dashboard' if user.is_staff else 'inventory:sales')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = UserCreationForm()
    return render(request, 'inventory/signup.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('inventory:admin_dashboard' if request.user.is_staff else 'inventory:sales')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in successfully!')
            return redirect('inventory:admin_dashboard' if user.is_staff else 'inventory:sales')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'inventory/login.html')

from django.contrib.auth import logout as auth_logout
def logout_view(request):
    auth_logout(request)
    return redirect("inventory:login_view")
