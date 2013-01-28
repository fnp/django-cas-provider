from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus': 'autofocus',
                                                          'max_length': '255'}))
    password = forms.CharField(widget=forms.PasswordInput())
    service = forms.CharField(widget=forms.HiddenInput, required=False)

    def __init__(self, *args, **kwargs):
        # renew = kwargs.pop('renew', None)
        # gateway = kwargs.pop('gateway', None)
        request = kwargs.pop('request', None)
        super(LoginForm, self).__init__(*args, **kwargs)
        self.request = request


class MergeLoginForm(LoginForm):
    username = forms.CharField(max_length=255, widget=forms.HiddenInput)
