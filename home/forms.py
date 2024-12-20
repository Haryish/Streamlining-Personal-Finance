# forms.py
from django import forms

class MonthSelectionForm(forms.Form):
    MONTH_CHOICES = [
        ('01', 'January'),
        ('02', 'February'),
        ('03', 'March'),
        ('04', 'April'),
        ('05', 'May'),
        ('06', 'June'),
        ('07', 'July'),
        ('08', 'August'),
        ('09', 'September'),
        ('10', 'October'),
        ('11', 'November'),
        ('12', 'December'),
    ]

    # Add a ChoiceField to select a month
    month = forms.ChoiceField(choices=MONTH_CHOICES, label='Select Month', required=True)
