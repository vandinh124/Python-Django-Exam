from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt

# Create your views here.
def index(request):
    return render(request,"index.html")

def register(request):
    errors = User.objects.registration_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect("/")
    else:
        hashed_password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = hashed_password
        )
        fresh_user = User.objects.last()
        request.session['userid'] = fresh_user.id
        return redirect("/success")

def success(request):
    if 'userid' not in request.session:
        return redirect("/")
    context = {
        "logged_in_user": User.objects.get(id=request.session['userid']),
    }
    return render(request, "quotes.html", context)

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect("/")
    else:
        potential_user = User.objects.filter(email=request.POST['login_email'])[0]
        if bcrypt.checkpw(request.POST['login_password'].encode(),potential_user.password.encode()):
            request.session['userid'] = potential_user.id
            return redirect("/quotes")
        else:
            messages.error(request, "Invalid Login", extra_tags="login_password")
            return redirect("/")

def logout(request):
    request.session.clear()
    return redirect ('/')

# show all quotes 
def show_quotes(request):
    if 'userid' not in request.session:
        return redirect('/')
    user = User.objects.get(id = request.session['userid'])
    # count = user.user_favorites.count()
    all_quotes= Quote.objects.all()
    favorites = user.user_favorites.all()
    count = len(favorites)
    
    # total = len(favorites)
    context = {
        "logged_in_user": user,
        "all_quotes": all_quotes,
        "favorites": favorites,
        "count":count
      
        }
    return render (request, "quotes.html", context)    

def show_user(request,id):
    user = User.objects.get(id=id)
    user_quotes = Quote.objects.filter(posted_by=user)    

    context = {
        'user':user,
        'user_quotes':user_quotes,
        
    }
    return render(request,'user_info.html',context)

def delete_quote(request,id):    
    Quote.objects.get(id=str(id)).delete()
    return redirect ("/quotes")

def add_quote(request):
    errors=Quote.objects.quote_validator(request.POST)
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect ("/quotes")
    else: 
        Quote.objects.create(
            author = request.POST['author'],
            quote_message = request.POST['quote_message'],
            posted_by = User.objects.get(id=request.session['userid'])
        )
    return redirect('/quotes')

def add_to_favorite(request,id):
    logged_in_user = User.objects.get(id=request.session['userid'])
    quote_like = Quote.objects.get(id=id)
  
    if len(quote_like.quote_favorites.filter(user = logged_in_user))==0 :  
        Favorite.objects.create(
            user = logged_in_user,
            quote = quote_like
        )
    else:
        return redirect ("/quotes") 
    return redirect ("/quotes") 



def edit(request):
    if request.method == "GET":
        context = {
            "user":User.objects.get(id=id)
        }
        return render(request, "edit_account.html",context)
    if request.method == "POST":
        errors = User.objects.edit_profile_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect("/myaccount")
        else:
            user = User.objects.get(id=request.session['userid'])
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.email = request.POST['email']
            user.save()
        return redirect("/quotes")
    
def account(request):
    return render(request, "edit_account.html")

  

