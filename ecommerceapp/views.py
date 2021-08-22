from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Category,Product
from django.core.paginator import Paginator,EmptyPage,InvalidPage
from django.shortcuts import render,get_object_or_404
from django.contrib.auth.models import User,auth
from django.contrib import messages
# Create your views here.
# def home(request):
#     return HttpResponse("hello")

def allProdCat(request,c_slug=None):
    c_page=None
    products_list=None
    if c_slug!=None:
        c_page=get_object_or_404(Category,slug=c_slug)
        products_list=Product.objects.filter(category=c_page,available=True)
    else:
        products_list=Product.objects.all().filter(available=True)
    paginator=Paginator(products_list,20)
    try:
        page=int(request.GET.get('page','1'))
    except:
        page=1
    try:
        products=paginator.page(page)
    except (EmptyPage,InvalidPage):
        products=paginator.page(paginator.num_pages)

    return render(request,'category.html',{'category':c_page,'products':products})


def ProdCatDetail(request,c_slug,product_slug):
    try:
        product=Product.objects.get(category__slug=c_slug,slug=product_slug)
    except Exception as e:
        raise e
    return render(request,'product.html',{'product':product})

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request,'Email already used')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(request,'Username Already used')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username,email=email,password=password)
                user.save()
                return redirect('login')
        else:
            messages.info(request,'Password not same')
            return redirect('register')
    else:
        return render(request,'register.html')

def login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']

        user=auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            return redirect('ecommerceapp/')
        else:
            messages.info(request,'User is invalid')
            return redirect('login')
    else:
        return render(request,'login.html')

def logout(request):
    auth.logout(request)
    return redirect('ecommerceapp/')