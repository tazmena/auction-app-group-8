from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, PermissionsMixin, UserManager

class CustomAccountManager(UserManager):

    def create_superuser(self, email: str, username: str, first_name: str, last_name: str, password: str, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True'
            )
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True'
            )

        return self.create_user(email, username, first_name, last_name, password, **extra_fields)
    
    def create_user(self, email: str, username: str, first_name: str, last_name: str, password: str, **extra_fields):
        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', True)

        user = self.model(email=email, username=username,
                            first_name=first_name, last_name = last_name,
                            **extra_fields)
        user.set_password(password)
        user.save()
        return user


class User(AbstractUser, PermissionsMixin):
    '''
    Our User models is a sub-class of Django's AbstractUser
    So we can make use of Django's authentication system
    '''

    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        db_column='user_name'  # <------------------------
    )
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    date_of_birth = models.DateField(auto_now=True)
    image = models.ImageField(upload_to='images', default='default.png')

    is_staff = models.BooleanField(default=False)
    is_active: models.BooleanField(default=False)

    objects = CustomAccountManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.username

class Product(models.Model):
    '''
    A Product is is an object with detailed properties
    that a User can purchase 
    '''
    product_name = models.CharField(_('name'), max_length=100)
    description = models.CharField(_('description'), max_length=4096, default='')
    start_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return f"Product Name: {self.product_name}"
        
