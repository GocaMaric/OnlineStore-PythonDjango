from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from .forms import NewItemForm, EditItemForm
from .models import Item, Category

def paginate_query(request, queryset, per_page=10):
    paginator = Paginator(queryset, per_page)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)

@login_required
def items(request):
    query = request.GET.get('query', '')
    category_id = request.GET.get('category', 0)
    categories = Category.objects.all()
    items_query = Item.objects.filter(is_sold=False)

    if category_id:
        items_query = items_query.filter(category_id=category_id)

    if query:
        items_query = items_query.filter(Q(name__icontains=query) | Q(description__icontains=query))

    items_paged = paginate_query(request, items_query)

    return render(request, 'item/items.html', {
        'items': items_paged,
        'query': query,
        'categories': categories,
        'category_id': int(category_id)
    })

@login_required
def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(pk=pk)[:3]

    return render(request, 'item/detail.html', {
        'item': item,
        'related_items': related_items
    })

@login_required
def new(request):
    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES)

        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()
            messages.success(request, 'Item created successfully.')
            return redirect('item:detail', pk=item.id)
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = NewItemForm()

    return render(request, 'item/form.html', {
        'form': form,
        'title': 'New item',
    })

@login_required
def edit(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    if request.method == 'POST':
        form = EditItemForm(request.POST, request.FILES, instance=item)

        if form.is_valid():
            form.save()
            messages.success(request, 'Item updated successfully.')
            return redirect('item:detail', pk=item.id)
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = EditItemForm(instance=item)

    return render(request, 'item/form.html', {
        'form': form,
        'title': 'Edit item',
    })

@login_required
def delete(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Item deleted successfully.')
        return redirect('dashboard:index')
    return render(request, 'item/confirm_delete.html', {'item': item})
