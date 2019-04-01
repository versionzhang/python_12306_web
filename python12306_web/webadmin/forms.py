from django import forms

from webadmin.models import BasicConfig

class BasicConfigForm(forms.ModelForm):
    class Meta:
        model = BasicConfig
        fields = '__all__'
