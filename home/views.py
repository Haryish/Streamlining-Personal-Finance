from django.shortcuts import render,HttpResponse,redirect
from django.contrib import messages
from django.contrib.auth import authenticate ,logout
from django.contrib.auth import login as dj_login
from django.contrib.auth.models import User
from .models import Addmoney_info,UserProfile, Addmoney_info1
from django.contrib.sessions.models import Session
from django.core.paginator import Paginator, EmptyPage , PageNotAnInteger
from django.db.models import Sum
from django.http import JsonResponse
import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import  viewsets
from .models import *
from .serializer import *
from rest_framework.authtoken.models import Token
from django.utils.timezone import now
from datetime import timedelta
import plotly.graph_objects as go
from .forms import MonthSelectionForm
from django.contrib import messages
from django.contrib.auth import authenticate, login as dj_login


@api_view(['POST'])
def log_in(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = User.objects.filter(username=username).first()
    if user and user.check_password(password):
        token, created = Token.objects.get_or_create(user=user)
        return Response({"user_id": user.id, "token": token.key}, status=status.HTTP_200_OK)
    return Response({"detail": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def add_money_info(request):
    if request.method == 'POST':
        serializer = AddmoneyInfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

def get_users(request):
    users = User.objects.values('id', 'username')
    return JsonResponse(list(users), safe=False)
    
def home(request):
    if request.session.has_key('is_logged'):
        return redirect('/index')
    return render(request,'home/login.html')
   # return HttpResponse('This is home')
def index(request):
    if request.session.has_key('is_logged'):
        user_id = request.session["user_id"]
        user = User.objects.get(id=user_id)
        addmoney_info = Addmoney_info.objects.filter(user=user).order_by('-Date')
        paginator = Paginator(addmoney_info , 4)
        page_number = request.GET.get('page')
        page_obj = Paginator.get_page(paginator,page_number)
        context = {
           'page_obj' : page_obj
        }
        return render(request,'home/index.html',context)
    return redirect('home')
def register(request):
    return render(request,'home/register.html')
def password(request):
    return render(request,'home/password.html')

def charts(request):
    return render(request,'home/charts.html')
def search(request):
    if request.session.has_key('is_logged'):
        user_id = request.session["user_id"]
        user = User.objects.get(id=user_id)
        fromdate = request.GET['fromdate']
        todate = request.GET['todate']
        addmoney = Addmoney_info.objects.filter(user=user, Date__range=[fromdate,todate]).order_by('-Date')
        res = 0
        for i in addmoney:
            res+=i.quantity
        return render(request,'home/tables.html',{'addmoney':addmoney,'res':res})
    return redirect('home')

def search1(request):
    if request.session.has_key('is_logged'):
        user_id = request.session["user_id"]
        user = User.objects.get(id=user_id)
        fromdate = request.GET['fromdate']
        todate = request.GET['todate']
        addmoney = Addmoney_info1.objects.filter(user=user, Date__range=[fromdate,todate]).order_by('-Date')
        res = 0
        for i in addmoney:
            res+=i.quantity
        return render(request,'home/tables1.html',{'addmoney':addmoney,'res':res})
    return redirect('home')

def tables(request):
    if request.session.has_key('is_logged'):
        user_id = request.session["user_id"]
        user = User.objects.get(id=user_id)
        addmoney = Addmoney_info.objects.filter(user=user).order_by('-Date')
        res = 0
        for i in addmoney:
            res+=i.quantity
        return render(request,'home/tables.html',{'addmoney':addmoney,'res':res})
    
    return redirect('home')

def tables1(request):
    if request.session.has_key('is_logged'):
        user_id = request.session["user_id"]
        user = User.objects.get(id=user_id)
        addmoney = Addmoney_info1.objects.filter(user=user).order_by('-Date')
        res = 0
        for i in addmoney:
            res+=i.quantity
        return render(request,'home/tables1.html',{'addmoney':addmoney,'res':res})
    return redirect('home')


def addmoney(request):
    return render(request,'home/addmoney.html')

def addmoney1(request):
    return render(request,'home./addmoney1.html')


def mon_exp_page(request):
    return render(request,'home/mon_exp_page.html')


def profile(request):
    if request.session.has_key('is_logged'):
        user_id = request.session["user_id"]
        data = UserProfile.objects.get(user_id=user_id).income
        res = 0
        user1 = User.objects.get(id=user_id)
        data1 = Addmoney_info1.objects.filter(user=user1)
        for i in data1:
            res+=i.quantity
        data+=res
        return render(request,'home/profile.html',{'data':data})
    return redirect('/home')

def E_table(request):
    user_id = request.session["user_id"]
    user1 = User.objects.get(id=user_id)
    data = Addmoney_info.objects.filter(user_id=user1)
    return render(request,'home/E_table.html',{'data':data})

def I_table(request):
    user_id = request.session["user_id"]
    user1 = User.objects.get(id=user_id)
    data = Addmoney_info1.objects.filter(user_id=user1)
    return render(request,'home/I_table.html',{'data':data})


def profile_edit(request,id):
    if request.session.has_key('is_logged'):
        add = User.objects.get(id=id)
        # user_id = request.session["user_id"]
        # user1 = User.objects.get(id=user_id)
        return render(request,'home/profile_edit.html',{'add':add})
    return redirect("/home")

def profile_update(request,id):
    if request.session.has_key('is_logged'):
        if request.method == "POST":
            user = User.objects.get(id=id)
            user.first_name = request.POST["fname"]
            user.last_name = request.POST["lname"]
            user.email = request.POST["email"]
            user.userprofile.gender = request.POST["gender"]
            user.userprofile.Savings = request.POST["Savings"]
            user.userprofile.income = request.POST["income"]
            user.userprofile.profession = request.POST["profession"]
            user.userprofile.save()
            user.save()
            return redirect("/profile")
    return redirect("/home")

def handleSignup(request):
    if request.method =='POST':
            # get the post parameters
            uname = request.POST["uname"]
            fname=request.POST["fname"]
            lname=request.POST["lname"]
            email = request.POST["email"]
            gender = request.POST["gender"]
            profession = request.POST['profession']
            Savings = request.POST['Savings']
            income = request.POST['income']
            pass1 = request.POST["pass1"]
            pass2 = request.POST["pass2"]
            profile = UserProfile(gender=gender,Savings = Savings,profession=profession,income=income)
            # check for errors in input
            if request.method == 'POST':
                try:
                    user_exists = User.objects.get(username=request.POST['uname'])
                    messages.error(request," Username already taken, Try something else!!!")
                    return redirect("/register")    
                except User.DoesNotExist:
                    if len(uname)>15:
                        messages.error(request," Username must be max 15 characters, Please try again")
                        return redirect("/register")
            
                    if not uname.isalnum():
                        messages.error(request," Username should only contain letters and numbers, Please try again")
                        return redirect("/register")
            
                    if pass1 != pass2:
                        messages.error(request," Password do not match, Please try again")
                        return redirect("/register")
            
            # create the user
            user = User.objects.create_user(uname, email, pass1)
            user.first_name=fname
            user.last_name=lname
            user.email = email
            # profile = UserProfile.objects.all()

            #user.set_password(User.cleaned_data['password'])
            user.save()
            # p1=profile.save(commit=False)
            profile.user = user
            profile.save()
            messages.success(request," Your account has been successfully created")
            return redirect("/")
    else:
        return HttpResponse('404 - NOT FOUND ')
    return redirect('/login')

def handlelogin(request):
    if request.method == 'POST':
        # Get the post parameters
        loginuname = request.POST["loginuname"]
        loginpassword1 = request.POST["loginpassword1"]
        
        # Try to authenticate the user
        user = authenticate(username=loginuname, password=loginpassword1)
        
        if user is not None:
            # If authentication is successful, log the user in
            dj_login(request, user)
            request.session['is_logged'] = True
            request.session["user_id"] = user.id  # Store the user ID in session
            messages.success(request, "Successfully logged in")
            return redirect('/index')
        else:
            # If authentication fails, show an error message
            messages.error(request, "Invalid credentials, please try again.")
            return redirect("/")  # Redirect back to the login page
    
    return HttpResponse('404 - NOT FOUND')

def handleLogout(request):
        del request.session['is_logged']
        del request.session["user_id"] 
        logout(request)
        messages.success(request, " Successfully logged out")
        return redirect('home')


#add money form
def addmoney_submission(request):
    if request.session.has_key('is_logged'):
        if request.method == "POST":
            user_id = request.session["user_id"]
            user1 = User.objects.get(id=user_id)
            addmoney_info1 = Addmoney_info.objects.filter(user=user1).order_by('-Date')
            add_money = request.POST["add_money"]
            quantity = request.POST["quantity"]
            Date = request.POST["Date"]
            today = datetime.date.today()
            Category = request.POST["Category"]
            add = Addmoney_info(user = user1,add_money=add_money,quantity=quantity,Date = Date,Category= Category)
            if Date>str(today):
                return render(request,'home/addmoney.html',{'mess':True})
            else:
                add.save()
            paginator = Paginator(addmoney_info1, 4)
            page_number = request.GET.get('page')
            page_obj = Paginator.get_page(paginator,page_number)
            context = {
                'page_obj' : page_obj
                }
            return render(request,'home/index.html',context)
    return redirect('/index')


def addmoney_submission1(request):
    if request.session.has_key('is_logged'):
        if request.method == "POST":
            user_id = request.session["user_id"]
            user1 = User.objects.get(id=user_id)
            addmoney_info1 = Addmoney_info1.objects.filter(user=user1).order_by('-Date')
            add_money = request.POST["add_money"]
            quantity = request.POST["quantity"]
            Date = request.POST["Date"]
            Category = request.POST["Category"]
            add = Addmoney_info1(user = user1,add_money=add_money,quantity=quantity,Date = Date,Category= Category)
            today = datetime.date.today()
            if Date>str(today):
                return render(request,'home/addmoney1.html',{'mess':True})
            else:
                add.save()
            paginator = Paginator(addmoney_info1, 4)
            page_number = request.GET.get('page')
            page_obj = Paginator.get_page(paginator,page_number)
            context = {
                'page_obj' : page_obj
                }
            return render(request,'home/index.html',context)
    return redirect('/index')



def addmoney_update(request,id):
    if request.session.has_key('is_logged'):
        if request.method == "POST":
            add  = Addmoney_info.objects.get(id=id)
            add .add_money = request.POST["add_money"]
            add.quantity = request.POST["quantity"]
            add.Date = request.POST["Date"]
            add.Category = request.POST["Category"]
            add .save()
            return redirect("/index")
    return redirect("/home")


def addmoney_update1(request,id):
    if request.session.has_key('is_logged'):
        if request.method == "POST":
            add  = Addmoney_info1.objects.get(id=id)
            add .add_money = request.POST["add_money"]
            add.quantity = request.POST["quantity"]
            add.Date = request.POST["Date"]
            add.Category = request.POST["Category"]
            add .save()
            return redirect("/index")
    return redirect("/home")   


def expense_edit(request,id):
    if request.session.has_key('is_logged'):
        addmoney_info = Addmoney_info.objects.get(id=id)
        return render(request,'home/expense_edit.html',{'addmoney_info':addmoney_info})
    return redirect("/home")  

def income_edit(request,id):
    if request.session.has_key('is_logged'):
        addmoney_info1 = Addmoney_info1.objects.get(id=id)
        return render(request,'home/expense_edit.html',{'addmoney_info':addmoney_info1})
    return render("/home")


def expense_delete(request,id):
    if request.session.has_key('is_logged'):
        addmoney_info = Addmoney_info.objects.get(id=id)
        addmoney_info.delete()
        return redirect("/index")
    return redirect("/home")

def income_delete(request,id):
    if request.session.has_key('is_logged'):
        addmoney_info = Addmoney_info1.objects.get(id=id)
        addmoney_info.delete()
        return redirect("/index")
    return redirect("/home")  

def expense_month(request):
    todays_date = datetime.date.today()
    one_month_ago = todays_date-datetime.timedelta(days=30)
    user_id = request.session["user_id"]
    user1 = User.objects.get(id=user_id)
    addmoney = Addmoney_info.objects.filter(user = user1,Date__gte=one_month_ago,Date__lte=todays_date)
    finalrep ={}

    def get_Category(addmoney_info):
        # if addmoney_info.add_money=="Expense":
        return addmoney_info.Category    
    Category_list = list(set(map(get_Category,addmoney)))

    def get_expense_category_amount(Category,add_money):
        quantity = 0 
        filtered_by_category = addmoney.filter(Category = Category,add_money="Expense") 
        for item in filtered_by_category:
            quantity+=item.quantity
        return quantity

    for x in addmoney:
        for y in Category_list:
            finalrep[y]= get_expense_category_amount(y,"Expense")
    return JsonResponse({'expense_category_data': finalrep}, safe=False)



def stats(request):
    # if request.session.has_key('is_logged'):
    #     todays_date = datetime.date.today()
    #     one_month_ago = todays_date-datetime.timedelta(days=30)
    #     user_id = request.session["user_id"]
    #     user1 = User.objects.get(id=user_id)
    #     addmoney_info = Addmoney_info.objects.filter(user = user1,Date__gte=one_month_ago,Date__lte=todays_date)
    #     sum = 0 
    #     for i in addmoney_info:
    #         if i.add_money == 'Expense':
    #             sum=sum+i.quantity
    #     addmoney_info.sum = sum
    #     sum1 = 0 
    #     for i in addmoney_info:
    #         if i.add_money == 'Income':
    #             sum1 =sum1+i.quantity
    #     addmoney_info.sum1 = sum1
    #     x= user1.userprofile.Savings+addmoney_info.sum1 - addmoney_info.sum
    #     y= user1.userprofile.Savings+addmoney_info.sum1 - addmoney_info.sum
    #     if x<0:
    #         messages.warning(request,'Your expenses exceeded your savings')
    #         x = 0
    #     if x>0:
    #         y = 0
    #     addmoney_info.x = abs(x)
    #     addmoney_info.y = abs(y)
    
    # Initialize the form with GET data if available
    # Initialize the form with GET data if available
    form = MonthSelectionForm(request.GET or None)
    
    # Initialize variables for the chart and month display
    graph1_html = None
    month_name = None

    if form.is_valid():
        # Get the selected month and year (current year)
        selected_month = form.cleaned_data['month']
        year = now().year
        
        # Get the start date of the selected month
        start_date = f'{year}-{selected_month}-01'
        
        # Calculate the end date of the selected month
        if selected_month == '12':
            end_date = f'{year + 1}-01-01'  # Next year if December
        else:
            next_month = int(selected_month) + 1
            end_date = f'{year}-{next_month:02d}-01'
        
        # Query the database for expenses within the selected month
        expenses = Addmoney_info.objects.filter(Date__gte=start_date, Date__lt=end_date)
        
        # Aggregate expenses by category
        category_expenses = expenses.values('Category').annotate(total_expense=Sum('quantity'))
        
        # Extract categories and amounts for the pie chart
        categories = [expense['Category'] for expense in category_expenses]
        amounts = [expense['total_expense'] for expense in category_expenses]
        
        # Generate the Plotly pie chart
        fig = go.Figure(data=[go.Pie(labels=categories, values=amounts, hole=0.3)])
        fig.update_traces(textinfo='percent+label')
        
        # Convert the figure to HTML
        graph1_html = fig.to_html(full_html=False)
        
        # Find the month name from MONTH_CHOICES
        month_name_dict = dict(MonthSelectionForm.MONTH_CHOICES)  # Create a dict from the choices
        month_name = month_name_dict.get(selected_month)  # Get the name of the month

    return render(request,'home/stats.html',{
        'form': form, 
        'graph1_html': graph1_html, 
        'month_name': month_name})

def expense_week(request):
    todays_date = datetime.date.today()
    one_week_ago = todays_date-datetime.timedelta(days=7)
    user_id = request.session["user_id"]
    user1 = User.objects.get(id=user_id)
    addmoney = Addmoney_info.objects.filter(user = user1,Date__gte=one_week_ago,Date__lte=todays_date)
    finalrep ={}

    def get_Category(addmoney_info):
        return addmoney_info.Category
    Category_list = list(set(map(get_Category,addmoney)))


    def get_expense_category_amount(Category,add_money):
        quantity = 0 
        filtered_by_category = addmoney.filter(Category = Category,add_money="Expense") 
        for item in filtered_by_category:
            quantity+=item.quantity
        return quantity

    for x in addmoney:
        for y in Category_list:
            finalrep[y]= get_expense_category_amount(y,"Expense")
    return JsonResponse({'expense_category_data': finalrep}, safe=False)

def weekly(request):
    # if request.session.has_key('is_logged'):
    #     todays_date = datetime.date.today()
    #     one_week_ago = todays_date-datetime.timedelta(days=7)
    #     user_id = request.session["user_id"]
    #     user1 = User.objects.get(id=user_id)
    #     addmoney_info = Addmoney_info.objects.filter(user = user1,Date__gte=one_week_ago,Date__lte=todays_date)
    #     sum = 0
    #     for i in addmoney_info:
    #         if i.add_money == 'Expense':
    #             sum=sum+i.quantity
    #     addmoney_info.sum = sum
    #     sum1 = 0
    #     for i in addmoney_info:
    #         if i.add_money == 'Income':
    #             sum1 =sum1+i.quantity
    #     addmoney_info.sum1 = sum1
    #     x= user1.userprofile.Savings+addmoney_info.sum1 - addmoney_info.sum
    #     y= user1.userprofile.Savings+addmoney_info.sum1 - addmoney_info.sum
    #     if x<0:
    #         messages.warning(request,'Your expenses exceeded your savings')
    #         x = 0
    #     if x>0:
    #         y = 0
    #     addmoney_info.x = abs(x)
    #     addmoney_info.y = abs(y)
    
    today = now().date()
    
    # Get the start of the current week (assuming Sunday is the first day of the week)
    start_date = today - timedelta(days=today.weekday())
    
    # Query the database for expenses within the current week
    expenses = Addmoney_info.objects.filter(Date__gte=start_date, Date__lte=today)
    
    # Aggregate expenses by category
    category_expenses = expenses.values('Category').annotate(total_expense=Sum('quantity'))

    # Extract categories and amounts
    categories = [expense['Category'] for expense in category_expenses]
    amounts = [expense['total_expense'] for expense in category_expenses]

    # Create a Plotly pie chart
    fig = go.Figure(data=[go.Pie(labels=categories, values=amounts, hole=0.3)])
    fig.update_traces(textinfo='percent+label')

    # Convert the plotly figure to HTML
    graph1_html = fig.to_html(full_html=False)

    return render(request,'home/weekly.html',{'graph1_html':graph1_html})

def check(request):
    if request.method == 'POST':
        user_exists = User.objects.filter(email=request.POST['email'])
        messages.error(request,"Email not registered, TRY AGAIN!!!")
        return redirect("/reset_password")

def info_year(request):
    todays_date = datetime.date.today()
    one_week_ago = todays_date-datetime.timedelta(days=30*12)
    user_id = request.session["user_id"]
    user1 = User.objects.get(id=user_id)
    addmoney = Addmoney_info.objects.filter(user = user1,Date__gte=one_week_ago,Date__lte=todays_date)
    finalrep ={}

    def get_Category(addmoney_info):
        return addmoney_info.Category
    Category_list = list(set(map(get_Category,addmoney)))


    def get_expense_category_amount(Category,add_money):
        quantity = 0 
        filtered_by_category = addmoney.filter(Category = Category,add_money="Expense") 
        for item in filtered_by_category:
            quantity+=item.quantity
        return quantity

    for x in addmoney:
        for y in Category_list:
            finalrep[y]= get_expense_category_amount(y,"Expense")

    return JsonResponse({'expense_category_data': finalrep}, safe=False)

def info(request):
    # Get the current date and the date 12 months ago
    current_date = now().date()
    start_date = current_date - timedelta(days=365)

    # Fetch expenses and incomes for the last 12 months
    expenses_data = Addmoney_info.objects.filter(
        Date__gte=start_date, Date__lte=current_date, add_money='Expense'
    ).values('Date__month').annotate(total_expenses=Sum('quantity')).order_by('Date__month').filter(user=request.user)

    income_data = Addmoney_info1.objects.filter(
        Date__gte=start_date, Date__lte=current_date, add_money='Income'
    ).values('Date__month').annotate(total_income=Sum('quantity')).order_by('Date__month').filter(user=request.user)

    # Prepare lists for months, expenses, and income
    months = [f'{i+1}' for i in range(12)]  # List for months (1, 2, ..., 12)
    expense_values = [0] * 12
    income_values = [0] * 12

    # Populate the expense and income values based on the month
    for expense in expenses_data:
        month = expense['Date__month'] - 1
        expense_values[month] = expense['total_expenses']

    for income in income_data:
        month = income['Date__month'] - 1
        income_values[month] = income['total_income']

    # Create the bar chart using plotly
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=months, y=expense_values,
        name='Expenses',
        marker_color='red'
    ))

    fig.add_trace(go.Bar(
        x=months, y=income_values,
        name='Income',
        marker_color='green'
    ))

    # Update layout of the plot
    fig.update_layout(
        barmode='group',
        title='Monthly Income vs Expenses (Last 12 Months)',
        xaxis_title='Month',
        yaxis_title='Amount',
        showlegend=True
    )

    # Convert the figure to HTML (without full HTML wrapper)
    graph1_html = fig.to_html(full_html=False)

    # Render the template and pass the graph HTML
    return render(request,'home/info.html', {'graph': graph1_html})
     