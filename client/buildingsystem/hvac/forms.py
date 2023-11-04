from django import forms

class SAForm(forms.Form):
    sa_temp = forms.FloatField(label = "Supply Air Temperature")