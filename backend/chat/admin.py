from django.contrib import admin
from guardian.admin import GuardedModelAdmin
# Register your models here.
from chat.models import Room


class RoomAdmin(GuardedModelAdmin):
    pass
    # prepopulated_fields = {"slug": ("title",)}
    # list_display = ('title', 'slug', 'created_at')
    # search_fields = ('title', 'content')
    # ordering = ('-created_at',)
    # date_hierarchy = 'created_at'

admin.site.register(Room, GuardedModelAdmin)