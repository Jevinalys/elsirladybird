from django.contrib import admin
from .models import Customer,Product,Service,Sale,Booking,Profile

# Register your models here.
admin.site.register(Profile)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        'first_name','second_name','phone','email_address','debt','loyalty_points'
    )

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'product_name','product_description','units','total_units','unit_buying_price','unit_selling_price'
    )

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        'service_name','service_description','service_price'
    )

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
     list_display = (
        'customer_name','phone','services','amount','date_paid'
    )
     #def get_services(self, obj):
        # return ", ".join([Service.service_name for Service in obj.services.all()])

    

     #def customer_name(self, obj):
        #return obj.Customer.first_name

    # customer_name.admin_order_field = 'customer_name'

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'first_name','second_name','phone_number','book_date','book_time'
    )