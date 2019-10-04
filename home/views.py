from django.shortcuts import render,redirect
from django.db import connection
from .models import *
from django.http import HttpResponse
from .cn import *
current_user={'username':'','no':0, 'email':'','address':'', 'hname':'', 'status':False,'type':'','product':'','stock':0,'shname':""}

# Create your views here.
def index(req):
    return render(req,"home/index.html")

def signup(req):
    if req.method=='POST':
        user1=user()
        user1.email=req.POST.get('email')
        user1.hname=req.POST.get('hname')
        user1.username=req.POST.get('username')
        if len(req.POST.get('password'))>=8:
            user1.password=hash_password(req.POST.get('password'))
        else:
            return render(req,'home/signup.html',{'error':'Length of password must be minimum 8 characters'})
        user1.address=req.POST.get('address')
        s_user=user.objects.raw('select * from home_user')
        for i in s_user:
            if user1.username in i.username:
                return render(req,'home/signup.html',{'error':'This username has already been taken'})
        else:
            user1.save()
            return redirect('home:login')
    else:
        return render(req,'home/signup.html')

def login(req):
    if req.method=='POST':
        uname=req.POST.get('username')
        pswrd=req.POST.get('password')
        try:
            login_user=user.objects.raw('select * from home_user where username=%s',[uname])[0]
        except:
            return render(req,'home/login.html',{'error':'No such username present!'})
        if login_user:
            if verify_password(login_user.password,pswrd):
                current_user['username']=login_user.username
                current_user['email']=login_user.email
                current_user['hname']=login_user.hname
                current_user['status']=True
                current_user['address']=login_user.address
                return redirect('home:four')
            else:
                return render(req,'home/login.html',{'error':'The password is incorrect!'})
    else:
        return render(req,'home/login.html')


def blood1(req):
    l=list()
    if current_user['status']==True:
        if req.method=='POST':
            current_user['product']=req.POST.get('search_blood')
            bg=blood.objects.raw('select * from home_blood where bgroup=%s and hname<>%s',[current_user['product'],current_user['hname']])
            current_user['stock']=req.POST.get('stock')
            print(current_user['stock'])
            return render(req,'home/blood.html',{'blood':bg})
        else:
            current_user['type']=req.GET['name']
            return render(req,'home/blood.html')
    else:
        return redirect('home:login')
    return render(req,'home/profile.html')


def four(req):
    return render(req,'home/four.html')

def Request(req):
    p=req_table.objects.raw('select * from home_req_table where hname=%s order by id desc',[current_user['hname']])
    return render(req,'home/request.html',{'p':p})

def profile(req):
    if current_user['status']==True:
        if req.method=='POST':
            pass
        else:
            return render(req,'home/profile.html',{'hname':current_user['hname'],'email':current_user['email'],'address':current_user['address'],'user':current_user['username']})
    else:
        return redirect('home:login')
    return render(req,'home/profile.html')

def logout(req):
    current_user['username']=''
    current_user['email']=''
    current_user['hname']=''
    current_user['status']=False
    current_user['address']=''
    return redirect('home:login')

def update(req):
    if current_user['status']==True:
        if req.method=='POST':
            current_user['email']=req.POST.get('email')
            current_user['hname']=req.POST.get('hname')
            current_user['address']=req.POST.get('address')
            if len(req.POST.get('password'))>=8:
                password=req.POST.get('password')
            else:
                return render(req,'home/update.html',{'error':'Length of password must be minimum 8 characters'})
            with connection.cursor() as cursor:
                cursor.execute('update home_user set email = %s, hname=%s,address=%s,password=%s where username=%s',[current_user['email'],current_user['hname'],current_user['address'],hash_password(password),current_user['username']])
            return render(req,'home/message.html',{'message':'Your profile has been updated!'})
        else:
            return render(req,'home/update.html')
            
    else:
        return redirect('home:login')

def delete(req):
    if current_user['status']==True:
        if req.method=="POST":
            pswd=req.POST.get('password')
            login_user=user.objects.raw('select * from home_user where username=%s',[current_user['username']])[0]
            if verify_password(login_user.password,pswd):
                    with connection.cursor() as cursor:
                        cursor.execute('delete from home_user where username=%s',[current_user['username']])
                    return HttpResponse('Your profile has been deleted successfully!')
            else:
                return render(req,'home/delete.html',{'error':'The password is incorrect'})
        else:
            return render(req,'home/delete.html')
    else:
        return redirect('home:login')

def accept (req):
    if current_user['status']==True:
        if req.method=='POST':
            s1=req.POST.get('stock')
            s=int(s1)
            current_user['no']=s
            if current_user['type']=='blood':
                u=blood.objects.raw('select * from home_blood where hname=%s and bgroup=%s',[current_user['shname'],current_user['product']])[0]
                if s>u.stock:
                    return HttpResponse('Not sufficient Stock!')
                else:
                    with connection.cursor() as cursor:
                        l=u.stock-s
                        cursor.execute('update home_blood set stock=%s where hname=%s and bgroup=%s',[l,current_user['shname'],current_user['product']])
            

            if current_user['type']=='medicine':
                u=medicine.objects.raw('select * from home_medicine where hname=%s and med_name=%s',[current_user['shname'],current_user['product']])[0]
                if s>u.stock:
                    return HttpResponse('Not sufficient Stock!')
                else:
                    with connection.cursor() as cursor:
                        l=u.stock-s
                        cursor.execute('update home_medicine set stock=%s where hname=%s and med_name=%s',[int(l),current_user['shname'],current_user['product']])
            
            return redirect('home:accepted')
        else:
            current_user['shname']=req.GET['id']
            return render(req,'home/accept.html')
    else:
        return redirect('home:login')

def request(req):
    if current_user['status']==True:
        od=req_table.objects.raw("select * from home_req_table where delivered_status=1 and s_hname=%s order by id desc",[current_user['s_hname']])
        return render(req,"home/request.html",{'order_d':od})
    else:
        return redirect('home:login')

def medicine1(req):
    if current_user['status']==True:
        if req.method=='POST':
            current_user['product']=req.POST.get('search_medicine')
            m=medicine.objects.raw('select * from home_medicine where med_name=%s and hname<>%s',[current_user['product'],current_user['hname']])
            current_user['stock']=req.POST.get('stock')
            print(current_user['stock'])
            return render(req,'home/medicine.html',{'medicine':m})
        else:
            current_user['type']=req.GET['name']
            return render(req,'home/medicine.html')
    else:
        return redirect('home:login')
    return render(req,'home/profile.html')
    
def accepted(req):
    p=req_table()
    p.d_hname=current_user["hname"]
    p.hname=current_user['shname']
    p.entity=current_user['type']
    p.product=current_user['product']
    p.no_stock=current_user['no']
    p.save()        
    return render(req,'home/accepted.html')