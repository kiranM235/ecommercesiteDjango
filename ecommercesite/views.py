from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from .models import User
from django.http import HttpResponse, JsonResponse
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views import View
from .models import Customer, Product, Cart, OrderPlaced
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.db.models import Q
from django.utils.decorators import method_decorator

class ProductView(View):
 def get(self, request):
  totalitem = 0
  menzsummerbottomwears = Product.objects.filter(category='MSBW')
  mobiles = Product.objects.filter(category='M')
  laptops = Product.objects.filter(category='L')
  menzsummertopwears = Product.objects.filter(category='MSTW')
  if request.user.is_authenticated:
    totalitem = len(Cart.objects.filter(user=request.user))
  return render(request, 'home.html', 
  {'menzsummerbottomwears':menzsummerbottomwears, 'mobiles':mobiles, 
  'laptops':laptops, 'menzsummertopwears':menzsummertopwears, 'totalitem':totalitem})
#def home(request):
    #if request.method == "POST":
        #email = request.POST['email']
          
        #return render(request, 'home.html', {'email': email})
    
    #else:
        #return render(request, 'home.html', {})

class ProductDetailView(View):
 def get(self, request, pk):
  totalitem = 0
  product = Product.objects.get(pk=pk)
  item_already_in_cart = False
  if request.user.is_authenticated:
    totalitem = len(Cart.objects.filter(user=request.user))
    item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
  return render(request, 'productdetail.html', {'product':product, 'item_already_in_cart':item_already_in_cart, 'totalitem':totalitem})

def categories(request):
    return render(request, 'category.html', {})
    
def product_list(request):
    return render(request, 'product_list.html', {})
    
def contact(request):
    if request.method == "POST":
        message_name = request.POST['message-name']
        message_email = request.POST['message-email']
        message = request.POST['message']

        # send an email
        send_mail(
            message_name, #subject
            message, # message
            message_email, # from email
            ['kiranmaharjan1989@gmail.com', 'kiranmaharjan89@gmail.com'], # To Email
            )
        return render(request, 'contact.html', {'message_name': message_name})
    else:
        return render(request, 'contact.html', {}) 

def blog(request):
    return render(request, 'blog.html')
    context = {}

def single_blog(request):
    return render(request, 'single-blog.html')
    context = {}

@login_required
def address(request):
 add = Customer.objects.filter(user=request.user)
 return render(request, 'address.html', {'add':add, 'active':'btn-primary'})

@login_required
def orders(request):
  op = OrderPlaced.objects.filter(user=request.user)
  return render(request, 'orders.html', {'order_placed':op})

def elements(request):
    return render(request, 'elements.html', {})
    

def about(request):
   if request.method == "POST":
      email = request.POST['email']
          
      return render(request, 'about.html', {'email': email})
    
   else:
        return render(request, 'about.html', {})
  
    

def confirmation(request):
    return render(request, 'confirmation.html', {})
    

def cart(request):
    return render(request, 'cart.html', {})
    
@login_required
def checkout(request):
  user = request.user
  add = Customer.objects.filter(user=user)
  cart_items = Cart.objects.filter(user=user)
  amount = 0.0
  shipping_amount = 120.0
  totalamount = 0.0
  cart_product = [p for p in Cart.objects.all() if p.user == 
  request.user]
  if cart_product: 
    for p in cart_product:
      tempamount = (p.quantity * p.product.discounted_price)
      amount += tempamount
      totalamount = amount + shipping_amount
  return render(request, 'checkout.html', {'add':add, 
  'totalamount':totalamount, 'cart_items':cart_items})

@login_required   
def payment_done(request):
  user = request.user
  custid = request.GET.get('custid')
  customer = Customer.objects.get(id=custid)
  cart = Cart.objects.filter(user=user)
  for c in cart:
    OrderPlaced(user=user, customer=customer, product=c.
    product, quantity=c.quantity).save()
    c.delete()
  return redirect("orders")

class CustomerRegistrationView(View):
 def get(self, request):
  form = CustomerRegistrationForm()
  return render(request, 'signup.html', 
  {'form':form})
 def post(self, request):
  form = CustomerRegistrationForm(request.POST)
  if form.is_valid():
   messages.success(request, 'Congratulations!! Registered Successfully')
   form.save()
  return render(request, 'signup.html', 
  {'form':form})
    
def account(request):
    return render(request, 'account.html')

def mobile(request, data=None):
 if data == None:
  mobiles = Product.objects.filter(category='M')
 elif data == 'Redmi' or data == 'Samsung':
  mobiles = Product.objects.filter(category='M').filter(brand=data)
 elif data == 'below':
  mobiles = Product.objects.filter(category='M').filter(discounted_price__lt=20000)
 elif data == 'above':
  mobiles = Product.objects.filter(category='M').filter(discounted_price__gt=20000)
 return render(request, 'mobile.html', {'mobiles':mobiles})

def fridge(request, data=None):
 if data == None:
  fridges = Product.objects.filter(category='F')
 elif data == 'LG' or data == 'Whirlpool':
  fridges = Product.objects.filter(category='F').filter(brand=data)
 elif data == 'below':
  fridges = Product.objects.filter(category='F').filter(discounted_price__lt=40000)
 elif data == 'above':
  fridges = Product.objects.filter(category='F').filter(discounted_price__gt=40000)
 return render(request, 'fridge.html', {'fridges':fridges})

def washingmachine(request, data=None):
 if data == None:
  washingmachines = Product.objects.filter(category='WM')
 elif data == 'LG' or data == 'Whirlpool':
  washingmachines = Product.objects.filter(category='WM').filter(brand=data)
 elif data == 'below':
  washingmachines = Product.objects.filter(category='WM').filter(discounted_price__lt=40000)
 elif data == 'above':
  washingmachines = Product.objects.filter(category='WM').filter(discounted_price__gt=40000)
 return render(request, 'washingmachine.html', {'washingmachines':washingmachines})

def television(request, data=None):
 if data == None:
  televisions = Product.objects.filter(category='TV')
 elif data == 'Samsung' or data == 'Sony':
  televisions = Product.objects.filter(category='TV').filter(brand=data)
 elif data == 'below':
  televisions = Product.objects.filter(category='TV').filter(discounted_price__lt=40000)
 elif data == 'above':
  televisions = Product.objects.filter(category='TV').filter(discounted_price__gt=40000)
 return render(request, 'television.html', {'televisions':televisions})

def treadmill(request, data=None):
 if data == None:
  treadmills = Product.objects.filter(category='T')
 elif data == 'Nordictrack' or data == 'Precor':
  treadmills = Product.objects.filter(category='T').filter(brand=data)
 elif data == 'below':
  treadmills = Product.objects.filter(category='T').filter(discounted_price__lt=70000)
 elif data == 'above':
  treadmills = Product.objects.filter(category='T').filter(discounted_price__gt=70000)
 return render(request, 'treadmill.html', {'treadmills':treadmills})


def laptop(request, data=None):
 if data == None:
  laptops = Product.objects.filter(category='L')
 elif data == 'Dell' or data == 'Acer':
  laptops = Product.objects.filter(category='L').filter(brand=data)
 elif data == 'below':
  laptops = Product.objects.filter(category='L').filter(discounted_price__lt=100000)
 elif data == 'above':
  laptops = Product.objects.filter(category='L').filter(discounted_price__gt=100000)
 return render(request, 'laptop.html', {'laptops':laptops})

def menzsummerbottomwear(request, data=None):
 if data == None:
  menzsummerbottomwears = Product.objects.filter(category='MSBW')
 elif data == 'Levis' or data == 'Adidas':
  menzsummerbottomwears = Product.objects.filter(category='MSBW').filter(brand=data)
 elif data == 'below':
  menzsummerbottomwears = Product.objects.filter(category='MSBW').filter(discounted_price__lt=3000)
 elif data == 'above':
  menzsummerbottomwears = Product.objects.filter(category='MSBW').filter(discounted_price__gt=3000)
 return render(request, 'menzsummerbottomwear.html', {'menzsummerbottomwears':menzsummerbottomwears})

def menzsummertopwear(request, data=None):
 if data == None:
  menzsummertopwears = Product.objects.filter(category='MSTW')
 elif data == 'Levis' or data == 'Adidas':
  menzsummertopwears = Product.objects.filter(category='MSTW').filter(brand=data)
 elif data == 'below':
  menzsummertopwears = Product.objects.filter(category='MSTW').filter(discounted_price__lt=650)
 elif data == 'above':
  menzsummertopwears = Product.objects.filter(category='MSTW').filter(discounted_price__gt=650)
 return render(request, 'menzsummertopwear.html', {'menzsummertopwears':menzsummertopwears})

def dumbbell(request, data=None):
 if data == None:
  dumbbells = Product.objects.filter(category='DB')
 elif data == 'Arora' or data == 'Hex':
  dumbbells = Product.objects.filter(category='DB').filter(brand=data)
 elif data == 'below':
  dumbbells = Product.objects.filter(category='DB').filter(discounted_price__lt=700)
 elif data == 'above':
  dumbbells = Product.objects.filter(category='DB').filter(discounted_price__gt=700)
 return render(request, 'dumbbell.html', {'dumbbells':dumbbells})

@login_required
def add_to_cart(request):
 user=request.user
 product_id = request.GET.get('prod_id')
 product = Product.objects.get(id=product_id)
 Cart(user=user, product=product).save()
 return redirect('/cart')

@login_required
def show_cart(request):
  totalitem = 0
  if request.user.is_authenticated:
    totalitem = len(Cart.objects.filter(user=request.user))
    user = request.user
    cart = Cart.objects.filter(user=user)
    #print(cart)
    amount = 0.0
    shipping_amount = 120.0
    total_amount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == 
    user]
    #print(cart_product)
    if cart_product: 
      for p in cart_product:
        tempamount = (p.quantity * p.product.discounted_price)
        amount += tempamount
        totalamount = amount + shipping_amount
      return render(request, 'addtocart.html', {'carts':cart, 'totalamount':totalamount, 'amount':amount, 'totalitem':totalitem})
    else:
      return render(request, 'emptycart.html', {'totalitem':totalitem})

def plus_cart(request):
  if request.method == 'GET':
    prod_id = request.GET['prod_id']
    print(prod_id)
    c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
    c.quantity+=1
    c.save()
    amount = 0.0
    shipping_amount = 120.0
    cart_product = [p for p in Cart.objects.all() if p.user == 
    request.user]
    for p in cart_product:
      tempamount = (p.quantity * p.product.discounted_price)
      amount += tempamount 

    data = {
      'quantity': c.quantity,
      'amount': amount,
      'totalamount': amount + shipping_amount
      }
    return JsonResponse(data)

def minus_cart(request):
  if request.method == 'GET':
    prod_id = request.GET['prod_id']
    print(prod_id)
    c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
    c.quantity-=1
    c.save()
    amount = 0.0
    shipping_amount = 120.0
    cart_product = [p for p in Cart.objects.all() if p.user == 
    request.user]
    for p in cart_product:
      tempamount = (p.quantity * p.product.discounted_price)
      amount += tempamount 

    data = {
      'quantity': c.quantity,
      'amount': amount,
      'totalamount': amount + shipping_amount
      }
    return JsonResponse(data)

def remove_cart(request):
  if request.method == 'GET':
    prod_id = request.GET['prod_id']
    c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
    c.delete()
    amount = 0.0
    shipping_amount = 120.0
    cart_product = [p for p in Cart.objects.all() if p.user == 
    request.user]
    for p in cart_product:
      tempamount = (p.quantity * p.product.discounted_price)
      amount += tempamount 

    data = {
      'amount': amount,
      'totalamount': amount + shipping_amount
      }
    return JsonResponse(data)
        
def buy_now(request):
    return render(request, 'buynow.html')

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
  def get(self, request):
    form = CustomerProfileForm()
    return render(request, 'profile.html', {'form':form, 
    'active':'btn-primary'})

  def post(self, request):
    form = CustomerProfileForm(request.POST)
    if form.is_valid():
      user = request.user
      name = form.cleaned_data['name']
      locality = form.cleaned_data['locality']
      city = form.cleaned_data['city']
      state = form.cleaned_data['state']
      zipcode = form.cleaned_data['zipcode']
      reg = Customer(user=user, name=name, locality=locality, city=city, state=state, zipcode=zipcode)
      reg.save()
      messages.success(request, 'Congratulations!! Profile Updated Successfully')
    return render(request, 'profile.html', {'form':form,
    'active':'btn-primary'})

def electronics(request, data=None):
 if data == None:
  mobiles = Product.objects.filter(category='M')
 elif data == 'Redmi' or data == 'Samsung':
  mobiles = Product.objects.filter(category='M').filter(brand=data)
 elif data == 'below':
  mobiles = Product.objects.filter(category='M').filter(discounted_price__lt=20000)
 elif data == 'above':
  mobiles = Product.objects.filter(category='M').filter(discounted_price__gt=20000)
 if data == None:
  laptops = Product.objects.filter(category='L')
 elif data == 'Dell' or data == 'Acer':
  laptops = Product.objects.filter(category='L').filter(brand=data)
 elif data == 'below':
  laptops = Product.objects.filter(category='L').filter(discounted_price__lt=100000)
 elif data == 'above':
  laptops = Product.objects.filter(category='L').filter(discounted_price__gt=100000)
 return render(request, 'electronics.html', {'mobiles':mobiles, 'laptops':laptops})

def fashion(request, data=None):
 if data == None:
  menzsummerbottomwears = Product.objects.filter(category='MSBW')
 elif data == 'Levis' or data == 'Adidas':
  menzsummerbottomwears = Product.objects.filter(category='MSBW').filter(brand=data)
 elif data == 'below':
  menzsummerbottomwears = Product.objects.filter(category='MSBW').filter(discounted_price__lt=3000)
 elif data == 'above':
  menzsummerbottomwears = Product.objects.filter(category='MSBW').filter(discounted_price__gt=3000)
 if data == None:
  menzsummertopwears = Product.objects.filter(category='MSTW')
 elif data == 'Levis' or data == 'Adidas':
  menzsummertopwears = Product.objects.filter(category='MSTW').filter(brand=data)
 elif data == 'below':
  menzsummertopwears = Product.objects.filter(category='MSTW').filter(discounted_price__lt=650)
 elif data == 'above':
  menzsummertopwears = Product.objects.filter(category='MSTW').filter(discounted_price__gt=650)
 return render(request, 'fashion.html', {'menzsummerbottomwears':menzsummerbottomwears, 'menzsummertopwears':menzsummertopwears})

def homeappliances(request, data=None):
 if data == None:
  fridges = Product.objects.filter(category='F')
 elif data == 'LG' or data == 'Whirlpool':
  fridges = Product.objects.filter(category='F').filter(brand=data)
 elif data == 'below':
  fridges = Product.objects.filter(category='F').filter(discounted_price__lt=40000)
 elif data == 'above':
  fridges = Product.objects.filter(category='F').filter(discounted_price__gt=40000)
 if data == None:
  washingmachines = Product.objects.filter(category='WM')
 elif data == 'LG' or data == 'Whirlpool':
  washingmachines = Product.objects.filter(category='WM').filter(brand=data)
 elif data == 'below':
  washingmachines = Product.objects.filter(category='WM').filter(discounted_price__lt=50000)
 elif data == 'above':
  washingmachines = Product.objects.filter(category='WM').filter(discounted_price__gt=50000)
 if data == None:
  televisions = Product.objects.filter(category='TV')
 elif data == 'Samsung' or data == 'Sony':
  televisions = Product.objects.filter(category='TV').filter(brand=data)
 elif data == 'below':
  televisions = Product.objects.filter(category='TV').filter(discounted_price__lt=25000)
 elif data == 'above':
  televisions = Product.objects.filter(category='TV').filter(discounted_price__gt=25000)
 return render(request, 'homeappliances.html', {'fridges':fridges, 'washingmachines':washingmachines, 'televisions':televisions})

def fitness(request, data=None):
 if data == None:
  treadmills = Product.objects.filter(category='T')
 elif data == 'Levis' or data == 'Adidas':
  treadmills = Product.objects.filter(category='T').filter(brand=data)
 elif data == 'below':
  treadmills = Product.objects.filter(category='T').filter(discounted_price__lt=100000)
 elif data == 'above':
  treadmills = Product.objects.filter(category='T').filter(discounted_price__gt=100000)
 if data == None:
  dumbbells = Product.objects.filter(category='DB')
 elif data == 'Arora' or data == 'Hex':
  dumbbells = Product.objects.filter(category='DB').filter(brand=data)
 elif data == 'below':
  dumbbells = Product.objects.filter(category='DB').filter(discounted_price__lt=700)
 elif data == 'above':
  dumbbells = Product.objects.filter(category='DB').filter(discounted_price__gt=700)
 return render(request, 'fitness.html', {'treadmills':treadmills, 'dumbbells':dumbbells})