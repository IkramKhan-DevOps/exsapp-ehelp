from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import (
    UserAdmin as BaseUserAdmin
)
# from .forms import (
#     UserAdminCreationForm,
#     UserAdminCsehangeForm
# )
from .models import (
    Account,
    Country,
    City,
    Request_Category,
    Response,
    Request as RequestModel,
    Queue)


# class UserAdmin(BaseUserAdmin):
#     # The forms to add and change user instances
#     form = UserAdminChangeForm
#     add_form = UserAdminCreationForm
#
#     # The fields to be used in displaying the User model.
#     # These override the definitions on the base UserAdmin
#     # that reference specific fields on auth.User.
#     list_display = ('email', 'full_name', 'phone', 'admin', 'staff', 'active', 'created', 'updated')
#     list_filter = ('admin', 'staff', 'active')
#     fieldsets = (
#         (None, {'fields': ('email', 'password')}),
#         ('Personal info', {'fields': ('profile', 'full_name', 'code', 'phone')}),
#         ('Statistics', {'fields': ('points', 'requests', 'responses', 'hearts', 'subscribers')}),
#         ('Permissions', {'fields': ('admin', 'staff', 'active', 'is_confirmed')}),
#     )
#     # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
#     # overrides get_fieldsets to use this attribute when creating a user.
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('email', 'password1', 'password2')}
#          ),
#     )
#     search_fields = ('email',)
#     ordering = ('email',)
#     filter_horizontal = ()


admin.site.register(Account)
admin.site.register(Response)
admin.site.register(Country)
admin.site.register(City)
admin.site.register(Request_Category)
admin.site.register(RequestModel)
admin.site.register(Queue)
