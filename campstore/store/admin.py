from django.contrib import admin
from .models import Category, Product, Order, OrderItem


class StatusFilter(admin.SimpleListFilter):
    title = 'Status'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return (
            ('active', 'Active'),
            ('sold_out', 'Sold Out'),
            ('waiting_approval', 'Waiting Approval'),
            ('deleted', 'Deleted'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'active':
            return queryset.filter(status='active')
        if self.value() == 'sold_out':
            return queryset.filter(status='sold_out')
        if self.value() == 'waiting_approval':
            return queryset.filter(status='waiting_approval')
        if self.value() == 'deleted':
            return queryset.filter(status='deleted')


@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ("title", "slug")
    search_fields = ("title",)
    list_filter = ("title",)


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ("category", "user", "title", "description", "price", "image", "quantity", "status")
    search_fields = ("category", "user", "title", "status")
    list_filter = (StatusFilter,)
    ordering = ("category", "title",)
    fieldsets = (
        ('General Information', {
            'fields': ('title', 'description', 'price'),
        }),
    )


@admin.register(Order)
class OrderModelAdmin(admin.ModelAdmin):
    list_display = ("created_by", "first_name", "last_name", "address", "post_code", "phone_number", )
    search_fields = ("created_by", "first_name", 'last_name')
    list_filter = ("created_by",)
    ordering = ("first_name", "last_name",)


@admin.register(OrderItem)
class OrderItemModelAdmin(admin.ModelAdmin):
    list_display = ("order", "product", "price", "quantity")
    search_fields = ("order", "product",)
    list_filter = ("product",)