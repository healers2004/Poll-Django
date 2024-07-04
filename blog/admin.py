from django.contrib import admin
from blog.models import Category, Comment, Post, ContactUsPageText

class CategoryAdmin(admin.ModelAdmin):
    pass

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'thumbnail_size', 'image_tag', 'created_on', 'last_modified')
    list_editable = ('thumbnail_size',)
    readonly_fields = ('image_tag',)

    def image_tag(self, obj):
        if obj.image:
            return f'<img src="{obj.get_thumbnail_url()}" style="max-width: 150px; max-height: 150px;" />'
        return 'No Image'
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True

class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'created_on', 'state')
    list_filter = ('state',)
    actions = ['approve_comments', 'reject_comments']

    def approve_comments(self, request, queryset):
        queryset.update(state=Comment.State.APPROVED)
    approve_comments.short_description = 'Approve selected comments'

    def reject_comments(self, request, queryset):
        queryset.update(state=Comment.State.REJECTED)
    reject_comments.short_description = 'Reject selected comments'


admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(ContactUsPageText)