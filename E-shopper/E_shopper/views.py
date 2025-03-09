from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from app.models import Category,Product,Contact_us,Order,Brand
from  django.contrib.auth import authenticate,login
from app.models import UserCreateForm
from  django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from django.core.paginator import Paginator
# Create your views here.
def Master(request):
    return render(request,'master.html')

def Index(request):
    category = Category.objects.all()
    brand = Brand.objects.all()
    categoryID = request.GET.get('category')
    brandID = request.GET.get('brand')
    price_range = request.GET.get('price_range')
    products = Product.objects.all()

    if categoryID:
        products = products.filter(sub_category=categoryID)
    if brandID:
        products = products.filter(brand=brandID).order_by('-id')
    if price_range:
        min_price, max_price = map(int, price_range.strip('[]').split(','))
        products = products.filter(price__gte=min_price, price__lte=max_price)

    products = products[:15]

    context = {
        'category': category,
        'product': products,
        'brand': brand,
    }
    return render(request, "index.html", context)

def signup(request):
    if request.method=='POST':
        form=UserCreateForm(request.POST)
        if form.is_valid():
            new_user=form.save()
            new_user=authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
            )
            login(request,new_user)
            return redirect('index')
    else:
        form=UserCreateForm()
    context={
        'form':form,
    }
    return render(request,'registration/signup.html',context)


@login_required(login_url="/accounts/login/")
def cart_add(request, product_id):
    product = Product.objects.filter(id=product_id).first()
    size = request.POST.get('size', 'M')  # Default to 'M' if size is not provided
    cart = request.session.get('cart', {})
    cart_item = {
        'product_id': product.id,
        'name': product.name,
        'price': product.price,
        'quantity': 1,
        'size': size,  # Store size in cart
        'image': product.image.url,
    }
    cart[str(product_id)] = cart_item
    request.session['cart'] = cart
    return redirect('cart_detail')


@login_required(login_url="/accounts/login/")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def cart_detail(request):
    return render(request, 'cart/cart_detail.html')

def Contact_Page(request):
    if request.method=='POST':
        contact=Contact_us(
            name=request.POST.get('name'), 
            email=request.POST.get('email'),  
            subject=request.POST.get('subject'), 
            message=request.POST.get('message'), 
        )
        contact.save()

    return render(request,'contact.html')


def checkout(request):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        user = request.user
        for key, value in cart.items():
            order = Order(
                image=value['image'],
                product=value['name'],
                user=user,
                price=value['price'],
                quantity=value['quantity'],
                size=value['size'],  # Store size in order
                total=value['price'] * value['quantity'],
                address=request.POST.get('address'),
                phone=request.POST.get('phone'),
                pincode=request.POST.get('pincode'),
            )
            order.save()
        # Clear the cart after checkout
        request.session['cart'] = {}
        return redirect('order')


def Your_Order(request):
    uid=request.session.get('_auth_user_id')
    user=User.objects.get(id=uid)

    order=Order.objects.filter(user = user)
    context={
        'order':order,
    }

    return render(request,'order.html',context)


def Product_page(request):
    category = Category.objects.all()
    brand = Brand.objects.all()
    categoryID = request.GET.get('category')
    brandID = request.GET.get('brand')
    price_range = request.GET.get('price_range')
    products = Product.objects.all()

    if categoryID:
        products = products.filter(sub_category=categoryID)
    if brandID:
        products = products.filter(brand=brandID).order_by('-id')
    if price_range:
        min_price, max_price = map(int, price_range.strip('[]').split(','))
        products = products.filter(price__gte=min_price, price__lte=max_price)

    # Pagination
    paginator = Paginator(products, 15)  # Show 15 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'category': category,
        'brand': brand,
        'product': page_obj,  # Pass the page object to the template
    }
    return render(request, 'product.html', context)

def Product_detail(request, id):
    product=Product.objects.filter(id=id).first()
    sizes = Product.SIZE_CHOICES
    context = {
        'product': product,
        'sizes': sizes,
    }
    return render(request, 'product_detail.html', context)


def Search(request):
    query=request.GET.get('query')
    product=Product.objects.filter(name__icontains=query)
    context={
        'product':product,

    }
    return render(request,'search.html',context)


def delete_order(request, order_id):
    uid = request.session.get('_auth_user_id')
    user = User.objects.get(id=uid)

    order = Order.objects.filter(id=order_id, user=user)
    order.delete()

    return redirect('order')



def checkout(request):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        user = request.user
        for key, value in cart.items():
            order = Order(
                image=value['image'],
                product=value['name'],
                user=user,
                price=value['price'],
                quantity=value['quantity'],
                size=value['size'],  # Store size in order
                total=value['price'] * value['quantity'],
                address=request.POST.get('address'),
                phone=request.POST.get('phone'),
                pincode=request.POST.get('pincode'),
            )
            order.save()
        # Clear the cart after checkout
        request.session['cart'] = {}
        return redirect('order')
    return redirect('cart')