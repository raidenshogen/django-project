from django.shortcuts import render,redirect
from django.http import JsonResponse
import json
import datetime
from .models import *
from . utils import cookieCart,  cartData, guestOrder
from django.contrib.auth.decorators import login_required

# Create your views here.

def store(request):
    data = cartData(request)
    cartItems = data['cartItems'];
     
    products= Product.objects.all()
    context = {'products':products,'cartItems':cartItems}
    return render(request, 'store/store.html',context)


def checkout(request):
    data = cartData(request)
    cartItems = data['cartItems'];
    order = data['order'];
    items = data['items'];
    context = {'items':items,'order':order,'cartItems':cartItems}
   
    return render(request, 'store/checkout.html',context)
def cart(request):
    data = cartData(request)
    cartItems = data['cartItems'];
    order = data['order'];
    items = data['items'];

    context = {'items':items,'order':order,'cartItems':cartItems}
    return render(request, 'store/cart.html',context)

def updateItem(request):
    data = json.loads(request.body)
    prodid = data['prodid']
    action = data['action']
    print('Action', action)
    print('prodid', prodid)
    customer = request.user.customer
    product = Product.objects.get(id=prodid)
    orders = Order.objects.filter(customer=customer, complete=False)
    if orders.exists():
        order = orders.first()
    else:
        order = Order.objects.create(customer=customer, complete=False)

    orderItems = OrderItems.objects.filter(Order=order, product=product)
    if orderItems.exists():
        orderItem = orderItems.first()
    else:
        orderItem = OrderItems.objects.create(Order=order, product=product)

    if action == 'add':
        orderItem.quantity += 1
    elif action == 'remove':
        orderItem.quantity -= 1
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('Item removed', safe=False)
#from django.views.decorators.csrf import csrf_exempt
#@csrf_exempt           
def processOrder(request):
    transaction_id=datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        # get the most recent order for the customer that has not been ordered yet
        order = Order.objects.filter(customer=customer, ordered=False).order_by('-date_ordered').first()
        # handle the case where there is a matching order
        if order is not None:
            # update the existing order
            order.transaction_id = transaction_id
            order.save()
        # handle the case where there is no matching order
        else:
            # create a new order for the customer
            order = Order.objects.create(customer=customer, transaction_id=transaction_id)
            # save the new order
            order.save()
    else:
        customer, order = guestOrder(request, data)
    total = float(data['form']['total'])
    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )
    return JsonResponse('Payment complete!',safe=False)