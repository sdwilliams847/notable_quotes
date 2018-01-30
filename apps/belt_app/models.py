from __future__ import unicode_literals
from django.db import models
from datetime import datetime
import bcrypt


class UserManager(models.Manager):
    def register(self, name, alias, dob, password, confirm_password):
        
        response = {
            "errors": [],
            "user": None,
            "valid": True
        }
        
        today = datetime.now()
        Yr = datetime.strftime(today,'%Y')
        Month = datetime.strftime(today,'%m')
        Day = datetime.strftime(today,'%d')
        newYr = int(Yr) - 10

        ageLimit = ("{}-{}-{}").format(newYr,Month,Day)

        if len(name) < 3:
            response["valid"] = False
            response["errors"].append("First name is required")
        if len(alias) < 3:
            response["valid"] = False
            response["errors"].append("First name is required")
        else:
            alias_list = User.objects.filter(alias=alias.lower())
            if len(alias_list) > 0:
                response["valid"] = False
                response["errors"].append("alias already exists")
        if str(dob) > str(ageLimit):
            response["valid"] = False
            response["errors"].append("You must be at least 10 years old to post on this site.")
        
        if len(password) < 8:
            response["valid"] = False
            response["errors"].append("Password must be at least 8 characters")
        if confirm_password != password:
            response['valid'] = False
            response["errors"].append("Passwords do not match")
        if response['valid']:
            User.objects.create(
                name=name,
                alias=alias.lower(),
                dob=dob,
                password=bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            )
            response['user'] = User.objects.get(alias=alias.lower())
            
        return response

    def login(self, alias, password):
        
        response = {
            "errors": [],
            "user": None,
            "valid": True
        }
        
        if len(alias) < 3:
            response["valid"] = False
            response["errors"].append("alias is incorrect.")

        else:
            alias_list = User.objects.filter(alias=alias.lower())
            if len(alias_list) == 0:
                response["valid"] = False
                response["errors"].append("alias or password does not match.")
        if len(password) < 8:
            response["valid"] = False
            response["errors"].append("Password must be at least 8 characters")
        if response["valid"]:
            if bcrypt.checkpw(password.encode(), alias_list[0].password.encode()):
                response["user"] = alias_list[0]
            else:
                response["valid"] = False
                response["errors"].append("Incorrect Password")
        return response

class QuoteManager(models.Manager):
    def new_quote(self, author, text, posted_by):
        response = {
            "errors": [],
            "quote": None,
            "valid": True
        }
        if len(author) < 3:
            response["valid"] = False
            response["errors"].append("An author name is required and must be longer than 3 characters.")
        if len(text) < 10:
            response["valid"] = False
            response["errors"].append("The quote must be longer than 10 characters.")
        
        if response['valid']:
            Quote.objects.create(
                author=author,
                text=text,
                posted_by=posted_by,
            )

        return response

    def new_favorite(self, quote, user):
        fave = Favorite.objects.create(
            quote=quote,
            user=user,
        )

        return fave

    def delete_favorite(self, id):
        Favorite.objects.get(id=id).delete()

        return
    
    def delete_quote(self, id):
        Quote.objects.get(id=id).delete()

        return


class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    dob = models.DateField(auto_now_add=False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = UserManager()


class Quote(models.Model):
    author = models.CharField(max_length=255)
    text = models.CharField(max_length=1000)
    posted_by = models.ForeignKey(User, related_name="poster")

    objects = QuoteManager()

class Favorite(models.Model):
    user = models.ForeignKey(User, related_name="favorited_quotes")
    quote = models.ForeignKey(Quote, related_name="favorited_quotes")

    objects = QuoteManager()