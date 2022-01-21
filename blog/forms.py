from django import forms
from django_jalali.admin import widgets
choices_view =(
    ("تعداد بازدید(زیاد به کم)", "تعداد بازدید(زیاد به کم)"),
    ("تعداد بازدید(کم به زیاد)", "تعداد بازدید(کم به زیاد)"),
    ("تاریخ (جدید به قدیمی)","تاریخ (جدید به قدیمی)"),
    ("تاریخ (قدیمی به جدید)","تاریخ (قدیمی به جدید)"),

)
  

class FilterForm(forms.Form):
    filter = forms.ChoiceField( choices=choices_view, required=False, label='بر اساس')
    start_date = forms.DateField(label=('تاریخ شروع'), required=False,
            widget=widgets.AdminjDateWidget
        )
    finish_date =forms.DateField(label=('تاریخ پایان'), required=False,
            widget=widgets.AdminjDateWidget
        )