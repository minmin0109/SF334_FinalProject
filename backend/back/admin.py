from django.contrib import admin
from .models import User, Product, Payment, Order, ProductOrder ,CartItem 

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'category')  # แสดงคอลัมน์ที่ต้องการ
    search_fields = ('name', 'category')  # เพิ่มช่องค้นหาสำหรับฟิลด์ name และ category

admin.site.register(Product, ProductAdmin)
admin.site.register(Payment)
admin.site.register(Order)
admin.site.register(ProductOrder)
admin.site.register(CartItem)