from django.contrib import admin

# Register your models here.
from Footballer.models import *

admin.site.register(Position)
admin.site.register(Footballer)
admin.site.register(Referee)
admin.site.register(Game)
admin.site.register(Division)
admin.site.register(Club)