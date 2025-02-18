from django.contrib import admin
from .models.account import Account

# Register accounts app models
admin.site.register(Account)
