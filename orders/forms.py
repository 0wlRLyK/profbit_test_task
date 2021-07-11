import datetime

from django import forms


class DatetimeRangeForm(forms.Form):
    from_date = forms.DateTimeField(label="Начальные дата и время:",
                                    initial=datetime.datetime(year=2018, month=1, day=1, hour=9))
    to_date = forms.DateTimeField(label="Конечные дата и время:",
                                  initial=datetime.datetime(year=2018, month=1, day=1, hour=10))


class MaxItemsForm(DatetimeRangeForm):
    max_items = forms.ChoiceField(label="Количество товаров на странице:",
                                  widget=forms.Select(),
                                  choices=([('10', '10'), ('20', '20'), ('50', '50'), ('100', '100')]), initial='20',
                                  required=True, )
