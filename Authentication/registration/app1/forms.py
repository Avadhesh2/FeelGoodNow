from django import forms
from .models import UserData


class UserInputForm(forms.ModelForm):
    class Meta:
        model = UserData
        fields = ['weight', 'gender', 'height',
                  'activity_level', 'sleeping_hours', 'age']
