from django.contrib.auth import logout, login
from django.http import HttpResponseRedirect, Http404

from dacks.views import render
from auth.forms import LoginForm
from authprofile.views import profile_url

@render('auth/login.html')
def login_view(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(profile_url(request.user))
    
    form = LoginForm(data=request.POST or None)
    
    if form.is_valid():
        if not form.cleaned_data['remember']:
            request.session.set_expiry(0)

        login(request, form.get_user())
        
        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()
        
        if 'next' in request.REQUEST:
            next = request.REQUEST['next']
            if next.startswith('/'):
                return HttpResponseRedirect(next)
        
        return HttpResponseRedirect(profile_url(request.user))
    
    request.session.set_test_cookie()
    
    return locals()

def logout_view(request):
    if not request.user:
        return Http404
    
    logout(request)
    
    next = request.GET.get('next', '')
    
    if not next or not next.startswith('/'):
        next = '/'
    
    return HttpResponseRedirect(next)
