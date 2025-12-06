from django.contrib import admin
from .models import Post

class PostAdmin(admin.ModelAdmin): 
    list_display = ('user', 'slug', 'update')
    search_fields = ('slug', 'user')
    list_filter = ('updated',)
    prepopulated_fields = {'slug' : ('body',)}
    raw_id_fields = ('user',)
admin.site.register(Post)
