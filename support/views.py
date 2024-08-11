# views.py

from django.shortcuts import render, redirect, get_object_or_404
from .models import SupportTicket
from .forms import SupportTicketForm,SupportTicketFormTeam,CreateSupportTicketForm
from django.contrib.auth.decorators import login_required
from accounts.decorators import allowed_users, admin_only
@login_required
@allowed_users(allowed_roles=['Support'])
def ticket_list(request):
   
    open_tickets = SupportTicket.objects.filter(status='Open')
    closed_tickets = SupportTicket.objects.filter(status='Closed')
    in_progress_tickets = SupportTicket.objects.filter(status='In Progress')
    
    context = {
        'open_tickets': open_tickets,
        'closed_tickets': closed_tickets,
        'in_progress_tickets': in_progress_tickets,
    }
    return render(request, 'support/ticket_list.html', context)

def ticket_detail(request, pk):
    ticket = get_object_or_404(SupportTicket, pk=pk)
    return render(request, 'support/ticket_detail.html', {'ticket': ticket})

def ticket_create(request):
    if request.method == 'POST':
        form = CreateSupportTicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user  # Assuming you are using Django's authentication
            ticket.save()
            return redirect('support:ticket_detail', pk=ticket.pk)
    else:
        form = CreateSupportTicketForm()
    return render(request, 'support/ticket_form.html', {'form': form})

def ticket_edit(request, pk):
    ticket = get_object_or_404(SupportTicket, pk=pk)
    if request.method == 'POST':
        form = SupportTicketFormTeam(request.POST, instance=ticket)
        if form.is_valid():
            ticket = form.save()
            return redirect('support:ticket_detail', pk=ticket.pk)
    else:
        form = SupportTicketFormTeam(instance=ticket)
    return render(request, 'support/ticket_form.html', {'form': form})

def ticket_delete(request, pk):
    ticket = get_object_or_404(SupportTicket, pk=pk)
    if request.method == 'POST':
        ticket.delete()
        return redirect('support:ticket_list')
    return render(request, 'support/ticket_confirm_delete.html', {'ticket': ticket})

def ticket_assign(request, pk):
    ticket = get_object_or_404(SupportTicket, pk=pk)
    if request.method == 'POST':
        user = request.POST.get('assigned_to')  # Assuming you have a form field to select user
        ticket.assigned_to_id = user
        ticket.save()
        return redirect('support:ticket_detail', pk=ticket.pk)
    return render(request, 'support/ticket_assign.html', {'ticket': ticket})
''''
def ticket_dashboard(request):
    open_tickets = SupportTicket.objects.filter(status='Open')
    closed_tickets = SupportTicket.objects.filter(status='Closed')
    in_progress_tickets = SupportTicket.objects.filter(status='In Progress')
    
    context = {
        'open_tickets': open_tickets,
        'closed_tickets': closed_tickets,
        'in_progress_tickets': in_progress_tickets,
    }
    return render(request, 'support/ticket_dashboard.html', context)'''