from .models import *

def global_variables(request):
    
    #------------------cart total------------------
    total = 0
    try:
        item_in_cart = Cart.objects.filter(UserID=request.user)
    except:
        item_in_cart = None
    if item_in_cart: 
        for item in item_in_cart:
            total += item.ProductID.Price * item.Qty
    
    #-------------number of items in cart-------------
    
    in_cart = 0
    try:
        cart = Cart.objects.filter(UserID=request.user)
    except:
        cart = None
    if cart:
        for p in cart:
            in_cart += 1 * p.Qty
    
     
    try:
        cart = Cart.objects.filter(UserID=request.user)
    except:
        cart = None
            
    return{'total' : total , 'in_cart' : in_cart , 'cart' : cart}




