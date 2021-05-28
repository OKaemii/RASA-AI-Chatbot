from django.contrib import auth
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

import os

from sean import settings
from seanWebapp.forms import UserForm, UserProfileForm, AddResourceForm, EditResourceForm
from seanWebapp.models import Resource, Log, UserProfile

# Functions for adding models to the database.
# Author: 2327846P - Veronika
def addResource(name, file):
	resource = resource = Resource(name=name, file=file)
	resource.save()
	return resource

# Author: 2327846P - Veronika
def addLog(log_id, guid, topic_discussed, log):
	log = Log(log_id=log_id, guid=guid, topic_discussed=topic_discussed, log=log)
	log.save()
	return log

# Author: 2327846P - Veronika
def addUser(username, email, password):
	user = User.objects.create(username=username, email=email)
	user.set_password(password)
	user.save()
	return user

# Author: 2327846P - Veronika
def addUserProfile(user, add_users, manage_logs, manage_resources):
	profile = UserProfile(user=user, add_users=add_users, manage_logs=manage_logs,
		manage_resources=manage_resources)
	profile.save()
	return profile


# Ensures that all models are saved as expected, to ensure that we handle the information well.
class ModelTests(TestCase):
	# Author: 2327846P - Veronika
	def testResource(self):
		resource = addResource(name='test file', file='testFile.pdf')
		self.assertEqual(resource.name, 'test file')
		self.assertEqual(resource.slug,  'test-file')
		self.assertIn('testFile', resource.file.name)
		self.assertEqual(str(resource), 'test file')

	# Author: 2327846P - Veronika
	def testLog(self):
		log = addLog(log_id='123456789', guid='2327846P', topic_discussed='test', log='This is a test.')
		self.assertEqual(log.log_id, '123456789')
		self.assertEqual(log.guid, '2327846P')
		self.assertEqual(log.topic_discussed, 'test')
		self.assertEqual(log.slug, '123456789')
		self.assertIn('test', log.log)
		self.assertEqual(str(log), '123456789')

	# Author: 2327846P - Veronika
	def testUserProfile(self):
		user = addUser(username='autoTest', email='seanchatbotTest@gmail.com', password='psswrd')
		profile = addUserProfile(user=user, add_users=True, manage_logs=False, manage_resources=True)
		self.assertEqual(profile.user.username, 'autoTest')
		self.assertEqual(profile.user.email, 'seanchatbotTest@gmail.com')
		self.assertEqual(profile.add_users, True)
		self.assertEqual(profile.manage_logs, False)
		self.assertEqual(profile.manage_resources, True)
		self.assertEqual(str(profile), 'autoTest')


# Tests that the page loaded successfully not logged in. These pages have to load under any circumstances.
class ViewTestsLoad(TestCase):
	# Author: 2327846P - Veronika
	def testHomeLoad(self):
		response = self.client.get(reverse('home'))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'seanWebapp/home.html')

	# Author: 2327846P - Veronika
	def testHelpLoad(self):
		response = self.client.get(reverse('help'))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'seanWebapp/help.html')

	# Author: 2327846P - Veronika
	def testSetupLoad(self):
		response = self.client.get(reverse('setup'))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'seanWebapp/settings.html')

	# Author: 2327846P - Veronika
	def testAboutUsLoad(self):
		response = self.client.get(reverse('aboutUs'))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'seanWebapp/aboutUs.html')

	# Author: 2327846P - Veronika
	def testViewResourceLoad(self):
		response = self.client.get(reverse('publicResources'))
		self.assertEqual(response.status_code, 200)

	# Author: 2327846P - Veronika
	def testNoPermissionLoad(self):
		response = self.client.get(reverse('noPermission'))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'seanWebapp/noPermission.html')


# Tests the passing of appropriate data to the context of the pages not logged in.
# Also tests the successful loading of the pages in question.
class ViewTestsFunctionLoggedOut(TestCase):
	# Author: 2327846P - Veronika
	def setUp(self):
		self.user = addUser(username='autoTest', email='seanchatbotTest@gmail.com', password='psswrd')
		self.profile = addUserProfile(user=self.user, add_users=True, manage_logs=False,
			manage_resources=True)

	# Author: 2327846P - Veronika
	def testPublicResourcesEmpty(self):
		response = self.client.get(reverse('publicResources'))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'seanWebapp/publicResources.html')
		self.assertQuerysetEqual(response.context['resources'], [])

	# Author: 2327846P - Veronika
	def testPublicResources(self):
		addResource(name='test file 1', file='testFile.pdf')
		addResource(name='test file 2', file='testFile.pdf')
		addResource(name='test file 3', file='testFile.pdf')
		response = self.client.get(reverse('publicResources'))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'seanWebapp/publicResources.html')
		self.assertContains(response, 'test file 1')
		self.assertContains(response, 'test file 2')
		self.assertContains(response, 'test file 3')
		resourceNum = len(response.context['resources'])
		self.assertEqual(resourceNum, 3)

	# Author: 2327846P - Veronika
	# Incorrect login details.
	def testLoginUserFalse(self):
		response = self.client.post('loginUser', {'username': self.profile.user.username,
			'password': 'incorrectPassword'})
		self.assertEqual(response.status_code, 200)
		user = auth.get_user(self.client)
		self.assertFalse(user.is_authenticated)

	# Author: 2327846P - Veronika
	# Profile not active.
	def testLoginUserNotActive(self):
		self.user.is_active = False
		response = self.client.post('loginUser', {'username': self.profile.user.username,
			'password': self.profile.user.password})
		self.assertEqual(response.status_code, 200)
		user = auth.get_user(self.client)
		self.assertFalse(user.is_authenticated)

	# Author: 2327846P - Veronika
	# No user logged in. Redirect to login.
	def testLogoutUserFalse(self):
		user = auth.get_user(self.client)
		self.assertFalse(user.is_authenticated)
		response = self.client.get(reverse('logoutUser'))
		self.assertEqual(response.status_code, 302)
		user = auth.get_user(self.client)
		self.assertFalse(user.is_authenticated)

	# Author: 2327846P - Veronika
	# Successfully finds the file, but as there is none to open, fails.
	def testViewReousceTrue(self):
		resource = addResource(name='test file', file='testFile.pdf')
		response = self.client.get(reverse('viewResource', args=('test-file',)))
		self.assertEqual(response.status_code, 404)

	# Author:2327846P - Veronika
	# Not logged in user attempts to enter restricted access page.
	def testLoginRedirectCreateProfile(self):
		response = self.client.get(reverse('createProfile'))
		self.assertEqual(response.status_code, 302)

	# Author:2327846P - Veronika
	# Not logged in user attempts to enter restricted access page.
	def testLoginRedirectResources(self):
		response = self.client.get(reverse('manageResources'))
		self.assertEqual(response.status_code, 302)

	# Author:2327846P - Veronika
	# Not logged in user attempts to enter restricted access page.
	def testLoginRedirectLogs(self):
		response = self.client.get(reverse('searchLogs'))
		self.assertEqual(response.status_code, 302)

	# Author: 2327846P - Veronika
	# Completely incorrect URL.
	def testWrongPage(self):
		response = self.client.get('something/wrong/not-existing')
		# Load the wrong page, not error out.
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'seanWebapp/wrongPage.html')


# Tests the passing of appropriate data to the context of the pages logged in.
# Also tests the successful loading of the pages in question.
class ViewTestsFunctionLoggedIn(TestCase):
	# Author: 2327846P - Veronika
	def setUp(self):
		self.user = addUser(username='autoTest', email='seanchatbotTest@gmail.com', password='psswrd')
		self.profile = addUserProfile(user=self.user, add_users=True, manage_logs=True,
			manage_resources=True)
		self.client.force_login(self.user)

	# Author: 2327846P - Veronika
	# User logged in. Redirect to home.
	def testLogoutUserTrue(self):
		user = auth.get_user(self.client)
		self.assertTrue(user.is_authenticated)
		response = self.client.get(reverse('logoutUser'))
		self.assertEqual(response.status_code, 302)
		user = auth.get_user(self.client)
		self.assertFalse(user.is_authenticated)

	# Author: 2327846P - Veronika
	def testStaffHomeLoad(self):
		response = self.client.get(reverse('staffHome'))
		self.assertTrue(response.status_code, 200)
		self.assertTemplateUsed(response, 'seanWebapp/staffHome.html')

	# Author: 2327846P - Veronika
	def testCreateProfileLoad(self):
		response = self.client.get(reverse('createProfile'))
		self.assertTrue(response.status_code, 200)
		self.assertTemplateUsed(response, 'seanWebapp/createProfile.html')
		self.assertIsInstance(response.context['user_form'], UserForm)
		self.assertIsInstance(response.context['profile_form'], UserProfileForm)

	# Author: 2327846P - Veronika
	def testManageResourcesLoadFull(self):
		addResource(name='test file 1', file='testFile.pdf')
		addResource(name='test file 2', file='testFile.pdf')
		addResource(name='test file 3', file='testFile.pdf')
		response = self.client.get(reverse('manageResources'))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'seanWebapp/manageResources.html')
		self.assertContains(response, 'test file 1')
		self.assertContains(response, 'test file 2')
		self.assertContains(response, 'test file 3')
		resourceNum = len(response.context['resources'])
		self.assertEqual(resourceNum, 3)

	# Author: 2327846P - Veronika
	def testManageResourcesLoadEmpty(self):
		response = self.client.get(reverse('manageResources'))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'seanWebapp/manageResources.html')
		self.assertNotContains(response, 'test file 1')
		self.assertNotContains(response, 'test file 2')
		self.assertNotContains(response, 'test file 3')
		resourceNum = len(response.context['resources'])
		self.assertEqual(resourceNum, 0)

	# Author: 2327846P - Veronika
	def testDeleteResource(self):
		addResource(name='test file 1', file='testFile.pdf')
		response = self.client.get(reverse('manageResources'))
		resourceNum = len(response.context['resources'])
		self.assertEqual(resourceNum, 1)
		response = self.client.get(reverse('deleteResource', args=('test-file-1',)))
		self.assertEqual(response.status_code, 302)
		response = self.client.get(reverse('manageResources'))
		resourceNum = len(response.context['resources'])
		self.assertEqual(resourceNum, 0)

	# Author: 2327846P - Veronika
	def testSearchLogsLoadFull(self):
		addLog(log_id='123456789', guid='2327846P', topic_discussed='test', log='This is a test.')
		addLog(log_id='987654321', guid='2327846P', topic_discussed='test', log='This is a test.')
		addLog(log_id='123498765', guid='2327846P', topic_discussed='test', log='This is a test.')
		response = self.client.get(reverse('searchLogs'))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'seanWebapp/manageLogs.html')
		self.assertContains(response, '123456789')
		self.assertContains(response, '987654321')
		self.assertContains(response, '123498765')
		logNum = len(response.context['logs'])
		self.assertEqual(logNum, 3)

	# Author: 2327846P - Veronika
	def testSearchLogsLoadEmpty(self):
		response = self.client.get(reverse('searchLogs'))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'seanWebapp/manageLogs.html')
		self.assertNotContains(response, '123456789')
		self.assertNotContains(response, '987654321')
		self.assertNotContains(response, '123498765')
		logNum = len(response.context['logs'])
		self.assertEqual(logNum, 0)

	# Author:2327846P - Veronika
	def testLogDetail(self):
		addLog(log_id='123456789', guid='2327846P', topic_discussed='test', log='This is a test.')
		response = self.client.get(reverse('logDetail', args=('123456789',)))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'seanWebapp/logDetail.html')
		self.assertContains(response, '123456789')

	# Author: 2327846P - Veronika
	def testDeleteLog(self):
		addLog(log_id='123456789', guid='2327846P', topic_discussed='test', log='This is a test.')
		response = self.client.get(reverse('searchLogs'))
		logNum = len(response.context['logs'])
		self.assertEqual(logNum, 1)
		response = self.client.get(reverse('deleteLog', args=('123456789',)))
		self.assertEqual(response.status_code, 302)
		response = self.client.get(reverse('searchLogs'))
		logNum = len(response.context['logs'])
		self.assertEqual(logNum, 0)


# Tests access denied to permission requiring pages.
class ViewTestsFunctionLoggedInNoPermission(TestCase):
	# Author: 2327846P - Veronika
	def setUp(self):
		self.user = addUser(username='autoTest', email='seanchatbotTest@gmail.com', password='psswrd')
		self.profile = addUserProfile(user=self.user, add_users=False, manage_logs=False,
			manage_resources=False)
		self.client.force_login(self.user)

	# Author:2327846P - Veronika
	def testPermissionRedirectCreateProfile(self):
		response = self.client.get(reverse('createProfile'))
		self.assertEqual(response.status_code, 302)

	# Author:2327846P - Veronika
	def testPermissionRedirectResources(self):
		response = self.client.get(reverse('manageResources'))
		self.assertEqual(response.status_code, 302)

	# Author:2327846P - Veronika
	def testPermissionRedirectAddResource(self):
		response = self.client.get(reverse('addResource'))
		self.assertEqual(response.status_code, 302)

	# Author:2327846P - Veronika
	def testPermissionRedirectEditResource(self):
		addResource(name='test file 1', file='testFile.pdf')
		response = self.client.get(reverse('editResource', args=('test-file-1',)))
		self.assertEqual(response.status_code, 302)

	# Author:2327846P - Veronika
	def testPermissionRedirectDeleteResource(self):
		addResource(name='test file 1', file='testFile.pdf')
		response = self.client.get(reverse('deleteResource', args=('test-file-1',)))
		self.assertEqual(response.status_code, 302)

	# Author:2327846P - Veronika
	def testPermissionRedirectLogs(self):
		response = self.client.get(reverse('searchLogs'))
		self.assertEqual(response.status_code, 302)

	# Author:2327846P - Veronika
	def testPermissionRedirectLogDetail(self):
		addLog(log_id='123456789', guid='2327846P', topic_discussed='test', log='This is a test.')
		response = self.client.get(reverse('logDetail', args=('123456789',)))
		self.assertEqual(response.status_code, 302)

	# Author:2327846P - Veronika
	def testPermissionRedirectDeleteLog(self):
		addLog(log_id='123456789', guid='2327846P', topic_discussed='test', log='This is a test.')
		response = self.client.get(reverse('deleteLog', args=('123456789',)))
		self.assertEqual(response.status_code, 302)


# Testing of the forms and their input.
class FormTests(TestCase):
	# Author: 2327846P - Veronika
	def setUp(self):
		self.user = addUser(username='autoTest', email='seanchatbotTest@gmail.com', password='psswrd')
		self.profile = addUserProfile(user=self.user, add_users=True, manage_logs=False,
			manage_resources=True)
		self.client.force_login(self.user)

	# Author: 2327846P - Veronika
	def testUserFormValid(self):
		user_data = {'username': 'testNew', 'email': 'seanchatbotTestNew@gmail.com'}
		user_form = UserForm(data=user_data)
		self.assertTrue(user_form.is_valid())

	# Author: 2327846P - Veronika
	def testUserFormInvalid(self):
		user_data = {'username': '', 'email': ''}
		user_form = UserForm(data=user_data)
		self.assertFalse(user_form.is_valid())

	# Author: 2327846P - Veronika
	def testUserFormInvalidDuplicate(self):
		user_data = {'username': 'newUser', 'email': 'seanchatbotTest@gmail.com'}
		user_form = UserForm(data=user_data)
		self.assertFalse(user_form.is_valid())

	# Author: 2327846P - Veronika
	def testUserProfileFormValid(self):
		profile_data = {'add_users': True, 'manage_logs': True, 'manage_resources': False}
		profile_form = UserProfileForm(data=profile_data)
		self.assertTrue(profile_form.is_valid())

	# Author: 2327846P - Veronika
	def testAddResourceFormValid(self):
		upload_file = open(os.path.join(settings.STATIC_DIR, 'images/send.png'), 'rb')
		resource_data = {'name': 'test new file'}
		file_data = {'file': SimpleUploadedFile(upload_file.name, upload_file.read())}
		resource_form = AddResourceForm(data=resource_data, files=file_data)
		self.assertTrue(resource_form.is_valid())

	# Author: 2327846P - Veronika
	def testAddResourceFormInvalid(self):
		resource_data = {'name': ''}
		file_data = {'file': ''}
		resource_form = AddResourceForm(data=resource_data, files=file_data)
		self.assertFalse(resource_form.is_valid())

	# Author: 2327846P - Veronika
	def testEditResourceFormValid(self):
		upload_file = open(os.path.join(settings.STATIC_DIR, 'images/send.png'), 'rb')
		resource_data = {'name': 'test new file'}
		file_data = {'file': SimpleUploadedFile(upload_file.name, upload_file.read())}
		resource_form = EditResourceForm(data=resource_data, files=file_data)
		self.assertTrue(resource_form.is_valid())

	# Author: 2327846P - Veronika
	def testEditResourceFormInvalid(self):
		resource_data = {'name': ''}
		file_data = {'file': ''}
		resource_form = EditResourceForm(data=resource_data, files=file_data)
		self.assertFalse(resource_form.is_valid())