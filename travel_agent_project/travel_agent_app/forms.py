from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import modelformset_factory, inlineformset_factory
from .models import TravelAgent, Website, TravelPackage, PackageMedia

class TravelAgentSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15, required=False)
    agency_name = forms.CharField(max_length=100, required=False)
    
    class Meta:
        model = TravelAgent
        fields = ('username', 'email', 'password1', 'password2', 'phone_number', 'agency_name')

class TravelAgentLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class WebsiteForm(forms.ModelForm):
    class Meta:
        model = Website
        fields = ('name', 'url')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'url': forms.URLInput(attrs={'class': 'form-control'}),
        }

class TravelPackageForm(forms.ModelForm):
    class Meta:
        model = TravelPackage
        fields = ('title', 'destination', 'duration_days', 'price', 'description')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'destination': forms.TextInput(attrs={'class': 'form-control'}),
            'duration_days': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

class PackageMediaForm(forms.ModelForm):
    class Meta:
        model = PackageMedia
        fields = ('media_type', 'file')  # Removed 'caption'
        widgets = {
            'media_type': forms.Select(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),  # Changed to FileInput
        }

PackageMediaFormSet = inlineformset_factory(
    TravelPackage,
    PackageMedia,
    form=PackageMediaForm,
    extra=1,
    can_delete=True
)

class PackageSearchForm(forms.Form):
    destination = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    duration_days = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    max_price = forms.DecimalField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control'}))