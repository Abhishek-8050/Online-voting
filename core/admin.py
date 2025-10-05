 

# Register your models here.
from django.contrib import admin
from .models import AdminUser, Candidate, Voter

# Register your models here
admin.site.register(AdminUser)
admin.site.register(Candidate)
admin.site.register(Voter)
