from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

UserModel = get_user_model()


class EmailOrUsernameModelBackend(ModelBackend):
    """
    Custom authentication backend that permits users to log in using either
    their email address or their username.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD) or kwargs.get('email')

        if not username or not password:
            return None

        try:
            user = UserModel.objects.filter(
                Q(email__iexact=username) | Q(username__iexact=username)
            ).first()
        except UserModel.DoesNotExist:
            return None

        if user and user.check_password(password) and self.user_can_authenticate(user):
            return user

        return None
