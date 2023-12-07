from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json
from datetime import datetime,time,timedelta
import calendar
from .models import Feedbacks,user_total,total_daily,rating_model,student_info
from .forms import Feedback_form,Rating_Form
import pandas as pd
import json
from staffdeck.models import staff_info



def stulogin(request):
    staff_members_list = []
    staff_object = staff_info.objects.all()
    for i in staff_object:
        staff_members_list.append(i.user_name)
    return render(request,'auth/stulogin.html',{"staff_names":staff_members_list})

def log_out(request):
    logout(request)
    return redirect("home")

def stuhome(request):
    user = request.user
    try:
        google_account = user.socialaccount_set.get(provider='google')
        profile_picture_url = google_account.extra_data['picture']
    except user.socialaccount_set.model.DoesNotExist:
        profile_picture_url = None
    
    try:
        fobj = open('menu.json','r')
        global menu_data
        menu_data = json.load(fobj)
        next_data = {}
        if( time(9,0) < datetime.now().time() < time(14,0)):
          for date,data in menu_data.items():
            if(datetime.now().date().strftime("%Y-%m-%d") == date):
                meal = list(data.items())[1]
                next_data = {meal[0]:meal[1]}
        elif( time(14,0) < datetime.now().time() < time(21,0) ):
          for date,data in menu_data.items():
            if(datetime.now().date().strftime("%Y-%m-%d") == date):
                meal = list(data.items())[2]
                next_data = {meal[0]:meal[1]}
        elif(time(21,0) < datetime.now().time() < time(0,0)):
          for date,data in menu_data.items():
            next_date = datetime.now().date() + timedelta(days=1)
            if(next_date.strftime("%Y-%m-%d") == date):
                meal = list(data.items())[0]
                next_data = {meal[0]:meal[1]}
        else:
            for date,data in menu_data.items():
                if(datetime.now().date().strftime("%Y-%m-%d") == date):
                    meal = list(data.items())[0]
                    next_data = {meal[0]:meal[1]}
    except:
        menu_data = {}
        next_data = {}
         
    try:
        studentdata = student_info.objects.filter(user_name = request.user.username).first()
        stubhawan = studentdata.student_bhawan
        stuid = studentdata.student_id
    except:
        stubhawan = ""
        stuid = ""
    
    context = {"bhawan":stubhawan,"ID":stuid,'user': user, 'profile_picture_url': profile_picture_url,'menu_data':menu_data,"next_menu":next_data}
    return render(request, 'home/stuhome.html',context )
    



    


def inc_attendance(request):

    user = user_total.objects.filter(user_name = request.user.username).first()
    date_data = total_daily.objects.filter(date = datetime.now().date()).first()
    if not date_data:
        new_date = total_daily(date = datetime.now().date())
        new_date.save()
        date_data = total_daily.objects.filter(date = datetime.now().date()).first()

    if not user:
        new_user = user_total(user_name = request.user.username)
        new_user.save()
        user = user_total.objects.filter(user_name = request.user.username).first()

    
    if time(7,0) <= datetime.now().time() <= time(9,0):
        user.breakfast += 1
        date_data.breakfast += 1
        date_data.save()
        user.save()
        messages.success(request,"attendance marked")
    elif time(13,0) <= datetime.now().time() <= time(14,0):
        user.lunch += 1
        date_data.lunch += 1
        date_data.save()
        user.save()
        messages.success(request,"attendance marked")
    elif time(19,0) <= datetime.now().time() <= time(21,0):
        user.dinner += 1
        date_data.dinner += 1
        date_data.save()
        user.save()
        messages.success(request,"attendance marked")
    else:
        messages.success(request,"cannot mark your attendance right now")
    
    return redirect("stuhome")
    
    
def monthmenu(request):
    return render(request,"stupages/monthlymenu.html",{"menu_data":menu_data})


def unique_menu_items():
    try:
        fobj = open('menu.json','r')
        menu_data = json.load(fobj)
        item_list = []
        for date,time in menu_data.items():
            for key,value in time.items():
                for i in value:
                    if i not in item_list:
                        item_list.append(i)
                    else:
                        pass
        return item_list
    except:
        menu_data = {}

        
    
def menu_rating(request):
    item_list = unique_menu_items()
    if request.method == "POST":
        food = request.POST.get('selected_item')
        rating_int = request.POST.get("rating")
        try:
            rating_data = rating_model.objects.get(user_name = request.user.username, food_item = food)
        except:
            rating_data = None
        try:
            rating_data.rating = rating_int
            rating_data.save()
            messages.success(request,"Rating updated")
        except:
            data = rating_model(user_name = request.user.username, food_item = food, rating = rating_int)
            data.save()
            messages.success(request,"Rating submited")

    item_Rating_dict = {}
    for i in item_list:
        x = 0
        food_obj = rating_model.objects.filter(food_item = i)  
        count = 0
        for j in food_obj:
            x += j.rating
            count += 1
        if(count == 0):
            item_Rating_dict[i] = 0
        else:
            item_Rating_dict[i] = x/count

        
        

    return render(request,"stupages/rating.html",{'itemlist':item_list,'avg_rating':item_Rating_dict})



def feedback(request):
    if request.method == 'POST':
        form = Feedback_form(request.POST, request.FILES)
        if form.is_valid():
            u_name = request.user.username
            fback = form.cleaned_data['feed_back']
            pic = form.cleaned_data['picture']
            data = Feedbacks(user_name = u_name,feed_back = fback,picture = pic)
            data.save()
            return HttpResponse('You feedback have been submited')
    else:
            form = Feedback_form()  

    return render(request,"stupages/feedback.html",{'form':form})




def student_data(request):
    bhawan_list = ["Bhagirath","Budh","C.V. Raman","Gandhi","Krishna","Malaviya","Meera","Meera","Ram","Shankar","Srinivas Ramanujan","Vishwakarma","Vyas"]

    if request.method == "POST":
        stu_bhawan = request.POST.get("bhawan")
        id = request.POST.get("stu_id")
        try:
            studentdata = student_info.objects.filter(user_name = request.user.username).first()
            studentdata.student_bhawan = stu_bhawan
            studentdata.student_id = id
            studentdata.save()
            return redirect("stuhome")

        except: 
            data = student_info(user_name = request.user.username, student_bhawan = stu_bhawan,student_id = id, email=request.user.email)
            data.save()
            return redirect("stuhome")

        


    return render(request,"stupages/student_info.html",{"bhawans":bhawan_list})