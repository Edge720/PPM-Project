from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class DateInput(forms.DateInput):
    input_type = 'date'

class DateForm(forms.Form):
    event_name = forms.CharField(label='Event_name', max_length=100)
    event_date = forms.DateField(widget = DateInput)

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name']

        #def clean_email(self):
            #email = self.cleaned_data.get('email')
            #if not email.endswith('police.uk'):
                #raise forms.ValidationError("Only .police.uk email addresses allowed")
            #return email
