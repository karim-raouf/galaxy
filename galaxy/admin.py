from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(User)
admin.site.register(Subscription)
admin.site.register(Account)
admin.site.register(Organization)
admin.site.register(Product)
admin.site.register(Cart)