from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, Category
from .forms import ProductForm


def product_list(request):
    products = Product.objects.all()
    return render(request, "products/product_list.html", {"products": products})


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, "products/product_detail.html", {"product": product})


@login_required
def create_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("product-list")
    else:
        form = ProductForm()
    return render(request, "products/product_form.html", {"form": form})
@login_required
def update_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect("product-list")
    else:
        form = ProductForm(instance=product)
    return render(request, "products/product_form.html", {"form": form})


@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        product.delete()
        return redirect("product-list")
    return render(request, "products/product_confirm_delete.html", {"product": product})


def storefront(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    brands = Product.objects.values_list('brand', flat=True).distinct()
    query = request.GET.get("q")
    category_filter = request.GET.get("category")
    brand_filter = request.GET.getlist("brand")
    sort_filter = request.GET.get("sort")

    if query:
        products = products.filter(name__icontains=query)

    if category_filter:
        products = products.filter(category__id=category_filter)

    if brand_filter:
        products = products.filter(brand__in=brand_filter)

    if sort_filter == "popular":
        products = products.order_by("-id")
    elif sort_filter == "newest":
        products = products.order_by("-created_at")
    elif sort_filter == "price_asc":
        products = products.order_by("price")
    elif sort_filter == "price_desc":
        products = products.order_by("-price")

    return render(request, "storefront/home.html", {
        "products": products,
        "categories": categories,
        "brands": brands,
        "query": query,
        "selected_category": category_filter,
        "selected_brands": brand_filter,
        "selected_sort": sort_filter,
    })
