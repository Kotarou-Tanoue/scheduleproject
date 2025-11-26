import datetime
from django import forms
from .models import SchedulePost

class ContactForm(forms.Form):
    name = forms.CharField(label = 'お名前')
    email = forms.EmailField(label = 'メールアドレス')
    title = forms.CharField(label = '件名')
    message = forms.CharField(label = 'メッセージ', widget = forms.Textarea)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['placeholder'] = 'お名前を入力して下さい'
        self.fields['name'].widget.attrs['class'] = 'form-control'

        self.fields['email'].widget.attrs['placeholder'] = 'メールアドレスを入力して下さい'
        self.fields['email'].widget.attrs['class'] = 'form-control'

        self.fields['title'].widget.attrs['placeholder'] = 'タイトルを入力して下さい'
        self.fields['title'].widget.attrs['class'] = 'form-control'

        self.fields['message'].widget.attrs['placeholder'] = 'メッセージを入力して下さい'
        self.fields['message'].widget.attrs['class'] = 'form-control'

class SchedulePostForm(forms.ModelForm):
    class Meta:
        model = SchedulePost
        fields = ['title', 'start_date', 'end_date', 'category', 'location_at', 'comment']

        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'タイトルを入力', 'class': 'form-control'}),
            'start_date': forms.widgets.SelectDateWidget,
            'end_date': forms.widgets.SelectDateWidget,
            'category' : forms.widgets.CheckboxSelectMultiple,
            'location_at': forms.TextInput(attrs={'placeholder': '場所を入力', 'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'placeholder': 'コメントを入力', 'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['start_date'].initial = datetime.date.today()
        self.fields['end_date'].initial = datetime.date.today()

class CalendarForm(forms.Form):
    start_date = forms.IntegerField(required=True)
    end_date = forms.IntegerField(required=True)