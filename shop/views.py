from django.shortcuts import render,redirect
from data.models import Product,Categories,Filter_Price,Brand,Contact,Order,OrderItem
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from django.urls import reverse
import razorpay
from django.views.decorators.csrf import csrf_exempt


client = razorpay.Client(auth=(settings.RAZORAY_KEY_ID,settings.RAZORAY_KEY_SECRECT))

def BASE(request):
    return render(request,'data/base.html')

def INDEX(request):
    product = Product.objects.all()
    context = {
        'product':product,
    }
    return render(request,'data/index.html',context)

def PRODUCT(request):
    product = Product.objects.all()

    categories = Categories.objects.all()
    filter_price = Filter_Price.objects.all()
    brand = Brand.objects.all()

    CATID = request.GET.get('categories')
    PRICE_FILTER_ID = request.GET.get('filter_price')
    BRANDID = request.GET.get('brand')
    PRICE_LOWTOHIGHID = request.GET.get('PRICE_LOWTOHIGH')
    PRICE_HIGHTOLOWID = request.GET.get('PRICE_HIGHTOLOW')
    
    if CATID:
        product = Product.objects.filter(categories=CATID,status='Publish')
        

    elif PRICE_FILTER_ID:
        product = Product.objects.filter(filter_price= PRICE_FILTER_ID,status='Publish')


    elif BRANDID:
        product = Product.objects.filter(brand=BRANDID,status='Publish')
        
       
       

    elif PRICE_LOWTOHIGHID:
        product = Product.objects.filter(status='Publish').order_by('price') 
       
        

    
    elif PRICE_HIGHTOLOWID:
        product = Product.objects.filter(status='Publish').order_by('-price')
          
      

    else:
        product = Product.objects.filter(status='Publish')
    


    context = {
        'product':product,
        
        'categories':categories,
        'filter_price':filter_price,
        'brand':brand,
    }
    return render(request,'data/product.html',context)

    
def SEARCH(request):
    query = request.GET.get('Query')
    product = Product.objects.filter(name__icontains = query)

    context = {
        'product':product
    }
    return render(request,'data/search.html',context)


def PRODUCT_DETAIL_PAGE(request,id):
    prod = Product.objects.filter(id=id).first()
   
   

    context = {
        'prod':prod,
       
    }
    return render(request,'data/singleproduct.html',context)    


def CONTACT(request):
    if request.method == 'POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        subject=request.POST.get('subject')
        message=request.POST.get('message')

        contact =Contact(
            name=name,
            email=email,
            subject=subject,
            message=message,
        )

        subject=subject
        message=message
        email_from = settings.EMAIL_HOST_USER
        try:
            send_mail (subject,message,email_from,['pranayjungade19@gmail.com'])
            contact.save()
            return redirect('index')
        except:            
            return redirect('contact')    
        

    return render(request,'data/contact.html')   

def HandelRegister(request):
    if request.method =='POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        customer = User.objects.create_user(username,email,password)
        customer.first_name = first_name 
        customer.last_name = last_name 
        customer.save()
        return redirect('register')
        
    return render(request,'Register/auth.html')   


def HandelLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('index')
        else:
            return redirect('login')    
    return render(request,'Register/auth.html') 

def HandelLogout(request):
    logout(request)

    return redirect('index')    






@login_required(login_url="/login/")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("index")


@login_required(login_url="/login/")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart")


@login_required(login_url="/login/")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart")


@login_required(login_url="/login/")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart")


@login_required(login_url="/login/")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart")


@login_required(login_url="/login/")
def cart(request):
    return render(request, 'cart/cartdetails.html')       

def CHECKOUT(request):
    payment = client.order.create({
        'amount':500,
        'currency':'INR',
        'payment_capture':'1',
        })
    order_id = payment['id']
    context = {
        'order_id':order_id,
        'payment':payment,        
    }

    return render(request,'cart/checkout.html',context)    

def PLACEORDER(request):
    if request.method == 'POST':
        uid = request.session.get('_auth_user_id')
        user = User.objects.get(id=uid)
        cart = request.session.get('cart')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        country = request.POST.get('country')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postcode = request.POST.get('postcode')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        amount = request.POST.get('amount')
        order_id = request.POST.get('order_id')
        payment = request.POST.get('payment')

        context = {
            'order_id':order_id,
        }

        order = Order (
            user = user,
            firstname = firstname,
            lastname = lastname,
            country = country,
            address = address,
            city = city,
            state = state,
            postcode = postcode,
            phone = phone,
            email = email,
            payment_id = order_id,
            amount = amount,
        )
        order.save()


        for i in  cart:
            a = (int(cart[i]['price']))
            b = cart[i]['quantity']

            total = a*b

            item = OrderItem (
                order = order,
                product = cart[i]['name'],
                image = cart[i]['image'],
                quantity = cart[i]['quantity'],
                price = cart[i]['price'],
                total = total
            )
            item.save()

        return render(request,'cart/placeorder.html',context)

def MEANSWEAR(request):
    return render(request,'data/meanswear.html')

@csrf_exempt
def SUCCESS(request):
    if request.method == 'POST':
        a = request.POST
        order_id = ""
        for key, val in a.items():
            if key == 'razorpay_order_id':
                order_id = val
                break
        user = Order.objects.filter(payment_id=order_id).first()
        user.paid = True
        user.save()

    return render(request, 'cart/thank-you.html')    