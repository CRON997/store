from django.contrib import admin
from users.models import User,EmailVerification
from products.admin import BasketAdminInline


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    inlines = (BasketAdminInline,)


@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ('code','user','expiration')
    fields = ('code','user','expiration','created')
    readonly_fields = ('created',)