from django.contrib import admin

from .models import CustomUser, Task, Project, Hiring


admin.site.register(CustomUser)
admin.site.register(Task)
admin.site.register(Project)
admin.site.register(Hiring)
