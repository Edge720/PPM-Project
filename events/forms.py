from django import forms

class DateInput(forms.DateInput):
    input_type = 'date'

class DateForm(forms.Form):
    event_name = forms.CharField(label='Event_name', max_length=100)
    event_date = forms.DateField(widget = DateInput)
