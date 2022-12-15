from django.contrib import admin
from api.services.models import Rating,Comment,Favorite,Reaction
# Register your models here.
admin.site.register(Rating)
admin.site.register(Comment)
admin.site.register(Favorite)
admin.site.register(Reaction)
