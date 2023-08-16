from django.shortcuts import render
# Create your views here.
from app.models import *
from app.forms import *

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login,logout
from django.shortcuts import render, redirect
from django.http import HttpResponse

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)  # Create an instance of UserCreationForm
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user, address='')

            # Log the user in
            login(request, user)
            return redirect('user_loggedin')
        else:
            HttpResponse("not a valid data")
    else:
        form = UserCreationForm()  # Create an instance of UserCreationForm

    return render(request, 'register.html', {'form': form})


def user_loggedin(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('user_profile')  # Redirect to the user's profile page or any other page
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


@login_required
def user_profile(request):

    user_profile = request.user.userprofile
    categories = Category.objects.all() 
    return render(request, 'user_profile.html', {'user_profile': user_profile, 'editing_profile': False,'categories': categories})



@login_required
def user_profile_edit(request):
    user_profile = request.user.userprofile
    user_form = UserForm(instance=request.user)
    profile_form = UserProfileForm(instance=user_profile)
    
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, instance=user_profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('user_profile')
    
    return render(request, 'user_profile.html', {'user_profile': user_profile, 'user_form': user_form, 'profile_form': profile_form, 'editing_profile': True})




def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})



def product_list(request, category_id=None):
    categories = Category.objects.all()
    products = Product.objects.all()
    
    if category_id:
        category = get_object_or_404(Category, id=category_id)
        products = products.filter(category=category)
        pc=0
        for i in products:
            pc+=1


        print("the value is ",pc)

    return render(request, 'product_list.html', {'products': products, 'categories': categories,"pc":pc})



def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    reviews = Review.objects.filter(product=product)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            Review.objects.create(product=product, user=request.user, text=text)
            return redirect('product_detail', product_id=product_id)
    else:
        form = ReviewForm()
    
    return render(request, 'product_detail.html', {'product': product, 'reviews': reviews, 'form': form})

@login_required
def cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_amount=0
    quantity=0
    for i in cart_items:
        quantity+=1
        amount=i.product.price
        total_amount+=amount


    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        qua = int(request.POST.get('quantity', 1))
        
        Cart.objects.create(user=request.user, product=product)

        return HttpResponse("Item added into cart")
    d= {'cart_items': cart_items,'total_amount':total_amount,'quantity':quantity}
    return render(request, 'cart.html',d)
@login_required
def checkout(request):
    user = request.user
    cart_items = Cart.objects.filter(user=user)
    total_amount = sum(item.product.price for item in cart_items)
    quantity = cart_items.count()

    if request.method == 'POST':
        # Perform the checkout process (e.g., create an order)
        order = Order.objects.create(user=user, total_amount=total_amount)
        for cart_item in cart_items:
            OrderItem.objects.create(order=order, product=cart_item.product, quantity=quantity)

            product = cart_item.product
            product.count -= quantity
            product.save()
        cart_items.delete()
        
        return HttpResponse('order placed successfully')
    d={'cart_items': cart_items, 'total_amount': total_amount, 'quantity': quantity}
    return render(request, 'checkout.html',)

@login_required
def user_logout(request):
    logout(request)
    return redirect('user_loggedin') 

@login_required
def myorders(request):
    user = request.user
    orders = Order.objects.filter(user=user)
    
    return render(request, 'myorders.html', {'orders': orders})


def home(request):

    return redirect('register')