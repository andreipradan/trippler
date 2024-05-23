from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

from trippler.models import TimeStampedModel


class UserManager(BaseUserManager):
    def create_user(self, email, password=None) -> "User":
        if not email:
            msg = "Users must have an email address"
            raise ValueError(msg)
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None) -> "User":
        user = self.create_user(email, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, TimeStampedModel):
    currency = models.ForeignKey(
        "expenses.Currency",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    email = models.EmailField("email address", blank=True, unique=True)
    first_name = models.CharField("first name", max_length=150)
    last_name = models.CharField("last name", max_length=150, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"

    def __str__(self) -> str:
        return self.get_short_name()

    @staticmethod
    def has_perm(perm, obj=None) -> bool:  # noqa: ARG004
        return True

    @staticmethod
    def has_module_perms(app_label) -> bool:  # noqa: ARG004
        return True

    @property
    def is_staff(self) -> bool:
        return self.is_admin

    def get_full_name(self) -> str:
        if self.first_name or self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.get_short_name()

    def get_short_name(self) -> str:
        return self.first_name or self.get_username()
