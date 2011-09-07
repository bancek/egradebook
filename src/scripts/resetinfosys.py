from infosys.models import *
import os
os.system('python manage.py reset infosys')
ids = [x['id'] for x in User.objects.all()[1:].values('id')]
User.objects.filter(id__in=ids).delete()