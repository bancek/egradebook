from functools import wraps

from django.http import Http404

from authprofile.models import UserProfile

def dijak_required(func):
    @wraps(func)
    def decorated(request, *args, **kwargs):
        try:
            profile = request.user.get_profile()
            if profile.is_dijak():
                return func(request, *args, **kwargs)
            else:
                raise Http404
        except UserProfile.DoesNotExist:
            raise Http404
    return decorated

def stars_required(func):
    @wraps(func)
    def decorated(request, *args, **kwargs):
        try:
            profile = request.user.get_profile()
            if profile.is_stars():
                return func(request, *args, **kwargs)
            else:
                raise Http404
        except UserProfile.DoesNotExist:
            raise Http404
    return decorated

def profesor_required(func):
    @wraps(func)
    def decorated(request, *args, **kwargs):
        try:
            profile = request.user.get_profile()
            if profile.is_profesor():
                return func(request, *args, **kwargs)
            else:
                raise Http404
        except UserProfile.DoesNotExist:
            raise Http404
    return decorated