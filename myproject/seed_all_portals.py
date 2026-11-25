import os
import django
from datetime import timedelta
from decimal import Decimal
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.contrib.auth.models import User
from home.models import (
    UserProfile, FoodListing, FoodRequest, PickupDelivery,
    CustomerOrder, DistributionRecord, ContactMessage, AppNotification, BusinessNotification
)

now = timezone.now()

# 1. Setup Profiles
# NGO User
ngo_user = User.objects.filter(email='pavanngo@gmail.com').first()
if ngo_user:
    ngo_user.first_name = "Ahmedabad"
    ngo_user.last_name = "Food Bank"
    ngo_user.save()
    p, _ = UserProfile.objects.get_or_create(user=ngo_user)
    p.role = 'ngo'
    p.ngo_name = "Ahmedabad Food Bank"
    p.ngo_type = "Food Bank & Shelter"
    p.daily_capacity_kg = 250
    p.requirements = "Cooked meals, vegetarian preferred, sealed food-grade containers"
    p.phone = "+91 98765 22001"
    p.address = "Sector 5, Navrangpura Community Complex"
    p.city = "Ahmedabad"
    p.state = "Gujarat"
    p.pincode = "380009"
    p.save()

# Customer User
cust_user = User.objects.filter(email='pavanc@gmail.com').first()
if cust_user:
    cust_user.first_name = "Mehul"
    cust_user.last_name = "Kumar"
    cust_user.save()
    p, _ = UserProfile.objects.get_or_create(user=cust_user)
    p.role = 'customer'
    p.phone = "+91 98111 44556"
    p.address = "B-402 Shivalik Heights, S.G. Highway, Bodakdev"
    p.city = "Ahmedabad"
    p.state = "Gujarat"
    p.pincode = "380054"
    p.save()

# Volunteer User
vol_user = User.objects.filter(email='pavanv@gmail.com').first()
if vol_user:
    vol_user.first_name = "Ravi"
    vol_user.last_name = "Shah"
    vol_user.save()
    p, _ = UserProfile.objects.get_or_create(user=vol_user)
    p.role = 'volunteer'
    p.phone = "+91 98989 77889"
    p.vehicle_type = "Honda Activa"
    p.vehicle_number = "GJ 01 AB 1234"
    p.is_available = True
    p.rating = Decimal("4.9")
    p.address = "Paldi Char Rasta"
    p.city = "Ahmedabad"
    p.state = "Gujarat"
    p.pincode = "380007"
    p.save()

# Business User
biz_user = User.objects.filter(email='pavanfb@gmail.com').first()
if not biz_user:
    biz_user = User.objects.first()

# 2. Add or Update Listings for NGO and Customer
extra_listings = [
    {
        "food_name": "Veg Pulao + Raita",
        "category": "Cooked Meal",
        "quantity": Decimal("10.0"),
        "unit": "kg",
        "prep_time": now - timedelta(hours=2),
        "expiry_time": now + timedelta(hours=6),
        "condition": "Hot in thermo boxes",
        "destination": "DONATE",
        "price": Decimal("0.00"),
        "status": "available",
        "notes": "Available for immediate NGO pickup"
    },
    {
        "food_name": "Samosas & Chutney (200 pcs)",
        "category": "Cooked Meal",
        "quantity": Decimal("8.0"),
        "unit": "kg",
        "prep_time": now - timedelta(hours=3),
        "expiry_time": now + timedelta(hours=2),
        "condition": "Crispy, packed in paper cartons",
        "destination": "DONATE",
        "price": Decimal("0.00"),
        "status": "available",
        "notes": "Ideal for afternoon tea snack distribution"
    },
    {
        "food_name": "Artisan Bread Loaves (30 loaves)",
        "category": "Bakery",
        "quantity": Decimal("12.0"),
        "unit": "kg",
        "prep_time": now - timedelta(hours=5),
        "expiry_time": now + timedelta(hours=18),
        "condition": "Sealed bread bags",
        "destination": "DONATE",
        "price": Decimal("0.00"),
        "status": "available",
        "notes": "Fresh morning bake"
    },
    {
        "food_name": "Gourmet Veg Pizza (10 boxes)",
        "category": "Cooked Meal",
        "quantity": Decimal("5.0"),
        "unit": "packets",
        "prep_time": now - timedelta(hours=1),
        "expiry_time": now + timedelta(hours=4),
        "condition": "Sealed pizza boxes, hot",
        "destination": "SELL",
        "price": Decimal("120.00"),
        "status": "available",
        "notes": "70% off regular menu price"
    },
    {
        "food_name": "Royal Thali Meal Packets (15 packets)",
        "category": "Cooked Meal",
        "quantity": Decimal("15.0"),
        "unit": "packets",
        "prep_time": now - timedelta(hours=2),
        "expiry_time": now + timedelta(hours=5),
        "condition": "Packed 5-compartment meal trays",
        "destination": "SELL",
        "price": Decimal("99.00"),
        "status": "available",
        "notes": "Buffet excess, hygienically sealed"
    }
]

for item in extra_listings:
    existing = FoodListing.objects.filter(food_name=item["food_name"]).first()
    if not existing:
        FoodListing.objects.create(business=biz_user, **item)

# 3. Create NGO Requests
if ngo_user:
    l1 = FoodListing.objects.filter(food_name__icontains="Dal Makhani").first()
    if l1 and not FoodRequest.objects.filter(requester=ngo_user, food_listing=l1).exists():
        FoodRequest.objects.create(
            food_listing=l1,
            requester=ngo_user,
            requester_name="Ahmedabad Food Bank",
            requester_type="NGO",
            requester_contact="+91 98765 22001",
            requested_qty=Decimal("15.0"),
            message="We have 60 beneficiaries lined up for dinner.",
            status="approved"
        )
    l2 = FoodListing.objects.filter(food_name__icontains="Veg Pulao").first()
    if l2 and not FoodRequest.objects.filter(requester=ngo_user, food_listing=l2).exists():
        FoodRequest.objects.create(
            food_listing=l2,
            requester=ngo_user,
            requester_name="Ahmedabad Food Bank",
            requester_type="NGO",
            requester_contact="+91 98765 22001",
            requested_qty=Decimal("10.0"),
            message="Night shelter feeding program.",
            status="pending"
        )

# 4. Create Pickups with Tracking Codes
all_listings = FoodListing.objects.all()
if all_listings.exists():
    pk1 = PickupDelivery.objects.filter(food_listing=all_listings[0]).first()
    if pk1:
        pk1.tracking_code = "R001"
        pk1.volunteer = vol_user
        pk1.volunteer_name = "Ravi Shah"
        pk1.volunteer_phone = "+91 98989 77889"
        pk1.status = "in_transit"
        pk1.otp_code = "5829"
        pk1.distance_km = Decimal("2.3")
        pk1.save()

# 5. Create NGO Distribution Records (Received History)
if ngo_user and not DistributionRecord.objects.filter(ngo=ngo_user).exists():
    DistributionRecord.objects.create(
        ngo=ngo_user,
        food_name="Veg Biryani + Mirchi Ka Salan",
        quantity=Decimal("20.0"),
        unit="kg",
        provider_name="Hotel Rajmahal",
        volunteer_name="Ravi Shah",
        beneficiaries_count=80,
        location="Navrangpura Slum & Shelter Cluster",
        received_date=now - timedelta(days=1, hours=3),
        status="Delivered"
    )
    DistributionRecord.objects.create(
        ngo=ngo_user,
        food_name="Moong Dal Khichdi & Kadhi",
        quantity=Decimal("30.0"),
        unit="kg",
        provider_name="Annapoorna Hotel",
        volunteer_name="Priya Patel",
        beneficiaries_count=120,
        location="Vastrapur Orphanage & Senior Center",
        received_date=now - timedelta(days=2),
        status="Delivered"
    )
    DistributionRecord.objects.create(
        ngo=ngo_user,
        food_name="Chapati + Paneer Sabji (50 meals)",
        quantity=Decimal("15.0"),
        unit="kg",
        provider_name="Shreeji Caterers",
        volunteer_name="Mohit Rathod",
        beneficiaries_count=50,
        location="Railway Station Night Shelter",
        received_date=now - timedelta(days=3),
        status="Delivered"
    )

# 6. Create Customer Orders for Mehul Kumar
if cust_user:
    pbm = FoodListing.objects.filter(food_name__icontains="Paneer Butter Masala").first()
    if pbm and not CustomerOrder.objects.filter(customer=cust_user, order_number="ORD-8492").exists():
        CustomerOrder.objects.create(
            order_number="ORD-8492",
            customer=cust_user,
            food_listing=pbm,
            food_name=pbm.food_name,
            business_name="Hotel Rajmahal",
            quantity=Decimal("2.0"),
            unit="kg",
            unit_price=Decimal("220.00"),
            total_amount=Decimal("440.00"),
            delivery_type="delivery",
            delivery_address="B-402 Shivalik Heights, S.G. Highway, Ahmedabad",
            status="in_transit",
            payment_method="UPI / Online",
            payment_status="Paid",
            otp_code="4829",
            notes="Please leave at door if doorbell rings"
        )
    thali = FoodListing.objects.filter(food_name__icontains="Royal Thali").first()
    if thali and not CustomerOrder.objects.filter(customer=cust_user, order_number="ORD-6204").exists():
        CustomerOrder.objects.create(
            order_number="ORD-6204",
            customer=cust_user,
            food_listing=thali,
            food_name=thali.food_name,
            business_name="Grand Taj Banquet",
            quantity=Decimal("2.0"),
            unit="packets",
            unit_price=Decimal("99.00"),
            total_amount=Decimal("198.00"),
            delivery_type="pickup",
            delivery_address="Restaurant Counter, Grand Taj Banquet, Bodakdev",
            status="ready",
            payment_method="Cash on Pickup",
            payment_status="Pending",
            otp_code="3190",
            notes="Pickup at 4:30 PM"
        )
    custard = FoodListing.objects.filter(food_name__icontains="Custard").first()
    if custard and not CustomerOrder.objects.filter(customer=cust_user, order_number="ORD-7310").exists():
        CustomerOrder.objects.create(
            order_number="ORD-7310",
            customer=cust_user,
            food_listing=custard,
            food_name=custard.food_name,
            business_name="Hotel Rajmahal",
            quantity=Decimal("1.5"),
            unit="kg",
            unit_price=Decimal("160.00"),
            total_amount=Decimal("240.00"),
            delivery_type="delivery",
            delivery_address="B-402 Shivalik Heights, Bodakdev",
            status="delivered",
            payment_method="UPI / Online",
            payment_status="Paid",
            otp_code="1029"
        )

# 7. Create App Notifications
notifications_to_create = [
    (ngo_user, "Request approved for Dal Makhani", "Hotel Rajmahal accepted your food request. Volunteer Ravi Shah is on the way.", "match"),
    (ngo_user, "Delivery arriving in 20 minutes", "Volunteer Ravi Shah is en route with 15kg Dal Makhani. OTP: 5829", "delivery"),
    (ngo_user, "New food available: Veg Pulao (10kg)", "Café Lotus has posted 10kg Veg Pulao available for donation nearby.", "info"),
    (cust_user, "Order #ORD-8492 is Out for Delivery", "Volunteer is delivering your Paneer Butter Masala. Share OTP 4829 on arrival.", "delivery"),
    (cust_user, "Surplus Discount: 70% OFF Pizza", "Pizza Bella listed 10 boxes of fresh gourmet pizza starting at ₹120.", "order"),
    (vol_user, "Active Task: Pickup from Hotel Rajmahal", "Pickup 15kg Dal Makhani for Ahmedabad Food Bank. ETA: 15 mins.", "volunteer"),
    (vol_user, "Delivery Confirmed by Beneficiary", "Ahmedabad Food Bank confirmed safe delivery of 20kg Veg Biryani. 5-star rating earned!", "delivery"),
]

for user_obj, title, msg, ntype in notifications_to_create:
    if user_obj and not AppNotification.objects.filter(user=user_obj, title=title).exists():
        AppNotification.objects.create(
            user=user_obj,
            title=title,
            message=msg,
            notif_type=ntype,
            is_read=False
        )

# 8. Contact Message
if not ContactMessage.objects.filter(email="contact@example.com").exists():
    ContactMessage.objects.create(
        name="Sunil Mehta",
        email="contact@example.com",
        phone="+91 98250 12345",
        subject="Surplus Food Donation Inquiry",
        message="We are organizing a 500-person community event in Ahmedabad and would like to register our caterers to donate excess meals."
    )

print("Comprehensive portal data successfully seeded!")
