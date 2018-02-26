# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from .models import User, Plan
from django.contrib import messages

def local(request):
    return redirect('/main')

def index(request):
    return render(request, 'travel_buddy/index.html')

def register(request):
    reginfo = User.objects.register(request.POST)
    if reginfo[0]: 
        request.session['username'] = reginfo[1].username
        return redirect('/travels')
    else: 
        for error in reginfo[1]:
            messages.add_message(request, messages.ERROR, error)
        return redirect('/')

def login(request):
    logininfo = User.objects.login(request.POST)
    if logininfo[0]: 
        request.session['username'] = logininfo[1].username 
        return redirect('/travels')
    else: 
        for error in logininfo[1]:
            messages.add_message(request, messages.ERROR, error)
        return redirect('/')

def dashboard(request):
    if 'username' not in request.session:
        return redirect('/')
    user = User.objects.get(username=request.session['username'])
    data = {
        "user": User.objects.get(id=user.id),
        "myplans": Plan.objects.filter(travelers=user.id),
        "otherplans": Plan.objects.exclude(travelers=user.id)
    }
    return render(request, 'travel_buddy/dashboard.html', data)

def add_plan(request):
    user = User.objects.get(username=request.session['username'])
    data = {
        "user": User.objects.get(id=user.id),
    }
    return render(request, 'travel_buddy/add.html', data)

def create(request):
    user = User.objects.get(username=request.session['username'])
    trip_info = Plan.objects.valid_plan(request.POST, user)
    if trip_info[0]: 
        return redirect('/travels')
    else: 
        for error in trip_info[1]:
            messages.add_message(request, messages.ERROR, error)
        return redirect('/travels/add')

def join(request, dest_id):
    this_user = User.objects.get(username=request.session['username'])
    this_trip = Plan.objects.get(id=dest_id) 
    this_trip.travelers.add(this_user)
    return redirect('/travels')

def destination(request, dest_id):
    user = User.objects.get(username=request.session['username'])
    data = {
        "user": User.objects.get(id=user.id),
        "trip": Plan.objects.get(id=dest_id),
        "users": Plan.objects.get(id=dest_id).travelers.all().exclude(id=user.id)
    }
    return render(request, 'travel_buddy/destination.html', data)


def logout(request):
    request.session.clear()
    return redirect('/')
