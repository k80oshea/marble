# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import re
import bcrypt 
from datetime import datetime

NAME_REGEX = re.compile(r"^[a-zA-Z-' ]+$")
USER_REGEX = re.compile(r"^[a-zA-Z0-9-_@$*]+$")
PASS_REGEX = re.compile(r"^[a-zA-Z0-9.+_-]{8,}$")


class UserManager(models.Manager):
    def register(self, post_data):
        errors = []
        if len(post_data['name']) < 1:
            errors.append("Name cannot be left blank!")
        elif len(post_data['name']) < 3:
            errors.append("Name must be at least 3 characters long")
        if not NAME_REGEX.match(post_data['name']):
            errors.append("Invalid characters in Name")

        if len(post_data['username']) < 1:
            errors.append("Username cannot be left blank!")
        elif len(post_data['username']) < 3:
            errors.append("Username must be at least 3 characters long")
        if not USER_REGEX.match(post_data['username']):
            errors.append("Invalid characters in Username")
        check_user = User.objects.filter(username = post_data['username'].lower())
        if len(check_user) > 0:
            errors.append("Username already exists")

        if len(post_data['password']) < 1:
            errors.append("Password cannot be left blank!")
        elif len(post_data['password']) < 8:
            errors.append("Password should be at least 8 characters")
        if not PASS_REGEX.match(post_data['password']):
            errors.append("Invalid characters in Password")
        if post_data['password'] != post_data['confirm']:
            errors.append("Passwords do not match!")
                
        if len(errors) > 0:
            return (False, errors)
        else: 
            user = User.objects.create(
                name = post_data['name'],
                username = post_data['username'],
                password = bcrypt.hashpw(post_data['password'].encode(), bcrypt.gensalt())
            )
            return(True, user)

    def login(self, post_data):
        errors = []
        if len(post_data['password']) < 1:
            errors.append("Password cannot be left blank!")
        elif len(post_data['password']) < 8:
            errors.append("Password should be at least 8 characters")
        if not PASS_REGEX.match(post_data['password']):
            errors.append("Invalid characters in Password")

        if len(post_data['username']) < 1:
            errors.append("Username cannot be left blank!")
        elif len(post_data['username']) < 3:
            errors.append("Username must be at least 3 characters long")
        if not USER_REGEX.match(post_data['username']):
            errors.append("Invalid characters in Username")
        check_user = User.objects.filter(username = post_data['username'].lower())
        if len(check_user) == 0:
            errors.append("Username does not exist")

        else:
            user = check_user[0]
            if not bcrypt.checkpw(post_data["password"].encode(), user.password.encode()):
                errors.append("Invalid Password")

            if len(errors) > 0:
                return (False, errors)
            else: 
                return(True, user)

class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class PlanManager(models.Manager):
    def valid_plan(self, post_data, user):
        errors = []
        if len(post_data['dest']) < 1:
            errors.append("Destination cannot be left blank!")
        elif len(post_data['dest']) < 5:
            errors.append("Destination must be at least 5 characters long")

        if len(post_data['desc']) < 1:
            errors.append("Description cannot be left blank!")
        elif len(post_data['desc']) < 15:
            errors.append("Description must be at least 15 characters long")

        if len(post_data["start"]) < 1:
            errors.append("Please select a Start Date")
        else:
            start = datetime.strptime(post_data["start"], "%Y-%m-%d")
            if start < datetime.now():
                errors.append("Start Date must be in the future")

        if len(post_data["end"]) < 1:
            errors.append("Please select an End Date")
        else:
            end = datetime.strptime(post_data["end"], "%Y-%m-%d")
            if end < datetime.now():
                errors.append("Start Date must be in the future")
            elif end < start:
                errors.append("End Date cannot be before Start Date")

        if len(errors) > 0:
                return (False, errors)
        else: 
            trip = Plan.objects.create(
                destination = post_data['dest'],
                description = post_data['desc'],
                start_date = post_data['start'],
                end_date = post_data['end'],
                planner = User.objects.get(id=user.id),
            )
            trip.travelers.add(user)

            return(True, trip)       


class Plan(models.Model):
    destination = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    planner = models.ForeignKey(User, related_name="plans")
    travelers = models.ManyToManyField(User, related_name="trips")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = PlanManager()

