from django.contrib import admin

from blog.models import *
# Register your models here.


class ContentImageInline(admin.TabularInline):
    model = ContentImage
    extra = 1


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1


class ReplyInline(admin.TabularInline):
    model = Reply
    extra = 1


class PostAdmin(admin.ModelAdmin):
    inlines = [
        ContentImageInline,
        CommentInline,
    ]


class CommentAdmin(admin.ModelAdmin):
    inlines = [
        ReplyInline,
    ]


admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Post, PostAdmin)
admin.site.register(ContentImage)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Reply)
