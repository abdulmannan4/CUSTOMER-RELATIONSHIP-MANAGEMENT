# views.py

from django.shortcuts import render
from .models import Sale
from .forms import SaleForm,CreateSaleForm,SaleFormTeam
from django.db.models import Count
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from accounts.decorators import allowed_users, admin_only
def sale_list(request):
    sales = Sale.objects.all()
    return render(request, 'sales/sale_list.html', {'sales': sales})

def edit_sale(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    if request.method == 'POST':
        form = SaleFormTeam(request.POST, instance=sale)
        if form.is_valid():
            form.save()
            return redirect('sales:sale_detail', pk=sale.pk)
    else:
        form = SaleFormTeam(instance=sale)
    return render(request, 'sales/edit_sale.html', {'form': form, 'sale': sale})
def sale_detail(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    return render(request, 'sales/sale_detail.html', {'sale': sale})
def sale_create(request):
    if request.method == 'POST':
        form = CreateSaleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sales:sale_list')
    else:
        form = CreateSaleForm()
    return render(request, 'sales/sale_form.html', {'form': form})

def sale_update(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    if request.method == 'POST':
        form = SaleFormTeam(request.POST, instance=sale)
        if form.is_valid():
            form.save()
            return redirect('sales:sale_list')
    else:
        form = SaleFormTeam(instance=sale)
    return render(request, 'sales/sale_form.html', {'form': form})

def sale_delete(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    if request.method == 'POST':
        sale.delete()
        return redirect('sale_list')
    return render(request, 'sales/sale_confirm_delete.html', {'sale': sale})

@login_required
@allowed_users(allowed_roles=['Sales'])
def sales_dashboard(request):
    # Example: Aggregate sales count by stage
    stage_counts = Sale.objects.values('stage').annotate(total=Count('id'))
    
    # Example: Aggregate sales count by assigned_to
    assigned_to_counts = Sale.objects.values('assigned_to__username').annotate(total=Count('id'))
    
    context = {
        'stage_counts': stage_counts,
        'assigned_to_counts': assigned_to_counts,
    }
    
    return render(request, 'sales/dashboard.html', context)