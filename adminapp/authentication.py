from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from voteapp.models import Member
from django.contrib.auth.hashers import check_password

class PhoneOnlyAuthenticationBackend(BaseBackend):
    def authenticate(self, request, phone=None, **kwargs):
        try:
            member = Member.objects.get(phone=phone)
            return member
        except Member.DoesNotExist:
            return None
        
    def get_user(self, user_id):
        try:
            return Member.objects.get(pk=user_id)
        except Member.DoesNotExist:
            return None