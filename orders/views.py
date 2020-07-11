from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Max, Sum
from .models import regularPizza, sicilianPizza, toppings, subs, pasta, dinnerPlatters, order, order_items, categories, salad

def index(request):
            return render(request,"orders/index.html")

#route for logged in users to order
def order_route(request, category):
    if request.user.is_authenticated:
        menu_items, columns = categoryMenu(category)
        context = {
        "current_category": category,
        "menu_items": menu_items,
        "categories": categories.objects.all(),
        "columns": columns
        }
        return render(request,"orders/order.html", context)

#function to run database queries based on category
def categoryMenu(category):
    if category == 'Regular Pizza':
        menu_items =  regularPizza.objects.all()
        numCol = 3
    elif category == 'Sicilian Pizza':
        menu_items = sicilianPizza.objects.all()
        numCol = 3
    elif category == 'Toppings':
        menu_items = toppings.objects.all()
        numCol = 1
    elif category == 'Subs':
        menu_items = subs.objects.all()
        numCol=3
    elif category == 'Pasta':
        menu_items = pasta.objects.all()
        numCol = 2
    elif category == 'Salad':
        menu_items = salad.objects.all()
        numCol = 2
    else:
        menu_items = dinnerPlatters.objects.all()
        numCol = 3
    return menu_items, numCol

#route for adding items to user's cart
def add(request, category, name, price):
    menu_items, columns = categoryMenu(category)
    #get the user's current order
    orderNum = order.objects.get(user=request.user, status="initialized").order_number
    currentOrder = order.objects.get(user=request.user, order_number = orderNum)
    toppings = 0

#set topping allowance if user has added a pizza with additional toppings
    if(category == "Regular Pizza" or category == "Sicilian Pizza"):
        if name == "1 topping":
            toppings = 1
            currentOrder.toppingAllowance += 1
            currentOrder.save()
        elif name == "2 toppings":
            toppings = 2
            currentOrder.toppingAllowance += 2
            currentOrder.save()
        elif name == "3 toppings":
            toppings = 3
            currentOrder.toppingAllowance += 3
            currentOrder.save()
        elif name == "Special":
            currentOrder.toppingAllowance = 19
            currentOrder.save()

    #alert to confirm that the item was successfully added to cart
    alertMessage = name + " " + category + " has been added to your cart!"

    context = {
            "current_category": category,
            "menu_items": menu_items,
            "categories": categories.objects.all(),
            "columns": columns,
            "alertMessage": alertMessage,
            "toppings": toppings
            }

    #if the current category is subs, add validation to ensure that sub extras are only added with a valid sub (i.e. mushrooms, green peppers and onions require a steak + cheese sub)
    if category == "Subs":
        orderSubs = order_items.objects.filter(order=currentOrder)

        if name[0] == "+" and orderSubs.filter(name = "Steak + Cheese").exists() == False:
            context["alertMessage"] = "Error: You must order a Steak + Cheese sub to add Mushrooms, Green Peppers or Onions. Please try again."
            return render(request, "orders/order.html", context)
        elif name == "Extra Cheese" and orderSubs.filter(category = "Subs").exists() == False:
            context["alertMessage"] = "Error: You must order a sub before adding extra cheese. Please try again."
            return render(request, "orders/order.html", context)

#if user attempts to add too many toppings, generate an error
    if category == "Toppings" and currentOrder.toppingAllowance == 0:
        context["alertMessage"] = "Error: You have either reached your topping allowance or have not added an item eligble for toppings."
        return render(request, "orders/order.html", context)
#if they have enough toppings, add the topping and update the allowance accordingly
    elif category == "Toppings" and currentOrder.toppingAllowance > 0:
        currentOrder.toppingAllowance -= 1
        currentOrder.save()

    orderAdd = order_items(order=currentOrder, category=category, name=name, price=price)
    orderAdd.save()

    return render(request, "orders/order.html", context)

#function to remove items from cart
def remove(request, id):
    order_items.objects.filter(id=id).delete()
    #get the user's current order and items/categories
    orderNum = order.objects.get(user=request.user, status="initialized").order_number
    currentOrder = order.objects.get(user=request.user, order_number = orderNum)

    context = {
        "orderCategories": order_items.objects.filter(order=currentOrder).values_list('category').distinct(),
        "orderItems": order_items.objects.filter(order=currentOrder),
        "alertMessage": "The item has been removed from your cart.",
        "Total": order_items.objects.filter(order=currentOrder).aggregate(Sum('price'))['price__sum'] #calculate the cart total by summing the item's prices
    }

    return render(request, "orders/cart.html", context)

def cart(request):
    #get the user's current order and items/categories
    orderNum = order.objects.get(user=request.user, status="initialized").order_number
    currentOrder = order.objects.get(user=request.user, order_number = orderNum)


    context = {
        "orderCategories": order_items.objects.filter(order=currentOrder).values_list('category').distinct(),
        "orderItems": order_items.objects.filter(order=currentOrder),
        "Total": order_items.objects.filter(order=currentOrder).aggregate(Sum('price'))['price__sum'] #calculate the cart total by summing the item's prices
    }
    return render(request, "orders/cart.html", context)

def submitOrder(request):
    #when a user submits an order, get the current order and update the status
    orderNum = order.objects.get(user=request.user, status="initialized").order_number
    currentOrder = order.objects.get(user=request.user, order_number = orderNum)
    currentOrder.status="Submitted"
    currentOrder.save()

    #setup new empty cart now that the previous order was submitted
    newOrderNum = order.objects.all().aggregate(Max('order_number'))['order_number__max']
    newOrder = order(user=request.user, order_number = (orderNum +1),toppingAllowance=0, status="initialized")
    newOrder.save()

    #send email confirmation to user
    subject = 'Your Pinochio\'s Pizza Order'
    message = 'Thank you for your order!'
    from_email = settings.EMAIL_HOST_USER

    context = {
    "orderCategories": order_items.objects.filter(order=currentOrder).values_list('category').distinct(),
    "orderItems": order_items.objects.filter(order=currentOrder),
    "Total": order_items.objects.filter(order=currentOrder).aggregate(Sum('price'))['price__sum']
    }
    return render(request, "orders/submit.html", context)


def login_route(request):
    #retrieve user entry from form when POST request is made
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        #check to ensure that username and password combination is valid
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            #check to see if the user already has an initialized order
            userCart = order.objects.filter(user=user, status="initialized").count()

            #if they do not have an existing initialized order, create a new empty order
            if userCart == 0:
                orderNum = order.objects.all().aggregate(Max('order_number'))['order_number__max']
                newOrder = order(user=user, order_number = (orderNum +1),toppingAllowance=0, status="initialized")
                newOrder.save()

            #set default category to Regular Pizza
            initialCat = "Regular Pizza"
            return HttpResponseRedirect(reverse("order", args=(initialCat,)))
        else:
            return render(request, "orders/login.html", {"error": "The username/password you entered is not valid. Please try again."})
    else:
        #if not a POST request, just display the login page
        return render(request,"orders/login.html")

def logout_route(request):
    logout(request)
    return render(request,"orders/index.html")


def register(request):
    #retrieve form data when a POST request is made
    if request.method == 'POST':
        email = request.POST["email"]
        username = request.POST["username"]
        password = request.POST["password"]
        passwordValidation = request.POST["password2"]
        if not password == passwordValidation:
            return render(request, "orders/register.html", {"error": "Please ensure your passwords match."})

        #validate to ensure that username and email do not already exist in Users table
        if User.objects.filter(username=username).exists():
            return render(request, "orders/register.html", {"error": "Username already exists!"})
        if User.objects.filter(email=email).exists():
            return render(request, "orders/register.html", {"error": "Email already exists!"})
        user = User.objects.create_user(username, email, password)
        user.save()
        return render(request, "orders/login.html", {"success": "Your account has successfully been created! Please login below."})
    else:
        #if not a POST request, just display the register page
        return render(request, "orders/register.html")
