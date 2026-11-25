import os
import django
from datetime import timedelta
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.contrib.auth.models import User
from home.models import UserProfile, FoodListing, FoodRequest, PickupDelivery, BusinessNotification

# Find or ensure business user
user = User.objects.filter(email='pavanfb@gmail.com').first()
if not user:
    user = User.objects.filter(username='pavanfb@gmail.com').first()
if not user:
    user = User.objects.create_user(
        username='pavanfb@gmail.com',
        email='pavanfb@gmail.com',
        password='Password123!',
        first_name='Pavan',
        last_name='FB'
    )

profile, _ = UserProfile.objects.get_or_create(user=user)
profile.role = 'business'
profile.business_name = 'Hotel Rajmahal'
profile.business_type = 'Hotel & Restaurant'
profile.phone = '+91 98765 12345'
profile.address = '123 Ring Road, Near Vastrapur Lake'
profile.city = 'Ahmedabad'
profile.state = 'Gujarat'
profile.pincode = '380015'
profile.save()

now = timezone.now()

# Clear previous data for clean state if needed
FoodListing.objects.filter(business=user).delete()
BusinessNotification.objects.filter(user=user).delete()

# 12 listings as shown in overview stat card (8 donated/sold, 3 pending pickup/matched, 1 wasted)
listings_data = [
    {
        "food_name": "Dal Makhani + Rice",
        "category": "Cooked Meal",
        "quantity": 15.0,
        "unit": "kg",
        "prep_time": now - timedelta(hours=3),
        "expiry_time": now + timedelta(hours=5),
        "condition": "Hot, freshly packed in sanitized containers",
        "destination": "DONATE",
        "price": 0.0,
        "status": "matched",
        "matched_recipient": "Ahmedabad Food Bank",
        "assigned_volunteer": "Ravi Kumar",
        "created_at": now - timedelta(hours=2)
    },
    {
        "food_name": "Paneer Butter Masala",
        "category": "Cooked Meal",
        "quantity": 8.0,
        "unit": "kg",
        "prep_time": now - timedelta(hours=2),
        "expiry_time": now + timedelta(hours=6),
        "condition": "Cooked at lunch buffet, refrigerated",
        "destination": "SELL",
        "price": 450.0,
        "status": "pending",
        "matched_recipient": "",
        "assigned_volunteer": "",
        "created_at": now - timedelta(hours=1, minutes=30)
    },
    {
        "food_name": "Veg Biryani",
        "category": "Cooked Meal",
        "quantity": 20.0,
        "unit": "kg",
        "prep_time": now - timedelta(hours=8),
        "expiry_time": now - timedelta(hours=1),
        "condition": "Standard catering pack",
        "destination": "DONATE",
        "price": 0.0,
        "status": "delivered",
        "matched_recipient": "Roti Bank NGO",
        "assigned_volunteer": "Amit Patel",
        "created_at": now - timedelta(hours=8)
    },
    {
        "food_name": "Bread Rolls (50 pcs)",
        "category": "Bakery",
        "quantity": 5.0,
        "unit": "kg",
        "prep_time": now - timedelta(hours=4),
        "expiry_time": now + timedelta(hours=4),
        "condition": "Baked fresh this morning, sealed paper bags",
        "destination": "DONATE",
        "price": 0.0,
        "status": "pickup_pending",
        "matched_recipient": "Hope Children Shelter",
        "assigned_volunteer": "Priya Sharma",
        "created_at": now - timedelta(hours=3, minutes=30)
    },
    {
        "food_name": "Mix Vegetable Curry",
        "category": "Cooked Meal",
        "quantity": 12.0,
        "unit": "kg",
        "prep_time": now - timedelta(days=1),
        "expiry_time": now - timedelta(hours=18),
        "condition": "Packed hot",
        "destination": "DONATE",
        "price": 0.0,
        "status": "delivered",
        "matched_recipient": "Care Foundation",
        "assigned_volunteer": "Ravi Kumar",
        "created_at": now - timedelta(days=1)
    },
    {
        "food_name": "Tawa Roti & Paratha",
        "category": "Bakery",
        "quantity": 7.0,
        "unit": "kg",
        "prep_time": now - timedelta(days=1, hours=2),
        "expiry_time": now - timedelta(hours=20),
        "condition": "Wrapped in foil bundles",
        "destination": "DONATE",
        "price": 0.0,
        "status": "delivered",
        "matched_recipient": "Roti Bank NGO",
        "assigned_volunteer": "Amit Patel",
        "created_at": now - timedelta(days=1, hours=2)
    },
    {
        "food_name": "Fresh Fruit Custard",
        "category": "Dairy",
        "quantity": 6.5,
        "unit": "kg",
        "prep_time": now - timedelta(days=2),
        "expiry_time": now - timedelta(days=1),
        "condition": "Chilled, dessert portions",
        "destination": "SELL",
        "price": 320.0,
        "status": "sold",
        "matched_recipient": "Customer Direct Order #FL89",
        "assigned_volunteer": "",
        "created_at": now - timedelta(days=2)
    },
    {
        "food_name": "Vegetable Pulao",
        "category": "Cooked Meal",
        "quantity": 18.0,
        "unit": "kg",
        "prep_time": now - timedelta(days=2, hours=4),
        "expiry_time": now - timedelta(days=1, hours=12),
        "condition": "Sealed warm boxes",
        "destination": "DONATE",
        "price": 0.0,
        "status": "delivered",
        "matched_recipient": "Ahmedabad Food Bank",
        "assigned_volunteer": "Ravi Kumar",
        "created_at": now - timedelta(days=2, hours=4)
    },
    {
        "food_name": "Hakka Noodles & Manchurian",
        "category": "Cooked Meal",
        "quantity": 9.0,
        "unit": "kg",
        "prep_time": now - timedelta(days=3),
        "expiry_time": now - timedelta(days=2, hours=12),
        "condition": "Party surplus, hygienically packed",
        "destination": "DONATE",
        "price": 0.0,
        "status": "delivered",
        "matched_recipient": "Urban Hunger Relief",
        "assigned_volunteer": "Priya Sharma",
        "created_at": now - timedelta(days=3)
    },
    {
        "food_name": "Assorted Danish Pastries",
        "category": "Bakery",
        "quantity": 4.0,
        "unit": "kg",
        "prep_time": now - timedelta(days=3, hours=5),
        "expiry_time": now - timedelta(days=2, hours=10),
        "condition": "Bakery display excess",
        "destination": "SELL",
        "price": 250.0,
        "status": "sold",
        "matched_recipient": "Customer Direct Order #FL74",
        "assigned_volunteer": "",
        "created_at": now - timedelta(days=3, hours=5)
    },
    {
        "food_name": "Pav Bhaji (Gravy & Pav)",
        "category": "Cooked Meal",
        "quantity": 14.0,
        "unit": "kg",
        "prep_time": now - timedelta(days=4),
        "expiry_time": now - timedelta(days=3, hours=14),
        "condition": "Separately packed gravy and pav",
        "destination": "DONATE",
        "price": 0.0,
        "status": "delivered",
        "matched_recipient": "Care Foundation",
        "assigned_volunteer": "Amit Patel",
        "created_at": now - timedelta(days=4)
    },
    {
        "food_name": "Dal Tadka",
        "category": "Cooked Meal",
        "quantity": 4.0,
        "unit": "kg",
        "prep_time": now - timedelta(hours=14),
        "expiry_time": now - timedelta(hours=2),
        "condition": "Exceeded safe holding temperature",
        "destination": "DONATE",
        "price": 0.0,
        "status": "wasted",
        "matched_recipient": "Safe Compost Facility",
        "assigned_volunteer": "",
        "created_at": now - timedelta(hours=14)
    }
]

created_listings = []
for item in listings_data:
    created_at = item.pop("created_at")
    obj = FoodListing.objects.create(business=user, **item)
    obj.created_at = created_at
    obj.save()
    created_listings.append(obj)

# Create Food Requests
FoodRequest.objects.create(
    food_listing=created_listings[0], # Dal Makhani
    requester_name="Care Foundation NGO",
    requester_type="NGO",
    requester_contact="+91 98222 11001",
    requested_qty=15.0,
    message="We have 60 destitute individuals waiting at our shelter. Can pick up promptly.",
    status="approved"
)
FoodRequest.objects.create(
    food_listing=created_listings[1], # Paneer Butter Masala
    requester_name="Aarav Sharma",
    requester_type="Customer",
    requester_contact="+91 99111 22334",
    requested_qty=4.0,
    message="Interested in 4 kg for family gathering tonight at discounted rate.",
    status="pending"
)
FoodRequest.objects.create(
    food_listing=created_listings[3], # Bread Rolls
    requester_name="Hope Children Shelter",
    requester_type="NGO",
    requester_contact="+91 98444 33221",
    requested_qty=5.0,
    message="For evening snack program for 40 resident children.",
    status="pending"
)

# Create Pickups
PickupDelivery.objects.create(
    food_listing=created_listings[3], # Bread Rolls
    volunteer_name="Priya Sharma",
    volunteer_phone="+91 98765 88990",
    recipient_name="Hope Children Shelter",
    recipient_address="Sector 5, Gandhinagar Highway, Ahmedabad",
    scheduled_time=now + timedelta(hours=1, minutes=30),
    status="scheduled",
    otp_code="3841"
)
PickupDelivery.objects.create(
    food_listing=created_listings[0], # Dal Makhani
    volunteer_name="Ravi Kumar",
    volunteer_phone="+91 98765 43210",
    recipient_name="Ahmedabad Food Bank",
    recipient_address="Navrangpura, Near University, Ahmedabad",
    scheduled_time=now + timedelta(minutes=45),
    status="in_transit",
    otp_code="4928"
)
PickupDelivery.objects.create(
    food_listing=created_listings[2], # Veg Biryani
    volunteer_name="Amit Patel",
    volunteer_phone="+91 98989 12345",
    recipient_name="Roti Bank NGO",
    recipient_address="Paldi Char Rasta, Ahmedabad",
    scheduled_time=now - timedelta(hours=3),
    status="delivered",
    otp_code="7182",
    delivered_at=now - timedelta(hours=1)
)

# Create Notifications
BusinessNotification.objects.create(
    user=user,
    food_listing=created_listings[0],
    title="Food matched with NGO!",
    message="Your Dal Makhani + Rice (15 kg) was successfully matched with Ahmedabad Food Bank.",
    notif_type="match",
    is_read=False
)
BusinessNotification.objects.create(
    user=user,
    food_listing=created_listings[3],
    title="Volunteer assigned for pickup",
    message="Volunteer Priya Sharma has been assigned for pickup of Bread Rolls (5 kg). ETA: 45 mins.",
    notif_type="volunteer",
    is_read=False
)
BusinessNotification.objects.create(
    user=user,
    food_listing=created_listings[2],
    title="Delivery confirmed by NGO",
    message="Roti Bank NGO confirmed delivery of Veg Biryani (20 kg). Thanks for supporting zero hunger!",
    notif_type="delivery",
    is_read=True
)
BusinessNotification.objects.create(
    user=user,
    food_listing=created_listings[11],
    title="Food expiry alert – Dal Tadka",
    message="Dal Tadka (4 kg) passed safe consumption window and was logged as safely disposed/wasted.",
    notif_type="expiry",
    is_read=False
)
BusinessNotification.objects.create(
    user=user,
    food_listing=created_listings[0],
    title="New request from Care Foundation NGO",
    message="Care Foundation requested 15 kg of surplus cooked meals.",
    notif_type="request",
    is_read=False
)

print("Successfully seeded FoodLoop Business data for", user.email)
