from django.contrib.auth import views as auth_views
from django.urls import path

from seanWebapp import views

# Author: 2327846P - Veronika
urlpatterns = [
	# general
	path('', views.home, name='home'),
	#path('', views.sendmessage), # AJAX 
	path('help/', views.help, name='help'),
	path('settings/', views.setup, name='setup'),
	path('about_us/', views.aboutUs, name='aboutUs'),
	path('resources/', views.publicResources, name='publicResources'),
	path('resources/<slug:resource_slug>/', views.viewResource, name='viewResource'),

	# account related
	path('login/', views.loginUser, name='loginUser'),
	path('logout/', views.logoutUser, name='logoutUser'),

	# staff
	path('staff/', views.staffHome, name='staffHome'),

	# staff create profile
	path('staff/create_profile/', views.createProfile, name='createProfile'),
	path('staff/activate/<slug:uidb64>/<slug:token>)/', views.activate, name='activate'),
	path('staff/change_password/', views.changePassword, name='changePassword'),

	# staff resources
	path('staff/manage_resources/', views.manageResources, name='manageResources'),
	path('staff/manage_resources/add/', views.addResource, name='addResource'),
	path('staff/manage_resources/edit/<slug:resource_slug>/', views.editResource, name='editResource'),
	path('staff/manage_resources/delete/<slug:resource_slug>/', views.deleteResource, name='deleteResource'),

	# staff logs
	path('staff/logs/', views.searchLogs, name='searchLogs'),
	path('staff/logs/<slug:log_id>/', views.logDetail, name='logDetail'),
	path('staff/logs/delete/<slug:log_id>/', views.deleteLog, name='deleteLog'),

	# no permission/error
	path('no_permission/', views.noPermission, name='noPermission'),
]
