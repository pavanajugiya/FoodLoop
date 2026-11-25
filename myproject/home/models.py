from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone



class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('business', 'Food Business'),
        ('ngo', 'NGO / Receiver'),
        ('customer', 'Customer'),
        ('volunteer', 'Volunteer'),
    )

    business_name = models.CharField(max_length=200, blank=True, null=True)
    business_type = models.CharField(max_length=50, blank=True, null=True, default='Hotel')
    ngo_name = models.CharField(max_length=200, blank=True, null=True)
    ngo_type = models.CharField(max_length=50, blank=True, null=True, default='NGO')
    daily_capacity_kg = models.IntegerField(default=200)
    requirements = models.TextField(blank=True, null=True, default='Cooked meals, vegetarian preferred, no expired items')
    vehicle_type = models.CharField(max_length=50, blank=True, null=True, default='Two-Wheeler')
    vehicle_number = models.CharField(max_length=50, blank=True, null=True, default='GJ 01 AB 1234')
    is_available = models.BooleanField(default=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=4.9)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    pincode = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email or self.user.username} - {self.get_role_display()}"


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)
    else:
        if hasattr(instance, 'profile'):
            instance.profile.save()


class FoodListing(models.Model):
    DESTINATION_CHOICES = (
        ('DONATE', 'Donate to NGO (Free)'),
        ('SELL', 'Sell at Discount'),
    )
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('available', 'Available'),
        ('matched', 'Matched'),
        ('pickup_pending', 'Pickup Pending'),
        ('in_transit', 'In Transit'),
        ('delivered', 'Delivered'),
        ('sold', 'Sold'),
        ('wasted', 'Wasted'),
        ('cancelled', 'Cancelled'),
    )
    CATEGORY_CHOICES = (
        ('Cooked Meal', 'Cooked Meal'),
        ('Bakery', 'Bakery'),
        ('Raw Vegetables', 'Raw Vegetables & Fruits'),
        ('Dairy', 'Dairy'),
        ('Beverages', 'Beverages'),
        ('Packaged Food', 'Packaged Food'),
        ('Other', 'Other'),
    )

    business = models.ForeignKey(User, on_delete=models.CASCADE, related_name='food_listings')
    food_name = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Cooked Meal')
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=20, default='kg')
    prep_time = models.DateTimeField()
    expiry_time = models.DateTimeField()
    condition = models.CharField(max_length=255, blank=True, null=True, default='Freshly prepared, sealed containers')
    destination = models.CharField(max_length=20, choices=DESTINATION_CHOICES, default='DONATE')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    is_eligible = models.BooleanField(default=True)
    matched_recipient = models.CharField(max_length=255, blank=True, null=True)
    assigned_volunteer = models.CharField(max_length=255, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.food_name} ({self.quantity} {self.unit}) - {self.get_status_display()}"


class FoodRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('declined', 'Declined'),
        ('completed', 'Completed'),
    )
    food_listing = models.ForeignKey(FoodListing, on_delete=models.CASCADE, related_name='requests')
    requester = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='food_requests')
    requester_name = models.CharField(max_length=255)
    requester_type = models.CharField(max_length=50, default='NGO')
    requester_contact = models.CharField(max_length=50, blank=True, null=True)
    requested_qty = models.DecimalField(max_digits=10, decimal_places=2)
    message = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Request by {self.requester_name} for {self.food_listing.food_name}"


class PickupDelivery(models.Model):
    STATUS_CHOICES = (
        ('scheduled', 'Volunteer Assigned'),
        ('in_transit', 'In Transit'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )
    food_listing = models.OneToOneField(FoodListing, on_delete=models.CASCADE, related_name='pickup')
    volunteer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='pickups')
    volunteer_name = models.CharField(max_length=255, default='Ravi Shah')
    volunteer_phone = models.CharField(max_length=50, default='+91 98765 43210')
    recipient_name = models.CharField(max_length=255, default='Ahmedabad Food Bank')
    recipient_address = models.CharField(max_length=255, default='Navrangpura, Ahmedabad')
    pickup_address = models.CharField(max_length=255, default='Hotel Rajmahal, S.G. Highway, Ahmedabad')
    tracking_code = models.CharField(max_length=50, blank=True, null=True, db_index=True)
    distance_km = models.DecimalField(max_digits=5, decimal_places=1, default=2.5)
    scheduled_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    otp_code = models.CharField(max_length=6, default='4928')
    pickup_otp = models.CharField(max_length=6, default='3841', help_text='Food business side OTP for volunteer pickup')
    delivery_otp = models.CharField(max_length=6, default='5829', help_text='NGO / Customer side OTP for delivery completion')
    delivered_at = models.DateTimeField(null=True, blank=True)
    delivery_notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.tracking_code:
            self.tracking_code = f"TRK-{self.id:04d}"
            PickupDelivery.objects.filter(pk=self.pk).update(tracking_code=self.tracking_code)

    def __str__(self):
        return f"Pickup for {self.food_listing.food_name} by {self.volunteer_name}"


class CustomerOrder(models.Model):
    STATUS_CHOICES = (
        ('placed', 'Order Placed'),
        ('confirmed', 'Confirmed'),
        ('ready', 'Ready for Pickup'),
        ('in_transit', 'Out for Delivery'),
        ('delivered', 'Delivered / Completed'),
        ('cancelled', 'Cancelled'),
    )
    order_number = models.CharField(max_length=50, unique=True, db_index=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer_orders')
    food_listing = models.ForeignKey(FoodListing, on_delete=models.SET_NULL, null=True, blank=True, related_name='customer_orders')
    food_name = models.CharField(max_length=255)
    business_name = models.CharField(max_length=255, default='Hotel Rajmahal')
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=1.0)
    unit = models.CharField(max_length=20, default='kg')
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    delivery_type = models.CharField(max_length=20, choices=(('pickup', 'Self Pickup'), ('delivery', 'Home Delivery')), default='pickup')
    delivery_address = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='placed')
    payment_method = models.CharField(max_length=50, default='UPI / Online')
    payment_status = models.CharField(max_length=20, default='Paid')
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=255, blank=True, null=True)
    otp_code = models.CharField(max_length=6, default='4829')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.business_name:
            self.business_name = 'Hotel Rajmahal'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.order_number} - {self.food_name} ({self.customer.email})"


class DistributionRecord(models.Model):
    ngo = models.ForeignKey(User, on_delete=models.CASCADE, related_name='distribution_records')
    food_listing = models.ForeignKey(FoodListing, on_delete=models.SET_NULL, null=True, blank=True)
    food_name = models.CharField(max_length=255)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=20, default='kg')
    provider_name = models.CharField(max_length=255, default='Hotel Rajmahal')
    volunteer_name = models.CharField(max_length=255, default='Ravi Shah')
    beneficiaries_count = models.IntegerField(default=50)
    location = models.CharField(max_length=255, default='Ahmedabad Shelter & Community Center')
    received_date = models.DateTimeField()
    status = models.CharField(max_length=30, default='Delivered')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-received_date']

    def save(self, *args, **kwargs):
        if not self.provider_name:
            self.provider_name = 'Hotel Rajmahal'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.food_name} distributed by {self.ngo.username} ({self.beneficiaries_count} people)"


class ContactMessage(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True, null=True)
    subject = models.CharField(max_length=200, blank=True, null=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.email}): {self.subject or 'Message'}"


class AppNotification(models.Model):
    TYPE_CHOICES = (
        ('match', 'Match'),
        ('volunteer', 'Volunteer'),
        ('delivery', 'Delivery'),
        ('expiry', 'Expiry'),
        ('request', 'Request'),
        ('order', 'Order'),
        ('info', 'General'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='app_notifications')
    title = models.CharField(max_length=255)
    message = models.TextField()
    notif_type = models.CharField(max_length=30, choices=TYPE_CHOICES, default='info')
    link = models.CharField(max_length=255, blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}: {self.title}"


class BusinessNotification(models.Model):
    TYPE_CHOICES = (
        ('match', 'Match'),
        ('volunteer', 'Volunteer'),
        ('delivery', 'Delivery'),
        ('expiry', 'Expiry'),
        ('request', 'Request'),
        ('info', 'General'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='business_notifications')
    food_listing = models.ForeignKey(FoodListing, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255)
    message = models.TextField(blank=True, null=True)
    notif_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='info')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}: {self.title}"


class FoodEligibility(models.Model):
    STATUS_CHOICES = (
        ('DONATION', 'Donation'),
        ('SALE', 'Sale'),
        ('COMMUNITY', 'Community Distribution'),
        ('DISPOSAL', 'Disposal'),
    )
    food_item = models.ForeignKey(FoodListing, on_delete=models.CASCADE, related_name='eligibilities')
    is_eligible = models.BooleanField(default=True)
    eligibility_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DONATION')
    reason = models.CharField(max_length=300, blank=True, null=True)
    checked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-checked_at']
        verbose_name = 'Food Eligibility'
        verbose_name_plural = 'Food Eligibilities'

    def __str__(self):
        return f"{self.food_item.food_name} - {'Eligible' if self.is_eligible else 'Unsuitable'} ({self.eligibility_status})"


class FoodMatch(models.Model):
    STATUS_CHOICES = (
        ('PROPOSED', 'Proposed'),
        ('ACCEPTED', 'Accepted'),
        ('REJECTED', 'Rejected'),
        ('COMPLETED', 'Completed'),
    )
    food_item = models.ForeignKey(FoodListing, on_delete=models.CASCADE, related_name='matches')
    receiver_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='food_matches')
    distance_km = models.DecimalField(max_digits=8, decimal_places=2, default=2.5)
    matched_quantity = models.DecimalField(max_digits=10, decimal_places=2)
    match_score = models.DecimalField(max_digits=5, decimal_places=2, default=90.0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PROPOSED')
    matched_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-matched_at']
        verbose_name = 'Food Match'
        verbose_name_plural = 'Food Matches'

    def __str__(self):
        return f"Match: {self.food_item.food_name} -> {self.receiver_user.username} ({self.matched_quantity} {self.food_item.unit})"


class FoodAnalytics(models.Model):
    food_item = models.ForeignKey(FoodListing, on_delete=models.SET_NULL, null=True, blank=True, related_name='analytics_records')
    prepared_quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    sold_quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    donated_quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    rescued_quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    wasted_quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    record_date = models.DateField(default=timezone.now)
    remarks = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        ordering = ['-record_date']
        verbose_name = 'Food Analytics Record'
        verbose_name_plural = 'Food Analytics Records'

    def __str__(self):
        return f"Analytics {self.record_date}: Rescued {self.rescued_quantity}kg / Wasted {self.wasted_quantity}kg"




