from django.contrib.auth.models import BaseUserManager

class MemberManager(BaseUserManager):
    def create_user(self, phone, first_name, last_name, email=None,password=None, is_admin=False, **extra_fields):
        if not phone:
            raise ValueError("The Phone field is required")
        
        if not first_name or not last_name:
            raise ValueError("First name and Last name are required")
        
        email= self.normalize_email(email)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        user = self.model(phone=phone,first_name=first_name,last_name=last_name,email=email,is_admin=is_admin, **extra_fields)
        if password:
            user.set_password(password)
        user.set_unusable_password()
        user.save(using=self._db)
        return user
    
    def create_superuser(self,phone,first_name,last_name, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_admin',True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser',True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Super user must have is_staff=True')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Super user must have is_superuser=True')
        
        return self.create_user(phone,first_name,last_name,email,password, **extra_fields)
