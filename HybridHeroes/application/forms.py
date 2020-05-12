# accounts.forms.py
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField, UserCreationForm
from .models import Account, Request


class FormUserProfile(forms.ModelForm):
    class Meta:
        model = Account
        fields = (
            'profile',
            'full_name',
            'code',
            'about',
        )
        labels = {
            'profile': 'Profile Image',
            'full_name': 'Full Name',
            'code': 'Quote',
            'about': 'About Yourself'
        }
        help_texts = {
            'profile': 'Image must be a size of 150 * 150',
            'code': 'like: be a reason of someone to smile, aspiring beam of light',
            'about': 'Come on tell us something about yourself, your requester/heroes needs to know you'
        }


class FormUserContact(forms.ModelForm):
    class Meta:
        model = Account
        fields = (
            'phone',
            'whatsapp',
            'facebook',
            'instagram',
            'address',
            'country',
            'city',
        )
        labels = {
            'phone': 'Mobile Number',
            'whatsapp': 'Whatsapp Number',
            'facebook': 'Facebook Username',
            'instagram': 'Instagram Username',
            'address': 'Address',
            'country': 'Country',
            'city': 'City',
        }


class FormRequest(forms.ModelForm):
    class Meta:
        model = Request
        fields = (
            'desc',
            'request_category',
            'address',
            'city',
            'country',
            'supply',
        )
        labels = {
            'desc': 'Description',
            'request_category': 'Request Category',
            'address': 'Address',
            'city': 'City',
            'country': 'Country',
            'supply': 'Need Supply',
        }
        help_texts = {
            'desc': 'Please describe your problem briefly for better response',
            'request_category': 'select the type of help you need like money, food, education etc',
            'address': 'default address will the address related to your profile but you can change '
                       'request address here',
            'supply': 'help will be supplied to  your address by your hero'
        }


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254,
                             help_text='email address must be unique, your account will be confirmed and '
                                       'registered for it')

    class Meta:
        model = Account
        fields = ('full_name', 'email', 'password1', 'password2')


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('email',)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = Account.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("email is taken")
        return email

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2


# class UserAdminCreationForm(forms.ModelForm):
#     """
#     A form for creating new users. Includes all the required
#     fields, plus a repeated password.
#     """
#     password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
#     password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
#
#     class Meta:
#         model = User
#         fields = ('email',)
#
#     def clean_password2(self):
#         # Check that the two password entries match
#         password1 = self.cleaned_data.get("password1")
#         password2 = self.cleaned_data.get("password2")
#         if password1 and password2 and password1 != password2:
#             raise forms.ValidationError("Passwords don't match")
#         return password2
#
#     def save(self, commit=True):
#         # Save the provided password in hashed format
#         user = super(UserAdminCreationForm, self).save(commit=False)
#         user.set_password(self.cleaned_data["password1"])
#         if commit:
#             user.save()
#         return user


# class UserAdminChangeForm(forms.ModelForm):
#     """A form for updating users. Includes all the fields on
#     the user, but replaces the password field with admin's
#     password hash display field.
#     """
#     password = ReadOnlyPasswordHashField()
#
#     class Meta:
#         model = User
#         fields = ('email', 'password', 'active', 'admin')
#
#     def clean_password(self):
#         # Regardless of what the user provides, return the initial value.
#         # This is done here, rather than on the field, because the
#         # field does not have access to the initial value
#         return self.initial["password"]
