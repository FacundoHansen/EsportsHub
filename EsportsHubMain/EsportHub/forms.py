from django import forms
from django.contrib.auth.forms import UserCreationForm ,  UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=254,help_text='Requerido. Ingrese una dirección de correo válida.')
    first_name = forms.CharField(max_length=30,required=True,help_text='Requerido. Ingrese su nombre.')
    last_name = forms.CharField(max_length=30,required=True,help_text='Requerido. Ingrese su apellido.' )
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name']
    username = forms.CharField(label='Nombre de usuario')
    password1 = forms.CharField(label='Contraseña')
    password2 = forms.CharField(label='Confirmación de contraseña')

class UserProfileUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class PasswordChangeForm(PasswordChangeForm):
    new_password1 = forms.CharField(
        label="Nueva Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False,
    )
    new_password2 = forms.CharField(
        label="Confirmación de Nueva Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False,
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('old_password')  # Elimina el campo 'old_password' del formulario
    def clean(self):
        cleaned_data = super().clean()
        if 'old_password' in self.cleaned_data:
            del self.cleaned_data['old_password']
        return cleaned_data
    
class UserProfileUpdateExtendedForm(UserChangeForm):
    date_joined = forms.DateField(disabled=True)  # Campo date_joined no editable
    last_login = forms.DateTimeField(disabled=True)  # Campo last_login no editable
    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','date_joined','last_login')

