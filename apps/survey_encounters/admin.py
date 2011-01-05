from django.contrib import admin

from survey_encounters.models import Answer, Question, QALink, Form

class QALinkInline(admin.TabularInline):
    model = QALink
    extra = 5

class FormAdmin(admin.ModelAdmin):
    inlines = [QALinkInline]
admin.site.register(Form, FormAdmin)

admin.site.register(Answer)
admin.site.register(Question)
admin.site.register(QALink)
