from django.contrib import admin
from api.post.models import Post
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ["pkid", "author", "views"]
    list_display_links = ["pkid", "author"]

admin.site.register(Post,PostAdmin)