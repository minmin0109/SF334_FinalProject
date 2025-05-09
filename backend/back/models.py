from django.db import models
from django.contrib.auth.models import User  
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User

class ProductManager(models.Manager):
    def flexible_lookup(self, product_id=None, name=None):
        if product_id:
            # ลองค้นหาด้วย ID หลัก
            try:
                return self.get(id=product_id)
            except self.model.DoesNotExist:
                # ถ้าไม่พบ ให้ค้นหาด้วยชื่อสินค้า
                if name:
                    # ค้นหาโดยใช้ icontains (ค้นหาแบบไม่สนใจตัวพิมพ์เล็ก/ใหญ่และค้นหาแบบบางส่วน)
                    return self.filter(name__icontains=name).first()
                
                # ถ้าไม่มีชื่อ สามารถค้นหาด้วยวิธีอื่นได้ เช่น slug, sku ฯลฯ
                # คุณสามารถเพิ่มตรงนี้ได้...
                
                # หากไม่พบด้วยวิธีอื่น ให้คืนค่า None
                return None
        elif name:
            # ถ้ามีแค่ชื่อ ค้นหาด้วยชื่อ
            return self.filter(name__icontains=name).first()
            
        # ถ้าไม่มีทั้ง ID และชื่อ ให้คืนค่า None
        return None

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)  # เพิ่มฟิลด์ description
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    category = models.CharField(max_length=255)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    objects = ProductManager()
    def __str__(self):
        return self.name

class Payment(models.Model):
    method = models.CharField(max_length=255)
    card_no = models.CharField(max_length=20, blank=True)
    expired = models.CharField(max_length=5)
    holder_name = models.CharField(max_length=500)
    payment_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_date = models.DateTimeField()

    def __str__(self):
        return f"{self.method} - {self.holder_name}"

class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.FloatField()
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=25)
    order_date = models.DateTimeField()
    shipping_name = models.CharField(max_length=255, blank=True, null=True)
    shipping_address = models.TextField(blank=True, null=True)
    shipping_city = models.CharField(max_length=100, blank=True)
    shipping_state = models.CharField(max_length=100, blank=True)
    shipping_postal = models.CharField(max_length=20, blank=True)
    shipping_country = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Order #{self.id} - {self.customer}"

class ProductOrder(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    total_price = models.FloatField()
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    def save(self, *args, **kwargs):
        # ตัด stock ตอนสร้าง (เฉพาะตอนสร้างใหม่เท่านั้น)
        if not self.pk:  # แปลว่าเป็นการสร้างใหม่ ไม่ใช่อัปเดต
            if self.product.stock < self.quantity:
                raise ValueError(f"Not enough stock for {self.product.name}")
            self.product.stock -= self.quantity
            self.product.save()
        super().save(*args, **kwargs)

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    def total_price(self):
        return self.product.price * self.quantity

