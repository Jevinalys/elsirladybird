from django.shortcuts import render,redirect,get_object_or_404
from django.http import JsonResponse
from django.http import HttpResponse
from .models import *
import datetime
from django.utils import timezone
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm,SalesForm,BookingForm,CustomerForm,ServiceForm
from django import forms
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from validate_email import validate_email
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, DjangoUnicodeDecodeError
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.urls import reverse
from .utils import account_activation_token
import json
from django.contrib import auth
from django.db.models import Sum
from django.utils import timezone
from .filters import salesRepofilter 
import xlwt
from django.template.loader import render_to_string
#from weasyprint import HTML
import tempfile
from django.db.models import Sum


# Create your views here.
def index(request):

    return render (request, 'index.html')

@csrf_exempt
def usernameValidation(request):
    if request.method == 'POST':
        user_name = request.POST.get('username')
        if not str(user_name).isalnum():
            return JsonResponse({'username_error': 'username should only contain alphanumeric characters'})
        if User.objects.filter(username=user_name).exists():
            return JsonResponse({'username_error': 'sorry username in use,choose another one '})
        return JsonResponse({'username_valid': True})
    
@csrf_exempt
def firstnameValidation(request):
    if request.method == 'POST':
        first_name = request.POST.get('firstname')
        if not str(first_name).isalnum():
            return JsonResponse({'name_error': 'Your name should only contain alphanumeric characters'})
        if len(first_name) > 14:
            return JsonResponse({'name_error': 'Invalid name, name cannot have more that 15 letters'})
        return JsonResponse({'name_valid': True})

@csrf_exempt
def secondnameValidation(request):
    if request.method == 'POST':
        second_name = request.POST.get('secondname')
        if not str(second_name).isalnum():
            return JsonResponse({'name_error': 'Your name should only contain alphanumeric characters'})
        if len(second_name) > 14:
            return JsonResponse({'name_error': 'Invalid name, name cannot have more that 15 letters'})
        return JsonResponse({'username_valid': True})

@csrf_exempt
def phoneValidation(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phoneNo')
        if len(phone_number)>12:
            return JsonResponse ({'phone_error': 'phone number cannot be more than 12 characters.'})
        if Profile.objects.filter(phone=phone_number).exists():
            return JsonResponse({'phone_error': 'sorry phone number in use,choose another one '})
        return JsonResponse({'phone_valid': True})
    
@csrf_exempt
def emailValidation(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if not validate_email(email):
            return JsonResponse({'email_error': 'Email is invalid'})
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'sorry email in use,choose another one'})
        return JsonResponse({'email_valid': True})
       
def register_user(request):
    if request.method == "POST":
                
                username = request.POST['username']
                firstname = request.POST['firstname']
                secondname = request.POST['secondname']
                phone = request.POST['phoneNo']
                email = request.POST['email']
                password = request.POST['password2']

                context = {
                    
                    'fieldValues': request.POST
                }

                if not User.objects.filter(username=username).exists():

                    if not User.objects.filter(email=email).exists():

                        if len(password) < 6:

                            messages.error(request, 'Password too short')
                            return render(request, 'register.html', context)

                        user = User.objects.create_user(username=username,first_name=firstname,last_name=secondname, email=email)
                        profile = Profile.objects.create(user=user, phone=phone)
                        user.set_password(password)
                        user.is_active = False
                        user.save()
                        current_site = get_current_site(request)
                        email_body = {
                            'user': user,
                            'domain': current_site.domain,
                            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                            'token': account_activation_token.make_token(user),
                         }
                        
                        link = reverse('activate', kwargs={
                            'uidb64': email_body['uid'], 'token': email_body['token']})

                        email_subject = 'Activate your account'
                        activate_url = 'http://'+current_site.domain+link

                        email = EmailMessage(

                            email_subject,
                            'Hi '+user.username + ', Please the link below to activate your account \n'+activate_url +
                            '\nYour Username is :' +user.username,
                            'noreply@elsir.com',
                            [email],
                        )
                        email.send(fail_silently=False)
                        profile.save()

                        messages.success(request, 'Account successfully created check your email to activate account')
                        return render(request, 'register.html')
                    
    return render(request, 'register.html')

def VerificationView(request,uidb64,token):
    if request.method == "GET":  
                try:

                    id = force_bytes(urlsafe_base64_decode(uidb64))
                    user = User.objects.get(pk=id)

                    if not account_activation_token.check_token(user, token):
                        return redirect('login'+'?message='+'User already activated')

                    if user.is_active:
                        return redirect('login')
                    user.is_active = True
                    user.save()

                    messages.success(request, 'Account activated successfully')
                    return redirect('login')

                except Exception as ex:
                    pass

                return redirect('login')

@csrf_exempt
def login_user(request):

    if request.method == "GET":
        return render(request, 'login.html')

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = auth.authenticate(username=username, password=password)
            
            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, 'Welcome ' +
                                     user.username+' you are now logged in')
                    return redirect('dashboard')
                messages.error(
                    request, 'Account is not active,please check your email')
                return render(request,'login.html')

            messages.error(
                request, 'Invalid credentials,try again')
            return render(request, 'login.html')

        messages.error(
            request, 'Please fill all fields')
        return render(request, 'login.html')
        
def logout_user(request):

    logout(request)
    messages.success(request,("You have been logged out!..."))
    return redirect('login')
 
 
@login_required(login_url='login')
def dashboard(request):

    customers = Customer.objects.count()
 
    sales = Sale.objects.all().order_by('-date_paid')
    daily_sales=0
    monthly_sales=0
    paginator = Paginator(sales,5)
    page_number = request.GET.get('page')
    page_obj =Paginator.get_page(paginator, page_number)
    
    
    #Daily Sales
    for sales.date_paid in sales:
        today = str(timezone.now())
        todaySales=str(sales.date_paid)
        if todaySales[:11] == today[:11]:
            daily_sales +=1

    #Monthly Sales
    for sales.date_paid in sales:
        month = str(timezone.now())
        monthlySales=str(sales.date_paid)

        if monthlySales[:8] == month[:8]:
            monthly_sales +=1
        

    context = {'customers':customers, 'sales':sales, 'page_obj':page_obj, 'daily_sales':daily_sales,'monthly_sales':monthly_sales}
    

    return render(request,'dashboard.html',context)

@login_required(login_url='login')
def sales(request):

    sales = Sale.objects.all().order_by('-date_paid')
    paginator = Paginator(sales,7)
    page_number = request.GET.get('page')
    page_obj =Paginator.get_page(paginator, page_number)

    context = {'sales':sales,'page_obj':page_obj}

    return render(request,'sales.html',context)

@csrf_exempt
def search_sales(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        sales = Sale.objects.filter(
            phone__istartswith=search_str) | Sale.objects.filter(
            services__istartswith=search_str) | Sale.objects.filter(
            mpesa_code__istartswith=search_str) | Sale.objects.filter(
            date_paid__istartswith=search_str) | Sale.objects.filter(
            amount__icontains=search_str) 
        data = sales.values()
        return JsonResponse(list(data), safe=False)
    

@login_required(login_url='login')
def salesrepo(request):
        sales = Sale.objects.all().order_by('-date_paid')
        myFilter = salesRepofilter(request.GET,queryset=sales)
        sales=myFilter.qs

        month = timezone.now()
        dispmonth= month.strftime("%B")

        #Get the current date and calculate the start and end of the current month:
        now = timezone.now()
        start_of_month = now.replace(day=1)
        end_of_month = (start_of_month + timezone.timedelta(days=32)).replace(day=1)

        #Write the query to calculate the total sales for the current month:
        total_sales_current_month = Sale.objects.filter(
        date_paid__gte=start_of_month,
        date_paid__lt=end_of_month).aggregate(total_sales=Sum('amount'))['total_sales'] or 0

        #Write the query to calculate the total debts:
        total_debt = Customer.objects.aggregate(total_debt=Sum('debt'))['total_debt'] or 0

    
        paginator = Paginator(sales,7)
        page_number = request.GET.get('page')
        page_obj =Paginator.get_page(paginator, page_number)


        context = {'sales':sales,'myFilter':myFilter, 'page_obj':page_obj,'dispmonth':dispmonth,'total_sales_current_month':total_sales_current_month,'total_debt':total_debt}
    
        return render(request,'salesRepo.html',context)
        

@login_required(login_url='login')
def customers(request):
    customers = Customer.objects.all().order_by('first_name')
    form = CustomerForm()
    paginator = Paginator(customers,6)
    page_number = request.GET.get('page')
    page_obj =Paginator.get_page(paginator, page_number)

    context = {'customers':customers,'form':form,'page_obj':page_obj}

    return render(request,'customers.html',context)

@csrf_exempt
def search_customers(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        customer = Customer.objects.filter(
            first_name__istartswith=search_str) | Customer.objects.filter(
            second_name__istartswith=search_str) | Customer.objects.filter(
            phone__istartswith=search_str) | Customer.objects.filter(
            debt__istartswith=search_str) | Customer.objects.filter(
            loyalty_points__istartswith=search_str) 
        data = customer.values()
        return JsonResponse(list(data), safe=False)
    
@login_required(login_url='login')
def Inventory(request):
    
    services = Service.objects.all().order_by('service_name')
    form =ServiceForm()
    paginator = Paginator(services,8)
    page_number = request.GET.get('page')
    page_obj =Paginator.get_page(paginator, page_number)

    context = {'services':services,'form':form,'page_obj':page_obj}

    return render(request,'Inventory.html',context)


@login_required(login_url='login')
def bookings(request):

    book = Booking.objects.all()
    
    paginator = Paginator(book,8)
    page_number = request.GET.get('page')
    page_obj =Paginator.get_page(paginator, page_number)

    context = {'book':book,'page_obj':page_obj}

    return render(request,'bookings.html',context)

def delete_bookings(request,pk):

    booking = Booking.objects.get(id=pk)
    booking.delete()
    messages.warning(request, 'Booking succesfully deleted')
    return redirect('bookings')

@login_required(login_url='login')
def redeemPoints(request,pk):
    customer = Customer.objects.get(id=pk)
    form = CustomerForm(initial = {'first_name':customer.first_name,'second_name':customer.second_name,'phone':customer.phone,'debt':customer.debt})
    context = {
        'customer':customer,
        'form':form,
        'values': request.POST
    }

    if request.method == 'POST':
        
        redeemPoints = (request.POST['redeempoints'])
        if not redeemPoints:
                messages.error(
                    request, 'Points required')
                return render(request, 'redeemPoints.html', context)
        Rpoints= int(redeemPoints)
        mypoints = float(customer.loyalty_points)

        if Rpoints > mypoints or Rpoints == 0 or type(Rpoints) != int :
                messages.error(
                    request, 'Invalid Points')
                return render(request, 'redeemPoints.html', context)
        
        if Rpoints <=mypoints:

            points = mypoints-Rpoints
          
            Customer.objects.filter(id=pk).update(loyalty_points=points)
           
            messages.success(request, f'{Rpoints} successfully Redeemed')

            return redirect('customers')

    return render(request,'redeemPoints.html',context)


@login_required(login_url='login')
def payDebt(request,pk):
    customer = Customer.objects.get(id=pk)
    form = CustomerForm(initial = {'first_name':customer.first_name,'second_name':customer.second_name,'phone':customer.phone,'debt':customer.debt})
    context = {
        'customer':customer,
        'form':form,
        'values': request.POST
    }

    if request.method == 'POST':
        
        amount = (request.POST['amount'])
        if not amount:
                messages.error(
                    request, 'Amount required')
                return render(request, 'paydebt.html', context)
        myamount= int(amount)
        debt = int(customer.debt)
        mypoints = float(customer.loyalty_points)

        if myamount > debt or myamount == 0 or type(myamount) != int :
                messages.error(
                    request, 'Invalid Amount')
                return render(request, 'paydebt.html', context)
        
        else:
            points = myamount*0.01
            points += mypoints
            print(points)

            Customer.objects.filter(id=pk).update(loyalty_points=points)
            debt -= myamount
            Customer.objects.filter(id=pk).update(debt = debt)

            messages.success(request, 'Debt paid successfully')

            return redirect('customers')

    return render(request,'paydebt.html',context)


@login_required(login_url='login')
def addSales(request,pk):
    customer = Customer.objects.get(id=pk)
    form = SalesForm(initial = {'customer_name':customer,'phone':customer.phone})
    services = Service.objects.all()

    context = {
        'customer':customer,
        'form':form,
        'sales': sales,
        'services': services,
        'values': request.POST
    }

    if request.method == 'POST':
        
        amount = (request.POST['amount'])
        if not amount:
                messages.error(
                    request, 'Amount required')
                return render(request, 'addSales.html', context)
        myamount= int(amount)
        customer_name= customer
        payment_mode = request.POST['payment']
        services = request.POST['services']
        mpesa_code = request.POST['code']
        price = int(request.POST['serviceprice'])
        phone=customer.phone
        
        if myamount > price or myamount == 0 or type(myamount) != int :
                messages.error(
                    request, 'Invalid Amount')
                return render(request, 'addSales.html', context)

        if services == "Select service":
                
                messages.error(
                    request, 'Service not selected')
                return redirect('sales')
                 
        else:
            debt = int(customer.debt)
            points = myamount*0.01
            Customer.objects.filter(id=pk).update(loyalty_points=points)
            if myamount < (price + debt) or price == 0:
                balance = price - myamount
                debt +=balance
                Customer.objects.filter(id=pk).update(debt = debt)
            Sale.objects.create(customer_name=customer_name, phone=phone, services=services,
                               amount=myamount, mpesa_code=mpesa_code,payment_mode=payment_mode)
            messages.success(request, 'Expense saved successfully')

            return redirect('sales')

    return render(request,'addSales.html',context)

@csrf_exempt
def addService(request):
       
       if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            service_id = request.POST.get('serviceid')
            service_name = request.POST['service_name']
            decription = request.POST['service_description']
            price = request.POST['service_price']
            
            if(service_id == ''):

                services = Service(service_name=service_name, service_description=decription,service_price=price)
            else:
              
              services = Service(id=service_id, service_name=service_name, service_description=decription,service_price=price)
            services.save()

            serviceObject= Service.objects.values()
            service_data = list(serviceObject)
            return JsonResponse({'status':'Data Saved','service_data':service_data})
        else:
            print('service')
            return JsonResponse({'status':'Not Saved'})    

@csrf_exempt
def addCustomer(request):
       
       if request.method == 'GET':
           return redirect('customers.html')
           
       if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            custid = request.POST.get('customerid')
            first_name = request.POST['first_name']
            second_name = request.POST['second_name']
            phone = request.POST['phone']
            email_address = request.POST['email_address']
            if not first_name:
                messages.error(request, 'First Na Required')
            
            if(custid == ''):

                customers = Customer(first_name=first_name, second_name=second_name, phone=phone,email_address=email_address )
            else:
              
              customers = Customer(id=custid,first_name=first_name, second_name=second_name, phone=phone,email_address=email_address)
            customers.save()

            customerObject= Customer.objects.values()
            customer_data = list(customerObject)
            return JsonResponse({'status':'Data Saved','customer_data':customer_data})
        else:
            return JsonResponse({'status':'Not Saved'})    

 # context = {
      #  'values': request.POST
   # }
  

    # first_name = request.POST['first_name']

       # if not first_name:
           # messages.error(request, 'First Name is required')
           # return render(request, 'addCustomer.html', context)
        
       # second_name = request.POST['second_name']

        #if not second_name:
           # messages.error(request, 'Second Name is required')
           # return render(request, 'addCustomer.html', context)
        
       # phone = request.POST['phone']

        #if not phone:
          #  messages.error(request, 'Phone Number is required')
        #    return render(request, 'addCustomer.html', context)
        
      #  email_address = request.POST['email_address']
        


        #Customer.objects.create(first_name=first_name, second_name=second_name, phone=phone,email_address=email_address)
       # messages.success(request, 'Customer added successfully')

        #return redirect('customers')
    


   # return render(request,'addCustomer.html',context)
@csrf_exempt
def customer_delete(request):
    if request.method == 'POST':
        id = request.POST.get('custid')
        customer = Customer.objects.get(pk=id)
        print(id)
        customer.delete()
        messages.success(request, 'Expense removed')
        return JsonResponse({'status':'Customer Deleted'}) 
    
@csrf_exempt
def service_delete(request):
    if request.method == 'POST':
        id = request.POST.get('servid')
        service = Service.objects.get(pk=id)
        service.delete()
        serviceObject= Service.objects.values()
        service_data = list(serviceObject)
        return JsonResponse({'status':'service deleted','service_data':service_data})
        

#def addService(request):

    #context = {
        #'values': request.POST
   # }
    

    #if request.method == 'POST':                 
        
       # service_name = request.POST['service_name']

        #if not service_name:
            #messages.error(request, 'Service name is required')
            #return render(request, 'addService.html', context)
        
        #service_description = request.POST['service_description']

        #if not service_description:
            #messages.error(request, 'Description is required')
            #return render(request, 'addService.html', context)
        
        #service_price = request.POST['service_price']

       # if not service_price:
           # messages.error(request, 'Price is required')
           # return render(request, 'addService.html', context)
        


       # Service.objects.create(service_name=service_name, service_description=service_description, service_price=service_price)
       # messages.success(request, 'Service saved successfully')

       # return redirect('Inventory')
    


   # return render(request,'addService.html',context)

def book(request):
    bookings = Booking.objects.all()

    form = BookingForm()

    context = {
        'values': request.POST,
        'form':form
    }
  
    if request.method == 'POST':                 
        
        first_name = request.POST['first_name']

        if not first_name:
            messages.error(request, 'First Name is required')
            return render(request, 'book.html', context)
        
        second_name = request.POST['second_name']

        if not second_name:
            messages.error(request, 'Second Name is required')
            return render(request, 'book.html', context)
        
        phone_number = request.POST['phone_number']

        if not phone_number:
            messages.error(request, "Phone Number is required")
            return render(request, 'book.html', context)
        
        book_date = request.POST['book_date']

        if not book_date:
            messages.error(request, 'Date is required')
            return render(request, 'book.html', context)
         
        book_time = request.POST['book_time']
         
        if not book_time:
            messages.error(request, 'time is required')
            return render(request, 'book.html', context)
        
        for date in bookings:
            if book_date == date.book_date and book_time == date.book_time :
                            print('Slot not Available, select a diffirent time or date')
                            return render(request, 'book.html', context)

        Booking.objects.create(first_name=first_name, second_name=second_name,phone_number=phone_number, book_date=book_date, book_time=book_time)
        messages.success(request, 'Booking added successfully')

        return redirect('index')
    
    return render(request,'book.html',context)

@csrf_exempt
def updateCustomer(request):
    if request.method == 'POST':
        id = request.POST.get('custid')
        customer = Customer.objects.get(pk=id)
        customer_data = {'id':customer.id,'first_name':customer.first_name, 'second_name':customer.second_name, 'phone':customer.phone,'email_address':customer.email_address}
        return JsonResponse(customer_data)
    
@csrf_exempt
def updateService(request):
    if request.method == 'POST':
        id = request.POST.get('servid')
        service = Service.objects.get(pk=id)
        service_data = {'id':service.id,'service_name':service.service_name, 'service_description':service.service_description, 'service_price':service.service_price}
        return JsonResponse(service_data)
    
@csrf_exempt
def updateprice(request):
    if request.method == 'POST':
        id = request.POST.get('servid')
        service = Service.objects.get(service_name=id)

        service_data = {'service_price':service.service_price}
        return JsonResponse(service_data)

def monthly_servicesales(request):
    todays_date = timezone.now()
    current_months = todays_date-timezone.timedelta(days=30)
    sales = Sale.objects.filter(date_paid__gte=current_months, date_paid__lte=todays_date)
    finalrep = {}

    def get_services(sale):
        return sale.services
    services_list = list(set(map(get_services, sales)))

    def get_services_amount(services): 
        amount = 0
        filtered_by_services = sales.filter(services=services)
    
        for item in filtered_by_services:
            amount += item.amount
        return amount
    
    for x in sales:
        for y in services_list:
            finalrep[y] = get_services_amount(y)

    return JsonResponse({'services_summary_data': finalrep}, safe=False)

def monthly_sales_distribution(request):
    #todays_date = datetime.date.today()
    todays_date = timezone.now()
    current_months = todays_date-datetime.timedelta(days=30)
    sales = Sale.objects.filter(date_paid__gte=current_months, date_paid__lte=todays_date)
    finalrep = {}

    def get_month(sale):
        return str(sale.date_paid)
    month_list = list(set(map(get_month, sales)))


    def get_services_amount(date_paid): 
        amount = 0
        filtered_by_services = sales.filter(date_paid=date_paid)
        
        for item in filtered_by_services:
            amount += item.amount
        return amount

    for x in sales:
        for y in month_list:
            finalrep[y] = get_services_amount(y)

    return JsonResponse({'services_summary_data': finalrep}, safe=False)

@csrf_exempt
def updatetime(request):
    if request.method == 'POST':
        time = request.POST.get('timeid')
        mydate = request.POST.get('dateid')
       
        service_data = {'time':time,'mydate':mydate}
        return JsonResponse(service_data)

def export_excel(request):

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition']='attachment; filename=Sales_Report'+\
        str(timezone.now())+'.xls'
    
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Sales')

    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    font_style2 = xlwt.XFStyle()
    font_style2.font.bold = True

    columns = ['FirstName','SecondName','Phone','Service','Amount','Date','Debt']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()

    rows = Sale.objects.all().values_list('customer_name__first_name','customer_name__second_name','phone','services','amount','date_paid','customer_name__debt')
    
    total_amount = 0

    for row in rows:
        row_num+=1
       
        for col_num in range(len(row)):
            if col_num == 4:  # Assuming the 'amount' column index is 4
                total_amount += row[col_num]  # Sum the amounts


            ws.write(row_num, col_num,str(row[col_num]), font_style)

    # Write the total amount row
    row_num += 1
    ws.write(row_num, 3, 'Total Sales',font_style2)  # 'Total' label in the 'Service' column
    ws.write(row_num, 4, str(total_amount), font_style2)  # Total amount in the 'Amount' column

    

    wb.save(response)
        
    return response

def customer_excel(request):

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition']='attachment; filename=customers'+\
        str(timezone.now())+'.xls'
    
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Customers')

    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    font_style2 = xlwt.XFStyle()
    font_style2.font.bold = True

    columns = ['FirstName','SecondName','Phone','Email','Debt','Points']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()

    rows = Customer.objects.all().values_list('first_name','second_name','phone','email_address','debt','loyalty_points')
    
    for row in rows:
        row_num+=1
       
        for col_num in range(len(row)):
       
            ws.write(row_num, col_num,str(row[col_num]), font_style)


    wb.save(response)
        
    return response


'''def export_pdf(request):

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition']='attachment; filename=Sales_report'+\
        str(datetime.datetime.now())+'.pdf'
    response['Content-Transfer-Encoding'] = 'binary'

    html_string=render_to_string('elsir/templates/pdf-output.html',{'sales':[],'total':0})
    html = HTML(string=html_string)

    result = html.write_pdf()
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output=open(output.name,'rb')
        response.write(output.read())

    return response '''
    
