from django.contrib.auth.forms import UserCreationForm
from django.forms import forms

from persons.models import Person


class SignUpForm(UserCreationForm):
    #email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = Person
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2', 'document_number', 'university',
                  'country', 'relation', 'user_type', 'affiliation', )
