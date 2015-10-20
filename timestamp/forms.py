from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import MakeUser, RecordTime
# from crispy_forms.helper import FormHelper


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name',
                   'last_name',
                   'email',
                   'username',
                   'password1',
                   'password2',
                   ]

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['job_title'] = forms.CharField()
        self.fields['terms_and_conditions'] = forms.BooleanField(
            error_messages={'required': 'You must accept the terms and conditions to proceed with use of this program.'},
            help_text='Check the box if you have fully read and agree the Terms and Conditions policy')
        self.fields['photo'] = forms.ImageField()

    def save(self):
        new_user = super(UserCreationForm, self).save()

        job_title = self.cleaned_data['job_title']
        terms = self.cleaned_data['terms_and_conditions']
        photo = self.cleaned_data['photo']
        MakeUser.objects.create(
            user=new_user,
            job_title=job_title,
            accept_term_condition=terms,
            photo=photo,
        )

        confirmed_pass = self.cleaned_data['password1']
        new_user.set_password(confirmed_pass)
        new_user.save()
        return new_user