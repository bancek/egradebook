from django.core.urlresolvers import reverse

def profile_url(user):
    profile = user.get_profile()
    
    if profile is None:
        return
    
    if profile.is_dijak():
        return reverse('dijak')
    
    elif profile.is_stars():
        return reverse('stars')
    
    elif profile.is_profesor():
        return reverse('profesor')
    
    elif profile.is_admin():
        return reverse('admin:index')
