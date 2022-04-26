from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from authapp.models import UserProfile
import django.forms as forms


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, item in self.fields.items():
            item.widget.attrs['class'] = f'form-profile {name}'


class RegisterForm(UserCreationForm):
    class Meta:
        model = UserProfile
        fields = ('username', 'first_name', 'last_name',
                  'gender', 'role', 'date_birth',
                  'password1', 'password2', 'email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, item in self.fields.items():
            item.widget.attrs['class'] = f'form-profile {name}'
            item.help_text = ''


class ProfileForm(UserChangeForm):
    class Meta:
        model = UserProfile
        fields = ('username', 'first_name', 'last_name',
                  'email', 'avatar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, item in self.fields.items():
            item.widget.attrs['class'] = f'form-profile {name}'
            item.help_text = ''
            if name == 'password':
                item.widget = forms.HiddenInput()

    