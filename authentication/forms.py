from django import forms
from django.utils.translation import gettext_lazy as _

ACCOUNT_TYPE = (
  ('USER', 'User'),
  ('STAFF', 'Staff'),
  ('ADMIN', 'Admin')
)

class SignupForm(forms.Form):
  first_name = forms.CharField(max_length=200)
  last_name = forms.CharField(max_length=200)
  password = forms.CharField(max_length=300, widget=forms.PasswordInput())
  password_again = forms.CharField(max_length=300, widget=forms.PasswordInput())
  username = forms.CharField(max_length=300)
  email = forms.EmailField(max_length=300)
  account_type = forms.ChoiceField(choices=ACCOUNT_TYPE)

  help_texts = {
    'email': _('Please enter your personal email id')
  }
  labels = {
    'first_name': _('First Name'),
    'last_name': _('Last Name')
  }
  error_messages = {
    'first_name': {
      'max_length': _('The first name is more than 200 characters!')
    },
    'last_name': {
      'max_length': _('The last name is more than 200 characters!')
    }
  }


  def __init__(self, *args, **kwargs):
    super(SignupForm, self).__init__(*args, **kwargs)
    for field in iter(self.fields):
      self.fields[field].widget.attrs.update({
        'class': 'form-control',
        'placeholder': None
      })
      # if field != 'have_watched' and field != 'on_watchlist' and field != 'is_franchise':
      # else:
      #   self.fields[field].widget.attrs.update({
      #     'class': 'form-check-input'
      # })



