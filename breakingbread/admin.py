from django.contrib import admin
from breakingbread.models import *

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Recipe)
admin.site.register(Review)
admin.site.register(Report)
admin.site.register(Cuisine)
admin.site.register(Image)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('username', 'description', 'rating', 'created', 'active')
    list_filter = ('active', 'created')
    search_fields = ('username', 'description')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)