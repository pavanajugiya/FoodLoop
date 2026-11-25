import json
from decimal import Decimal
from datetime import timedelta
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.utils import timezone
from home.models import (
    UserProfile, FoodListing, FoodRequest, PickupDelivery,
    FoodEligibility, FoodMatch, FoodAnalytics, AppNotification
)


class FoodLoopProjectTestSuite(TestCase):
    """
    Automated Test Suite for The FoodLoop System.
    Directly verifies all 18 Test Cases (TC-01 through TC-18)
    specified in Table 17.1 of the Software Project Report.
    """

    def setUp(self):
        self.client = Client()
        self.now = timezone.now()

        # Admin User
        self.admin_user = User.objects.create_superuser(
            username='thefoodloop13947@gmail.com',
            email='thefoodloop13947@gmail.com',
            password='AdminPassword123!',
            first_name='Harpal',
            last_name='Patel'
        )
        self.admin_profile = UserProfile.objects.get(user=self.admin_user)
        self.admin_profile.role = 'admin'
        self.admin_profile.phone = '9876543210'
        self.admin_profile.save()

        # Food Business User
        self.biz_user = User.objects.create_user(
            username='pavanfb@gmail.com',
            email='pavanfb@gmail.com',
            password='BusinessPass123!',
            first_name='Pavan',
            last_name='Ajugiya'
        )
        self.biz_profile = UserProfile.objects.get(user=self.biz_user)
        self.biz_profile.role = 'business'
        self.biz_profile.business_name = 'Spice Garden Restaurant'
        self.biz_profile.business_type = 'Restaurant'
        self.biz_profile.city = 'Ahmedabad'
        self.biz_profile.save()

        # NGO User
        self.ngo_user = User.objects.create_user(
            username='pavanngo@gmail.com',
            email='pavanngo@gmail.com',
            password='NgoPassword123!',
            first_name='Takshil',
            last_name='Thakor'
        )
        self.ngo_profile = UserProfile.objects.get(user=self.ngo_user)
        self.ngo_profile.role = 'ngo'
        self.ngo_profile.ngo_name = 'Ahmedabad Food Bank'
        self.ngo_profile.daily_capacity_kg = 150
        self.ngo_profile.city = 'Ahmedabad'
        self.ngo_profile.save()

        # Customer User
        self.cust_user = User.objects.create_user(
            username='pavanc@gmail.com',
            email='pavanc@gmail.com',
            password='CustPassword123!',
            first_name='Mehul',
            last_name='Kumar'
        )
        self.cust_profile = UserProfile.objects.get(user=self.cust_user)
        self.cust_profile.role = 'customer'
        self.cust_profile.city = 'Ahmedabad'
        self.cust_profile.save()

        # Volunteer User
        self.vol_user = User.objects.create_user(
            username='pavanv@gmail.com',
            email='pavanv@gmail.com',
            password='VolPassword123!',
            first_name='Ravi',
            last_name='Shah'
        )
        self.vol_profile = UserProfile.objects.get(user=self.vol_user)
        self.vol_profile.role = 'volunteer'
        self.vol_profile.phone = '9898977889'
        self.vol_profile.is_available = True
        self.vol_profile.city = 'Ahmedabad'
        self.vol_profile.save()


    # -------------------------------------------------------------
    # TC-01: Register with valid details
    # -------------------------------------------------------------
    def test_tc01_registration_valid_details(self):
        payload = {
            'first_name': 'Aarav',
            'last_name': 'Sharma',
            'email': 'aarav@foodloop.org',
            'password': 'Password123!',
            'confirm_password': 'Password123!',
            'phone': '9876500001',
            'role': 'customer',
            'city': 'Ahmedabad',
            'state': 'Gujarat',
            'address': '123 SG Highway',
            'pincode': '380054'
        }
        response = self.client.post('/register/', json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data.get('status'), 'success')
        self.assertTrue(User.objects.filter(email='aarav@foodloop.org').exists())

    # -------------------------------------------------------------
    # TC-02: Register with existing email
    # -------------------------------------------------------------
    def test_tc02_registration_existing_email(self):
        payload = {
            'first_name': 'Duplicate',
            'last_name': 'User',
            'email': 'pavanfb@gmail.com',  # already registered in setUp
            'password': 'Password123!',
            'confirm_password': 'Password123!',
            'role': 'customer'
        }
        response = self.client.post('/register/', json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 409)
        data = response.json()
        self.assertEqual(data.get('status'), 'error')
        self.assertIn('already exists', data.get('message', '').lower())

    # -------------------------------------------------------------
    # TC-03: Login with valid credentials
    # -------------------------------------------------------------
    def test_tc03_login_valid_credentials(self):
        payload = {
            'email': 'pavanfb@gmail.com',
            'password': 'BusinessPass123!'
        }
        response = self.client.post('/login/', json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data.get('status'), 'success')

    # -------------------------------------------------------------
    # TC-04: Login with invalid password
    # -------------------------------------------------------------
    def test_tc04_login_invalid_password(self):
        payload = {
            'email': 'pavanfb@gmail.com',
            'password': 'WrongPassword999'
        }
        response = self.client.post('/login/', json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 401)
        data = response.json()
        self.assertEqual(data.get('status'), 'error')
        self.assertIn('invalid', data.get('message', '').lower())

    # -------------------------------------------------------------
    # TC-05: Add valid surplus food
    # -------------------------------------------------------------
    def test_tc05_add_valid_surplus_food(self):
        self.client.force_login(self.biz_user)
        payload = {
            'food_name': 'Vegetable Biryani',
            'category': 'Cooked Meal',
            'quantity': 25.50,
            'unit': 'kg',
            'prep_time': (self.now - timedelta(hours=1)).isoformat(),
            'expiry_time': (self.now + timedelta(hours=5)).isoformat(),
            'condition': 'Freshly prepared, packed in thermal containers',
            'destination': 'DONATE'
        }
        response = self.client.post('/business-api/food/add/', json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data.get('status'), 'success')
        self.assertTrue(FoodListing.objects.filter(food_name='Vegetable Biryani').exists())

    # -------------------------------------------------------------
    # TC-06: Enter invalid quantity (0 or negative)
    # -------------------------------------------------------------
    def test_tc06_invalid_quantity(self):
        self.client.force_login(self.biz_user)
        payload = {
            'food_name': 'Dal Makhani',
            'category': 'Cooked Meal',
            'quantity': 0,  # Invalid quantity
            'unit': 'kg',
            'destination': 'DONATE'
        }
        response = self.client.post('/business-api/food/add/', json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertEqual(data.get('status'), 'error')
        self.assertIn('validation error', data.get('message', '').lower())

    # -------------------------------------------------------------
    # TC-07: Check eligible food (fresh with valid usable time)
    # -------------------------------------------------------------
    def test_tc07_check_eligible_food(self):
        payload = {
            'expiry_time': (self.now + timedelta(hours=6)).isoformat()
        }
        response = self.client.post('/api/food/check-eligibility/', json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data.get('status'), 'success')
        self.assertTrue(data.get('is_eligible'))
        self.assertEqual(data.get('message'), 'Food is marked eligible')

    # -------------------------------------------------------------
    # TC-08: Check expired food (expiry time has passed)
    # -------------------------------------------------------------
    def test_tc08_check_expired_food(self):
        payload = {
            'expiry_time': (self.now - timedelta(hours=2)).isoformat()
        }
        response = self.client.post('/api/food/check-eligibility/', json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data.get('status'), 'success')
        self.assertFalse(data.get('is_eligible'))
        self.assertEqual(data.get('message'), 'Food is marked unsuitable/disposal')

    # -------------------------------------------------------------
    # TC-09: Match food with suitable receiver
    # -------------------------------------------------------------
    def test_tc09_match_food_with_suitable_receiver(self):
        # Create a food listing of 25 kg (Ahmedabad Food Bank has capacity 150 kg)
        listing = FoodListing.objects.create(
            business=self.biz_user,
            food_name='Paneer Pulav',
            category='Cooked Meal',
            quantity=Decimal('25.0'),
            unit='kg',
            prep_time=self.now - timedelta(hours=1),
            expiry_time=self.now + timedelta(hours=5),
            destination='DONATE',
            status='available'
        )
        response = self.client.get(f'/api/food/{listing.id}/match/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data.get('status'), 'success')
        self.assertIn('suggested/matched', data.get('message', '').lower())
        self.assertTrue(FoodMatch.objects.filter(food_item=listing).exists())

    # -------------------------------------------------------------
    # TC-10: Receiver capacity is insufficient
    # -------------------------------------------------------------
    def test_tc10_receiver_capacity_insufficient(self):
        # Set all NGOs to low capacity (e.g., 10 kg)
        UserProfile.objects.filter(role='ngo').update(daily_capacity_kg=10)

        # Create food listing with 50 kg (greater than 10 kg capacity)
        listing = FoodListing.objects.create(
            business=self.biz_user,
            food_name='Bulk Rice Feast',
            category='Cooked Meal',
            quantity=Decimal('50.0'),
            unit='kg',
            prep_time=self.now - timedelta(hours=1),
            expiry_time=self.now + timedelta(hours=5),
            destination='DONATE',
            status='available'
        )
        response = self.client.get(f'/api/food/{listing.id}/match/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data.get('status'), 'warning')
        self.assertIn('not selected for the full quantity', data.get('message', '').lower())

    # -------------------------------------------------------------
    # TC-11: Submit valid food request
    # -------------------------------------------------------------
    def test_tc11_submit_valid_food_request(self):
        self.client.force_login(self.ngo_user)
        listing = FoodListing.objects.create(
            business=self.biz_user,
            food_name='Fresh Chapati & Subzi',
            category='Cooked Meal',
            quantity=Decimal('30.0'),
            unit='kg',
            prep_time=self.now - timedelta(hours=1),
            expiry_time=self.now + timedelta(hours=4),
            destination='DONATE',
            status='available'
        )
        payload = {
            'listing_id': listing.id,
            'quantity': 15.0,
            'message': 'Requesting food for shelter community dinner.'
        }
        response = self.client.post('/ngo-api/request-food/', json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data.get('status'), 'success')
        self.assertTrue(FoodRequest.objects.filter(food_listing=listing).exists())

    # -------------------------------------------------------------
    # TC-12: Assign available volunteer
    # -------------------------------------------------------------
    def test_tc12_assign_available_volunteer(self):
        listing = FoodListing.objects.create(
            business=self.biz_user,
            food_name='Samosa Packets',
            category='Cooked Meal',
            quantity=Decimal('10.0'),
            unit='kg',
            prep_time=self.now,
            expiry_time=self.now + timedelta(hours=4),
            status='matched'
        )
        pickup = PickupDelivery.objects.create(
            food_listing=listing,
            scheduled_time=self.now + timedelta(hours=1),
            status='scheduled',
            otp_code='1234'
        )
        response = self.client.post(f'/api/pickups/{pickup.id}/assign-volunteer/', json.dumps({}), content_type='application/json')
        self.assertEqual(response.status_code, 200)


        data = response.json()
        self.assertEqual(data.get('status'), 'success')
        self.assertIn('assigned successfully', data.get('message', '').lower())
        pickup.refresh_from_db()
        self.assertIsNotNone(pickup.volunteer)

    # -------------------------------------------------------------
    # TC-13: Update delivery status
    # -------------------------------------------------------------
    def test_tc13_update_delivery_status(self):
        listing = FoodListing.objects.create(
            business=self.biz_user,
            food_name='Curd Rice',
            quantity=Decimal('15.0'),
            prep_time=self.now,
            expiry_time=self.now + timedelta(hours=4),
            status='matched'
        )
        pickup = PickupDelivery.objects.create(
            food_listing=listing,
            scheduled_time=self.now,
            status='scheduled',
            otp_code='9876'
        )
        payload = {'status': 'in_transit'}
        response = self.client.post(f'/business-api/pickups/{pickup.id}/update-status/', json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        pickup.refresh_from_db()
        self.assertEqual(pickup.status, 'in_transit')

    # -------------------------------------------------------------
    # TC-14: Verify pickup/delivery with OTP/QR
    # -------------------------------------------------------------
    def test_tc14_verify_pickup_delivery(self):
        listing = FoodListing.objects.create(
            business=self.biz_user,
            food_name='Idli Sambhar',
            quantity=Decimal('20.0'),
            prep_time=self.now,
            expiry_time=self.now + timedelta(hours=4),
            status='in_transit'
        )
        pickup = PickupDelivery.objects.create(
            food_listing=listing,
            scheduled_time=self.now,
            status='in_transit',
            otp_code='4321'
        )
        payload = {'otp': '4321'}
        response = self.client.post(f'/api/pickups/{pickup.id}/verify/', json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data.get('status'), 'success')
        self.assertIn('verified successfully', data.get('message', '').lower())
        pickup.refresh_from_db()
        self.assertEqual(pickup.status, 'delivered')

    # -------------------------------------------------------------
    # TC-15: Generate request notification on request approval
    # -------------------------------------------------------------
    def test_tc15_generate_request_notification(self):
        self.client.force_login(self.biz_user)
        listing = FoodListing.objects.create(
            business=self.biz_user,
            food_name='Vegetable Pulao',
            quantity=Decimal('20.0'),
            prep_time=self.now,
            expiry_time=self.now + timedelta(hours=5),
            status='available'
        )
        req = FoodRequest.objects.create(
            food_listing=listing,
            requester=self.ngo_user,
            requester_name='Ahmedabad Food Bank',
            requested_qty=Decimal('20.0'),
            status='pending'
        )
        payload = {'action': 'approve'}
        response = self.client.post(f'/business-api/requests/{req.id}/handle/', json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 200)

        # Verify notification was generated for the requester user
        notif = AppNotification.objects.filter(user=self.ngo_user, title="Food Request Accepted").first()
        self.assertIsNotNone(notif)
        self.assertEqual(notif.title, "Food Request Accepted")
        self.assertEqual(notif.message, "Your food request has been accepted.")

    # -------------------------------------------------------------
    # TC-16: Admin view/manage users
    # -------------------------------------------------------------
    def test_tc16_admin_view_manage_users(self):
        self.client.force_login(self.admin_user)
        response = self.client.get('/dashboard-admin/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Admin Dashboard')
        self.assertContains(response, 'User Management')

    # -------------------------------------------------------------
    # TC-17: Generate food report
    # -------------------------------------------------------------
    def test_tc17_generate_food_report(self):
        self.client.force_login(self.admin_user)
        response = self.client.get('/admin-api/reports/food/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data.get('status'), 'success')
        self.assertIn('statistics', data)
        self.assertEqual(data.get('message'), 'Correct food statistics are displayed')

    # -------------------------------------------------------------
    # TC-18: Access restricted admin page
    # -------------------------------------------------------------
    def test_tc18_security_access_restricted_admin_page(self):
        # Normal customer user tries to access /dashboard-admin/
        self.client.force_login(self.cust_user)
        response = self.client.get('/dashboard-admin/')
        self.assertEqual(response.status_code, 403)
        self.assertIn('unauthorized', response.content.decode('utf-8').lower())
