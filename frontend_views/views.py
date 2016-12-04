import json

from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.contrib.auth.models import User
from api.models import Category, Account
from api.forms import UpdateProfileImage
from django.conf import settings


from legislation import sunlightapi as sun
from utils.custom_decorators import beta_blocker, login_required, full_account

def base_view(request):
    if not request.user.is_authenticated():
        return TemplateResponse(request, 'static_templates/landing.html', {})

    a = Account.objects.get(user=request.user)
    if not a.beta_access:
        return HttpResponseRedirect('/beta')
    if not a.full_account:
        return HttpResponseRedirect('/setup')

    categories = [{'id': c.id, 'name': c.name} for c in Category.objects.all()]

    data = dict(
        categories=categories
    )

    return TemplateResponse(request, 'feed.html', {'data': json.dumps(data)})


@login_required
@beta_blocker
@full_account
def user_profile(request, username=None):
    if not username:
        return HttpResponseRedirect('/profile/{0}'.format(request.user))

    else:
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return HttpResponseRedirect('/404')

    return TemplateResponse(request, 'account.html', {'username': user,
                                                    'profile_image_form': UpdateProfileImage,
                                                    'google_map_api_key': settings.GOOGLE_API_KEY,
                                                    'sunlight_api_key': settings.SUNLIGHT_API_KEY })

@login_required
@beta_blocker
def user_setup(request):
    a = Account.objects.get(user=request.user)
    if a.full_account:
        return HttpResponseRedirect('/')
        #start temp rep rendering TODO: REMOVE THIS
    else:
        return TemplateResponse(request, 'user-setup.html', {'username': request.user.username,
                                                            'email': request.user.email,
                                                            'google_map_api_key': settings.GOOGLE_API_KEY,
                                                            'sunlight_api_key': settings.SUNLIGHT_API_KEY })



@login_required
@beta_blocker
@full_account
def issue_thread(request, thread_id=None):
    if not thread_id:
        return HttpResponseRedirect('/404')

    return TemplateResponse(request, 'thread.html', {'thread_id': thread_id})

@login_required
@beta_blocker
@full_account
def create_group(request):
	return TemplateResponse(request, 'newgroup.html', {})

@login_required
@beta_blocker
@full_account
def dbview(request):
	result = [{'id': c.id, 'name': c.name} for c in Category.objects.all()]

	return TemplateResponse(request, 'dbview.html', {'result': json.dumps(result)})

@login_required
@beta_blocker
@full_account
def add_civi(request):
	categories = [{'id': c.id, 'name': c.name} for c in Category.objects.all()]
	topics = [{'id': c.id, 'topic': c.topic} for c in Topic.objects.all()]

	return TemplateResponse(request, 'add_civi.html', {'categories': json.dumps(categories), 'topics': json.dumps(topics)})

def login_view(request):
    if request.user.is_authenticated():
        if request.user.is_active:
            return HttpResponseRedirect('/')

    return TemplateResponse(request, 'login.html', {})

def beta_view(request):
	return TemplateResponse(request, 'beta_blocker.html', {})

def declaration(request):
	return TemplateResponse(request, 'declaration.html', {})

def landing_view(request):
	return TemplateResponse(request, 'static_templates/landing.html', {})

def how_it_works_view(request):
	return TemplateResponse(request, 'static_templates/how_it_works.html', {})

def about_view(request):
	return TemplateResponse(request, 'static_templates/about.html', {})

def support_us_view(request):
	return TemplateResponse(request, 'static_templates/support_us.html', {})

def does_not_exist(request):
	return TemplateResponse(request, 'base/404.html', {})
