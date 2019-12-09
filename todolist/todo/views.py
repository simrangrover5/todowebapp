from django.shortcuts import render
from .models import Myuser,Mytasks
from django.views import View
from django.http import Http404
from django.contrib.auth.hashers import make_password,check_password
from datetime import datetime
import json
from django.http import HttpResponse
# Create your views here.
def index(request):
    if request.session.get('email'):
        now = datetime.now()
        date = now.strftime("%d/%m/%Y")
        day = now.strftime("%A")
        return render(request,"new.html",{'error':'Already Logged In','day':day,'date':date})
    else:
        return render(request,"register.html")


def login(request):
    if request.session.get('email'):
        now = datetime.now()
        date = now.strftime("%d/%m/%Y")
        day = now.strftime("%A")
        return render(request,"new.html",{'error':'Already Logged In','day':day,'date':date})
    else:
        return render(request,"login.html")

class register(View):
    def get(self,request):
        return Http404("page not found") 

    def post(self,request):
        if request.method == "POST":
            email = request.POST.get("email")
            password = request.POST.get("psw")
            cpassword = request.POST.get("cpsw")
            if password == cpassword:
                newpassword = make_password(password)
                data = {"email" : email,
                        "password" : newpassword
                        }
                newuser = Myuser.objects.create(**data)
                newuser.save()
                return render(request,"login.html",{'error':"login to continue"})
            else:
                return render(request,"register.html",{'error':'password does not matched'})

def afterlogin(request):
    email = request.POST.get("email")
    password = request.POST.get("psw")
    try:
        data = Myuser.objects.get(email=email)
    except Myuser.DoesNotExist as e:
        error = "No such user"
        return render(request,"login.html",{'error':error})
    else:
        if check_password(password,data.password):
            now = datetime.now()
            date = now.strftime("%d/%m/%Y")
            day = now.strftime("%A")
            request.session['email'] = email
            return render(request,"new.html",{'date':date,'day':day})
        else:
            return render(render,"login.html",{'error':"invalid password"})

class addtask(View):
    def get(self,request):
        return Http404("Page not found")
    
    def post(self,request):
        data = {
            'user' : Myuser.objects.get(email=request.session.get('email')),
            'priority' : request.POST.get('prior'),
            'schedule' : request.POST.get('sch'),
            'task'     : request.POST.get('task')
        }
        newtask = Mytasks.objects.create(**data)
        newtask.save()
        now = datetime.now()
        date = now.strftime("%d/%m/%Y")
        day = now.strftime("%A")
        return render(request,"new.html",{'error':'Task Added','day':day,'date':date})


def mytasks(request):

    data = Mytasks.objects.filter(user=Myuser.objects.get(email=request.session.get('email')))
    if len(data) == 0:
        return render(request,"task.html",{'error':"NO TASKS"})
    tasks = []
    colors = []
    for var in data:
        if var.priority.lower() == "high":
            color = "red"
        elif var.priority.lower() == "medium":
            color = "orange"
        else:
            color = "green"
        colors.append(color) 
    for var in range(len(data)):
        d = {
            'tasks' : data[var].task,
            'color' : colors[var],
            'date' : data[var].schedule
        }
        tasks.append(d)
    print(tasks)
    return render(request,'task.html',{'tasks':tasks})

def deltask(request,var):
    print(var)
    obj = Mytasks.objects.get(task=var)
    obj.delete()
    return render(request,"new.html",{'error':'successfully deleted'})

def logout(request):
    del request.session['email']
    return render(request,"login.html")
