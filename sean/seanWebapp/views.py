from django.conf import settings
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.urls import reverse
from django.utils.encoding import force_bytes, force_text

import mimetypes
import os
import random, string

from seanWebapp.forms import UserForm, UserProfileForm, AddResourceForm, EditResourceForm
from seanWebapp.models import UserProfile, Log, Resource
from seanWebapp.tokens import account_activation_token

#import sys, os
#sys.path.append(os.path.join(os.getcwd(), ""))
from . import rasaAPI


# Author: 2327846P - Veronika
# Author: 2391564V - Charles
conversation = []
log_id = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
def home(request):
    global conversation
    
    if request.method == 'POST':
        # 1 -> Retrieve user message, append to conversation
        message = request.POST.get('message', '')
        conversation.append(("user", message))
        newLog, created = Log.objects.get_or_create(log_id=log_id)
        if newLog.log == None:
        	newLog.log = 'User: ' + message
        else:
        	newLog.log += '#User: ' + message
        # 2 -> Send user message to RASA agent
        reply = rasaAPI.message(str(message))
        # 3 -> Retrieve RASA agent response, append to conversation
        for r in reply:
            # Check if reply contains text
            if 'text' in r:
                conversation.append(("rasa", r['text']))
                newLog.log += '#SEAN: ' + r['text']
            # Check if reply contains an image
            if 'image' in r:
                conversation.append(("image", r['image']))
        newLog.save()
    
    else:
        # Reset conversation.
        conversation = [("rasa", "Welcome to SEAN!")]
    
        
    context_dict = {
        "title": "Welcome to SEAN!",
        "conversation" : conversation}
    
    return render(request, 'seanWebapp/home.html', context=context_dict)

def sendmessage(request):
    global conversation
    
    # AJAX call to add to conversation
    if request.method == 'POST':
        # 1 -> Retrieve user message, append to conversation
        message = request.POST.get('message', '')
        conversation.append(("user", message))
        # 2 -> Send user message to RASA agent
        reply = rasaAPI.message(str(message))
        # 3 -> Retrieve RASA agent response, append to conversation
        conversation.append(("rasa", reply['text']))
        
    return HttpResponse('')

# Author:2327846P - Veronika
def help(request):
	return render(request, 'seanWebapp/help.html', {})

# Author: 2327846P - Veronika
# This is the settings page. Cannot name it settings, due to import.
def setup(request):
	return render(request, 'seanWebapp/settings.html', {})

# Author: 2327846P - Veronika
def aboutUs(request):
	return render(request, 'seanWebapp/aboutUs.html', {})

# Author: 2327846P - Veronika
def publicResources(request):
	resource_list = Resource.objects.order_by('name')
	paginator = Paginator(resource_list, 10)
	page = request.GET.get('page', 1)
	if page != None:
		resources_all = paginator.page(page)
	else:
		resources_all = resource_list
	context_dict = {'resources': resources_all}
	return render(request, 'seanWebapp/publicResources.html', context_dict)

# Author: 2327846P - Veronika
def viewResource(request, resource_slug):
	resource = Resource.objects.get(slug=resource_slug)
	filePath = os.path.join(settings.MEDIA_DIR, resource.file.name)
	fs = FileSystemStorage()
	if fs.exists(resource.file.name):
		with fs.open(resource.file.name) as serveFile:
			mimeType, _ = mimetypes.guess_type(filePath)
			response = HttpResponse(serveFile, content_type=mimeType)
			response['Content-Disposition'] = "attachment; filename=%s" % resource.name
			return response
	else:
		return HttpResponseNotFound("Sorry, the file was not found.")
	return HttpResponse(os.path.join(settings.MEDIA_DIR, resource.file.name))

# Author: 2327846P - Veronika
def loginUser(request):
	message = None
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(username=username, password=password)

		if user:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect(reverse('staffHome'))
			else:
				message = "disabled"
				return render(request, 'seanWebapp/login.html', {'message': message})
		else:
			message = "invalid"
			return render(request, 'seanWebapp/login.html', {'message': message})

	else:
		return render(request, 'seanWebapp/login.html', {'message': message})

# Author: 2327846P - Veronika
@login_required
def logoutUser(request):
	logout(request)
	return HttpResponseRedirect(reverse('home'))

# Author: 2327846P - Veronika
@login_required
def staffHome(request):
	profile = UserProfile.objects.get(user=request.user)
	return render(request, 'seanWebapp/staffHome.html', {'profile': profile})

# Author: 2327846P - Veronika
@login_required
def createProfile(request):
	userPermission = UserProfile.objects.get(user=request.user).add_users
	if not userPermission:
		return HttpResponseRedirect(reverse('noPermission'))
	registered = None
	if request.method == 'POST':
		user_form = UserForm(data=request.POST)
		profile_form = UserProfileForm(data=request.POST)

		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()
			user.is_active = False
			# automatically generates a random password
			password = User.objects.make_random_password()
			user.set_password(password)
			user.save()
			profile = profile_form.save(commit=False)
			profile.user = user
			profile.save()
			registered = "success"
			currentSite = get_current_site(request)
			# Create email message
			subject = "Activate your SEAN chatbot staff account"
			message = render_to_string('seanWebapp/accountActivationEmail.html', {
				'user': user,
				'domain': currentSite.domain,
				'uid': urlsafe_base64_encode(force_bytes(user.pk)),
				'token': account_activation_token.make_token(user),
				})
			# Send activation email
			user.email_user(subject=subject, message=message)
		else:
			print(user_form.errors, profile_form.errors)
	else:
		user_form = UserForm()
		profile_form = UserProfileForm()
	return render(request, 'seanWebapp/createProfile.html',
				  {'user_form': user_form,
				   'profile_form': profile_form,
				    'registered': registered})

# Author: 2327846P - Veronika
def activate(request, uidb64, token):
	try:
		uid = force_text(urlsafe_base64_decode(uidb64))
		user = User.objects.get(pk=uid)
	except(TypeError, ValueError, OverflowError, User.DoesNotExist):
		user = None
	if user is not None and account_activation_token.check_token(user, token):
		# Activates and logs in the user.
		user.is_active = True
		user.save()
		login(request, user)
		return redirect('changePassword')
	else:
		# Invalid token (ex. already used).
		return redirect('noPermission')

# Author: 2327846P - Veronika
@login_required
def changePassword(request):
	message = None
	if request.method == 'POST':
		passForm = SetPasswordForm(data=request.POST, user=request.user)
		if passForm.is_valid():
			passForm.save()
			# Reauthenticates the user with new password.
			update_session_auth_hash(request, request.user)
			login(request, request.user)
			message = "success"
			return render(request, 'seanWebapp/changePassword.html', {'form': passForm,
				'message': message})
		else:
			message = "invalid"
			return render(request, 'seanWebapp/changePassword.html', {'form': passForm,
				'message': message})
	else:
		passForm = SetPasswordForm(user=request.user)
	return render(request, 'seanWebapp/changePassword.html', {'form': passForm,
		'message': message})

# Author: 2327846P - Veronika
@login_required
def manageResources(request):
	userPermission = UserProfile.objects.get(user=request.user).manage_resources
	if not userPermission:
		return HttpResponseRedirect(reverse('noPermission'))
	resource_list = Resource.objects.order_by('name')
	paginator = Paginator(resource_list, 10)
	page = request.GET.get('page', 1)
	if page != None:
		resources_all = paginator.page(page)
	else:
		resources_all = resource_list
	context_dict = {'resources': resources_all}
	return render(request, 'seanWebapp/manageResources.html', context_dict)

# Author: 2327846P - Veronika
@login_required
def addResource(request):
	userPermission = UserProfile.objects.get(user=request.user).manage_resources
	if not userPermission:
		return HttpResponseRedirect(reverse('noPermission'))
	# Handle the add resource form
	message = None
	resource = None
	if request.method == 'POST':
		resource_form = AddResourceForm(data=request.POST, files=request.FILES)
		if resource_form.is_valid():
			resource = resource_form.save(commit=True)
			if 'file' in request.FILES:
				resource.file = request.FILES['file']
			resource.save()
			message = "success"
		else:
			print(resource_form.errors)
	else:
		resource_form = AddResourceForm()
	context_dict = {'message': message, 'resource': resource, 'form': resource_form}
	return render(request, 'seanWebapp/addResource.html', context_dict)

# Author: 2327846P - Veronika
@login_required
def editResource(request, resource_slug):
	userPermission = UserProfile.objects.get(user=request.user).manage_resources
	if not userPermission:
		return HttpResponseRedirect(reverse('noPermission'))
	resource = Resource.objects.get(slug=resource_slug)
	message = None
	if request.method == 'POST':
		edit_form = EditResourceForm(data=request.POST, files=request.FILES)
		if edit_form.is_valid():
			if edit_form.data['name'] != None:
				resource.name = edit_form.data['name']
			if 'file' in request.FILES:
				resource.file = request.FILES['file']
			resource.save()
			message = "success"
		else:
			print(edit_form.errors)
	else:
		edit_form = EditResourceForm()
	context_dict = {'resource': resource, 'edit_form': edit_form, 'message': message}
	#return HttpResponse(resource)
	return render(request, 'seanWebapp/editResource.html', context_dict)

# Author: 2327846P - Veronika
@login_required
def deleteResource(request, resource_slug):
	userPermission = UserProfile.objects.get(user=request.user).manage_resources
	if not userPermission:
		return HttpResponseRedirect(reverse('noPermission'))
	resource = Resource.objects.get(slug=resource_slug)
	resource.delete()
	return redirect('manageResources')


# Author: 2133861W - Andrew
# Editted: 2327846P - Veronika
@login_required
def searchLogs(request):
	userPermission = UserProfile.objects.get(user=request.user).manage_logs
	if not userPermission:
		return HttpResponseRedirect(reverse('noPermission'))
	logs = Log.objects.order_by('conversation_time')
	paginator = Paginator(logs, 10)
	page = request.GET.get('page', 1)
	if page != None:
		logs_list = paginator.page(page)
	else:
		logs_list = logs
	context_dict = {'logs': logs_list}
	return render(request,'seanWebapp/manageLogs.html', context_dict)

# Author: 2133861W - Andrew
@login_required
def logDetail(request, log_id):
	userPermission = UserProfile.objects.get(user=request.user).manage_logs
	if not userPermission:
		return HttpResponseRedirect(reverse('noPermission'))
	log = Log.objects.get(slug=log_id)
	logMessages = log.log.split('#')
	context_dict = {'log': log, 'messages': logMessages}
	return  render(request,'seanWebapp/logDetail.html', context_dict)

# Author: 2327846P - Veronika
@login_required
def deleteLog(request, log_id):
	userPermission = UserProfile.objects.get(user=request.user).manage_logs
	if not userPermission:
		return HttpResponseRedirect(reverse('noPermission'))
	log = Log.objects.get(slug=log_id)
	log.delete()
	return redirect('searchLogs')

# Author: 2327846P - Veronika
# If the user attempts to enter a page they do not have permissions for.
def noPermission(request):
	return render(request, 'seanWebapp/noPermission.html', {})

# Author: 2327846P - Veronika
# Wrong page default response.
def wrongPage(request, exception):
	return render(request, 'seanWebapp/wrongPage.html', {})
