from django.http import HttpResponseRedirect
from django.contrib.auth.views import redirect_to_login

from authprofile.views import profile_url

def home(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(profile_url(request.user))
    else:
        return redirect_to_login(request.path)
