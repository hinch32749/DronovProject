from django.contrib import admin

from .models import Machine, Spare, Kit, Note


class MachineAdmin(admin.ModelAdmin):
    list_display = ('name', 'notes')


class SpareAdmin(admin.ModelAdmin):
    list_display = ('name',)


class KitAdmin(admin.ModelAdmin):
    list_display = ('machine', 'spare', 'count')


class NoteAdmin(admin.ModelAdmin):
    list_display = ('content', 'content_type', 'content_object')


admin.site.register(Machine, MachineAdmin)
admin.site.register(Spare, SpareAdmin)
admin.site.register(Kit, KitAdmin)
admin.site.register(Note, NoteAdmin)