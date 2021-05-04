from django.shortcuts import render


# landing page
def index(request):
    return render(request, 'pizza_orders/index.html')
