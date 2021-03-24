from django.contrib import admin

# Register your models here.
from post.models import Post, PostImage, PostComment, PostReaction, StoryComment, StoryReaction, StoryImage, Story

admin.site.register(Post)
admin.site.register(PostImage)
admin.site.register(PostReaction)
admin.site.register(PostComment)

admin.site.register(Story)
admin.site.register(StoryImage)
admin.site.register(StoryReaction)
admin.site.register(StoryComment)