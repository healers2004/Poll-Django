from django.contrib import admin
from blog.models import Category, Comment, Post

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
    pass

admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)