from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    content_type = models.ForeignKey(ContentType, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    profile = generic.GenericForeignKey ('content_type', 'object_id')

    def is_dijak(self):
        from infosys.models import Dijak
        return isinstance(self.profile, Dijak)
    
    def is_stars(self):
        from infosys.models import Stars
        return isinstance(self.profile, Stars)
    
    def is_profesor(self):
        from infosys.models import Profesor
        return isinstance(self.profile, Profesor)
    
    def is_admin(self):
        return self.user.is_staff

    class Meta:
        verbose_name = 'User profile'
        verbose_name_plural = 'User profiles'

    def __unicode__(self):
        return unicode(self.user)

def on_user_save(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(on_user_save, User)
