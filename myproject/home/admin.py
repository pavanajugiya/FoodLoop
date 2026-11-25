from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import (
    UserProfile, FoodListing, FoodRequest, PickupDelivery,
    BusinessNotification, CustomerOrder, DistributionRecord,
    ContactMessage, AppNotification, FoodEligibility, FoodMatch, FoodAnalytics
)


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_role', 'is_staff', 'is_superuser')

    def get_role(self, instance):
        if hasattr(instance, 'profile'):
            return instance.profile.get_role_display()
        return '-'
    get_role.short_description = 'Role'


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'business_name', 'ngo_name', 'phone', 'city', 'created_at')
    list_filter = ('role', 'city', 'state')
    search_fields = ('user__username', 'user__email', 'business_name', 'ngo_name', 'phone')


@admin.register(FoodListing)
class FoodListingAdmin(admin.ModelAdmin):
    list_display = ('food_name', 'business', 'category', 'quantity', 'unit', 'destination', 'status', 'created_at')
    list_filter = ('status', 'destination', 'category')
    search_fields = ('food_name', 'business__username', 'business__email')


@admin.register(FoodRequest)
class FoodRequestAdmin(admin.ModelAdmin):
    list_display = ('food_listing', 'requester_name', 'requester_type', 'requested_qty', 'status', 'created_at')
    list_filter = ('status', 'requester_type')
    search_fields = ('requester_name', 'food_listing__food_name')


@admin.register(PickupDelivery)
class PickupDeliveryAdmin(admin.ModelAdmin):
    list_display = ('food_listing', 'volunteer_name', 'recipient_name', 'scheduled_time', 'status', 'otp_code', 'tracking_code')
    list_filter = ('status',)
    search_fields = ('food_listing__food_name', 'volunteer_name', 'recipient_name', 'tracking_code')


@admin.register(CustomerOrder)
class CustomerOrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'customer', 'food_name', 'quantity', 'total_amount', 'status', 'payment_status', 'created_at')
    list_filter = ('status', 'payment_status')
    search_fields = ('order_number', 'customer__email', 'food_name')


@admin.register(DistributionRecord)
class DistributionRecordAdmin(admin.ModelAdmin):
    list_display = ('food_name', 'ngo', 'quantity', 'unit', 'beneficiaries_count', 'received_date', 'status')
    list_filter = ('status',)
    search_fields = ('food_name', 'ngo__email', 'location')


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'is_read', 'created_at')
    list_filter = ('is_read',)
    search_fields = ('name', 'email', 'subject', 'message')


@admin.register(AppNotification)
class AppNotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'notif_type', 'is_read', 'created_at')
    list_filter = ('notif_type', 'is_read')
    search_fields = ('title', 'message', 'user__email')


@admin.register(BusinessNotification)
class BusinessNotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'notif_type', 'is_read', 'created_at')
    list_filter = ('notif_type', 'is_read')
    search_fields = ('title', 'message', 'user__email')


@admin.register(FoodEligibility)
class FoodEligibilityAdmin(admin.ModelAdmin):
    list_display = ('food_item', 'is_eligible', 'eligibility_status', 'reason', 'checked_at')
    list_filter = ('is_eligible', 'eligibility_status')
    search_fields = ('food_item__food_name', 'reason')


@admin.register(FoodMatch)
class FoodMatchAdmin(admin.ModelAdmin):
    list_display = ('food_item', 'receiver_user', 'matched_quantity', 'match_score', 'status', 'matched_at')
    list_filter = ('status',)
    search_fields = ('food_item__food_name', 'receiver_user__username', 'receiver_user__email')


@admin.register(FoodAnalytics)
class FoodAnalyticsAdmin(admin.ModelAdmin):
    list_display = ('food_item', 'prepared_quantity', 'sold_quantity', 'donated_quantity', 'rescued_quantity', 'wasted_quantity', 'record_date')
    list_filter = ('record_date',)
    search_fields = ('food_item__food_name', 'remarks')

