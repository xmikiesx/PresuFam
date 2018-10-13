from django.contrib import admin
from .models import MyUser, Income, Expense, Category
from django.contrib.auth.admin import UserAdmin


class MyUserAdmin(UserAdmin):
    fieldsets = ()
    add_fieldsets = (
        (None, {'fields', ('email', 'password1', 'password2'), })
    )
    list_display = ('email', 'nombre', 'is_active', 'is_staff',)
    search_fields = ('nombre', 'email')
    ordering = ('nombre',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'create_on')


class IncomeAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'monto')


class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'monto')


admin.site.register(MyUser, MyUserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Income, IncomeAdmin)
admin.site.register(Expense, ExpenseAdmin)