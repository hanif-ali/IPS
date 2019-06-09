from django.contrib import admin
from vote.models import Poll, House, Vote, Candidate, Grade, Student
# Register your models here.

admin.site.register(Grade)
admin.site.register(Student)
admin.site.register(Poll)
admin.site.register(House)
admin.site.register(Vote)
admin.site.register(Candidate)
