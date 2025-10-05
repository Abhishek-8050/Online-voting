from django import forms
from .models import AdminForm

class AdminFormForm(forms.ModelForm):
    class Meta:
        model = AdminForm
        fields = ['name', 'phone', 'email']   # unique_code नहीं दिखाना
