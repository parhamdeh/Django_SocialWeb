from django.contrib import admin
from .models import Post, Comment, Vote

class PostAdmin(admin.ModelAdmin): 
    list_display = ('user', 'slug', 'update')
    search_fields = ('slug', 'user')
    list_filter = ('updated',)
    prepopulated_fields = {'slug' : ('body',)}
    raw_id_fields = ('user',)

class CommentAdmi(admin.ModelAdmin):
    list_display = ['user', 'post', 'created', 'is_reply']
    raw_id_fields = ['user', 'post', 'reply']


admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Vote)
