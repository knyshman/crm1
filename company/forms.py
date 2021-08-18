from django.forms.models import inlineformset_factory
from .models import Company, CompanyEmail, CompanyManager, Phone
from django import forms


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = '__all__'


ManagerFormSet = inlineformset_factory(Company, CompanyManager, fields='__all__', can_delete=True)
PhoneFormset = inlineformset_factory(Company, Phone, fields='__all__', extra=3, can_delete=True)
EmailFormSet = inlineformset_factory(Company, CompanyEmail, fields='__all__', extra=3, can_delete=True)