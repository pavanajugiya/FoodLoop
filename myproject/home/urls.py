from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("index.html", views.index, name="index_html"),

    path("login/", views.login_view, name="login"),
    path("login.html", views.login_view, name="login_html"),

    path("register/", views.register_view, name="register"),
    path("register.html", views.register_view, name="register_html"),

    path("logout/", views.logout_view, name="logout"),
    path("logout.html", views.logout_view, name="logout_html"),

    path("track/", views.track_view, name="track"),
    path("track.html", views.track_view, name="track_html"),

    path("dashboard-admin/", views.dashboard_admin, name="dashboard_admin"),
    path("dashboard-admin.html", views.dashboard_admin, name="dashboard_admin_html"),

    path("dashboard-business/", views.dashboard_business, name="dashboard_business"),
    path("dashboard-business.html", views.dashboard_business, name="dashboard_business_html"),

    path("dashboard-customer/", views.dashboard_customer, name="dashboard_customer"),
    path("dashboard-customer.html", views.dashboard_customer, name="dashboard_customer_html"),

    path("dashboard-ngo/", views.dashboard_ngo, name="dashboard_ngo"),
    path("dashboard-ngo.html", views.dashboard_ngo, name="dashboard_ngo_html"),

    path("dashboard-volunteer/", views.dashboard_volunteer, name="dashboard_volunteer"),
    path("dashboard-volunteer.html", views.dashboard_volunteer, name="dashboard_volunteer_html"),

    # Admin User Management API
    path("admin-api/users/add/", views.admin_add_user, name="admin_add_user"),
    path("admin-api/users/<int:user_id>/toggle-status/", views.admin_toggle_user_status, name="admin_toggle_user_status"),
    path("admin-api/users/<int:user_id>/change-role/", views.admin_change_user_role, name="admin_change_user_role"),
    path("admin-api/users/<int:user_id>/delete/", views.admin_delete_user, name="admin_delete_user"),
    path("admin-api/users/export/", views.admin_export_users_csv, name="admin_export_users_csv"),
    path("admin-api/switch-mode/", views.admin_switch_mode, name="admin_switch_mode"),
    path("admin-api/food/<int:listing_id>/update-status/", views.admin_update_food_status, name="admin_update_food_status"),
    path("admin-api/requests/<int:request_id>/update-status/", views.admin_update_request_status, name="admin_update_request_status"),
    path("admin-api/users/<int:user_id>/verify/", views.admin_verify_account, name="admin_verify_account"),
    path("admin-api/settings/save/", views.admin_save_settings, name="admin_save_settings"),

    # Business Dashboard API
    path("business-api/food/add/", views.business_add_food, name="business_add_food"),
    path("business-api/food/<int:listing_id>/", views.business_get_food, name="business_get_food"),
    path("business-api/food/<int:listing_id>/update/", views.business_update_food, name="business_update_food"),
    path("business-api/food/<int:listing_id>/delete/", views.business_delete_food, name="business_delete_food"),
    path("business-api/requests/<int:request_id>/handle/", views.business_handle_request, name="business_handle_request"),
    path("business-api/pickups/<int:pickup_id>/update-status/", views.business_update_pickup_status, name="business_update_pickup_status"),
    path("business-api/profile/update/", views.business_update_profile, name="business_update_profile"),
    path("business-api/notifications/mark-read/", views.business_mark_notifications_read, name="business_mark_notifications_read"),
    path("business-api/export-csv/", views.business_export_csv, name="business_export_csv"),

    # NGO Dashboard API
    path("ngo-api/request-food/", views.ngo_request_food, name="ngo_request_food"),
    path("ngo-api/confirm-delivery/<int:pickup_id>/", views.ngo_confirm_delivery, name="ngo_confirm_delivery"),
    path("ngo-api/profile/update/", views.ngo_update_profile, name="ngo_update_profile"),
    path("ngo-api/notifications/mark-read/", views.ngo_mark_notifications_read, name="ngo_mark_notifications_read"),

    # Customer Dashboard API
    path("customer-api/order/create/", views.customer_place_order, name="customer_place_order"),
    path("customer-api/razorpay/create-order/", views.customer_create_razorpay_order, name="customer_create_razorpay_order"),
    path("customer-api/razorpay/verify-payment/", views.customer_verify_razorpay_payment, name="customer_verify_razorpay_payment"),
    path("customer-api/order/<int:order_id>/cancel/", views.customer_cancel_order, name="customer_cancel_order"),
    path("customer-api/order/<int:order_id>/confirm/", views.customer_confirm_delivery, name="customer_confirm_delivery"),
    path("customer-api/profile/update/", views.customer_update_profile, name="customer_update_profile"),
    path("customer-api/notifications/mark-read/", views.customer_mark_notifications_read, name="customer_mark_notifications_read"),

    # Volunteer Dashboard API
    path("volunteer-api/task/<int:pickup_id>/accept/", views.volunteer_accept_task, name="volunteer_accept_task"),
    path("volunteer-api/task/<int:pickup_id>/update-status/", views.volunteer_update_status, name="volunteer_update_status"),
    path("volunteer-api/toggle-availability/", views.volunteer_toggle_availability, name="volunteer_toggle_availability"),
    path("volunteer-api/profile/update/", views.volunteer_update_profile, name="volunteer_update_profile"),
    path("volunteer-api/notifications/mark-read/", views.volunteer_mark_notifications_read, name="volunteer_mark_notifications_read"),

    # Live Tracking API
    path("api/track/", views.api_track_delivery, name="api_track_delivery"),

    # Public Contact & Subscription
    path("api/contact/", views.api_contact_submit, name="api_contact_submit"),
    path("api/subscribe/", views.api_newsletter_subscribe, name="api_newsletter_subscribe"),

    # Core FoodLoop Intelligence & Verification APIs (Per PDF Spec & Test Cases)
    path("api/food/check-eligibility/", views.api_check_eligibility, name="api_check_eligibility"),
    path("api/food/<int:listing_id>/match/", views.api_match_food_receiver, name="api_match_food_receiver"),
    path("api/pickups/<int:pickup_id>/assign-volunteer/", views.api_assign_volunteer, name="api_assign_volunteer"),
    path("api/pickups/<int:pickup_id>/verify/", views.api_verify_delivery, name="api_verify_delivery"),
    path("admin-api/reports/food/", views.admin_generate_food_report, name="admin_generate_food_report"),
]

