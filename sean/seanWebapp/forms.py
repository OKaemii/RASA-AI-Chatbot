from django import forms
from django.contrib.auth.models import User

from seanWebapp.models import UserProfile, Resource

# Author: 2327846P - Veronika
class UserForm(forms.ModelForm):
	username = forms.CharField()
	email = forms.EmailField()

	class Meta:
		model = User
		fields = ('username', 'email', )

	def clean_email(self):
		email = self.cleaned_data['email']
		if User.objects.filter(email=email).exists():
			raise forms.ValidationError("Please  use a different email, this one is already in use.")
		return email

# Author: 2327846P - Veronika
class UserProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ('add_users', 'manage_logs', 'manage_resources')

# Author: 2327846P - Veronika
class AddResourceForm(forms.ModelForm):
	name = forms.CharField(max_length=128)
	file = forms.FileField()

	class Meta:
		model = Resource
		fields = ('name', 'file')

# Author:2327846P - Veronika
class EditResourceForm(forms.ModelForm):
	name = forms.CharField(max_length=128)
	file = forms.FileField(required=False)

	class Meta:
		model = Resource
		fields = ('name', 'file')