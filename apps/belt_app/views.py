from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Quote, Favorite
from datetime import *

def index(request):
    today = datetime.now()
    Yr = datetime.strftime(today,'%Y')
    Month = datetime.strftime(today,'%m')
    Day = datetime.strftime(today,'%d')
    newYr = int(Yr) - 10

    ageLimit = ("{}-{}-{}").format(newYr,Month,Day)

    age = {
        'age':ageLimit
    }

    return render(request, 'belt_app/index.html', age)

def register(request):
    response = User.objects.register(
        name = request.POST['name'],
        alias = request.POST['alias'],
        password = request.POST['password'],
        confirm_password = request.POST['confirm_password'],
        dob = request.POST['dob']
    )

    if response['valid']:
        request.session["user_id"] = response['user'].id
        return redirect("/quotes")
    else: 
        for error in response['errors']:
            messages.error(request, error)
        return redirect('/')

def login(request):
    response = User.objects.login(
        alias = request.POST['alias'], 
        password = request.POST['password'],
    )

    if response['valid']:
        request.session['user_id'] = response['user'].id
        return redirect('/quotes')
    
    if len(response['errors']) > 0:
        for error in response['errors']:
            messages.warning(request, error)
        return redirect('/')

def logout(request):
    request.session.flush()
    return redirect('/')

def quotes(request):
    if 'user_id' not in request.session:
        messages.warning(request, 'You must log in first!')
        return redirect("/")

    allQuotes = Quote.objects.all()
    totalQuotes = Quote.objects.all()
    faveQuotes = Favorite.objects.filter(user_id=request.session["user_id"])
    
    for fqs in faveQuotes:
        allQuotes = allQuotes.exclude(id=fqs.quote.id)

    data = {
        'quotes': allQuotes,
        'faves': faveQuotes,
        'user': User.objects.get(id=request.session["user_id"])
    }

    return render(request, 'belt_app/quotes.html', data)

def new_quote(request):
    if 'user_id' not in request.session:
        messages.warning(request, 'You must log in first!')
        return redirect("/")

    response = Quote.objects.new_quote(
        request.POST['author'],
        request.POST['text'],
        posted_by =User.objects.get(id=request.session["user_id"])
    )

    if response['valid']:
        return redirect("/quotes")
    else: 
        for error in response['errors']:
            messages.error(request, error)
        return redirect('/quotes')

def new_favorite(request, id):
    if 'user_id' not in request.session:
        messages.warning(request, 'You must log in first!')
        return redirect("/")

    response = Favorite.objects.new_favorite(
        quote = Quote.objects.get(id=id),
        user = User.objects.get(id=request.session["user_id"])
    )
    
    return redirect('/quotes')

def delete_favorite(request, id):
    if 'user_id' not in request.session:
        messages.warning(request, 'You must log in first!')
        return redirect("/")
    
    allFavorites = Favorite.objects.filter(quote_id=id)
    for fave in allFavorites:
        dQDelete =  fave.id

    response = Favorite.objects.delete_favorite(
        id = dQDelete
    )
    
    return redirect('/quotes')

def user_page(request, id):
    if 'user_id' not in request.session:
        messages.warning(request, 'You must log in first!')
        return redirect("/")
    
    postedQuotes = Quote.objects.filter(posted_by_id=id)
    totalquote = Quote.objects.filter(posted_by_id=id)

    for i in range(len(totalquote)):
        total = i + 1

    data = {
        'quotes': postedQuotes,
        'user': User.objects.get(id=id),
        'total': total,
        'sesh': User.objects.get(id=request.session['user_id'])
    }

    return render(request, 'belt_app/user_page.html', data)

def delete_quote(request, id):
    
    Quote.objects.delete_quote(id=id)

    return redirect('/quotes')