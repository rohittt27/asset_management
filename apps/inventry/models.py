# Python Imports
import datetime

# Django Imports
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _

# Project Imports

# Third Party Imports


PAYMENT_CHOICES = (
    ("due", "due"),
    ("done", "done"),
)


TECHNOLOGY_CHOICES = (
    ("Python", "Python"),
    ("Quality_Analyst", "Quality_Analyst"),
    ("Angular", "Angular"),
    ("React", "React"),
    ("IOS", "IOS"),
    ("Flutter", "Flutter"),
    ("Blockchain", "Blockchain"),
    ("Android", "Android"),
    ("SEO", "SEO"),
    ("React-Native", "React-Native"),
    ("Node", "Node"),
    ("Business_Development", "Business_Development"),
    ("Web_Design", "Web_Design"),
    ("other", "other"),
)


class AssetType(models.Model):
    asset_name = models.CharField(max_length=250, unique=True)

    def __str__(self):
        return self.asset_name


class User(AbstractUser):
    email = models.EmailField(_("email address"), unique=True)
    mobile_number = models.CharField(max_length=10)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return "{}".format(self.email)


class BaseModel(models.Model):
    created_at = models.DateField(auto_now_add=True)
    deleted_at = models.DateTimeField(auto_now=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Asset(BaseModel):
    DUE = "due"
    DONE = "done"
    YES = "yes"
    NO = "no"
    PAYMENT_CHOICES = [
        (DUE, "due"),
        (DONE, "done"),
    ]
    INVOICE_CHOICES = [
        (YES, "yes"),
        (NO, "no"),
    ]
    RAM = [
        ("4GB", "4GB"),
        ("6GB", "6GB"),
        ("8GB", "8GB"),
        ("16GB", "16GB"),
        ("32GB", "32GB"),
        ("64GB", "64GB"),
    ]
    SSD = [
        ("120", "120"),
        ("250", "250"),
        ("256", "256"),
        ("500", "500"),
    ]
    PROCESSOR = [
        ("i3", "i3"),
        ("i5", "i5"),
        ("i7", "i7"),
        ("i9", "i9"),
        ("i10", "i10"),
    ]
    OS = [
        ("UBUNTU", "ubuntu"),
        ("MAC OS", "mac os"),
        ("WINDOW", "window"),
        ("HACKINTOSH", "hackintosh"),
    ]
    STORAGE = [
        ("16", "16"),
        ("32", "32"),
        ("64", "64"),
        ("128", "128"),
        ("256", "256"),
        ("512", "512"),
    ]

    asset_type = models.ForeignKey(
        AssetType, on_delete=models.SET_NULL, null=True, related_name="assettype"
    )
    asset_brand = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    vendor = models.ForeignKey(
        "Vendor", on_delete=models.SET_NULL, null=True, related_name="vendor_asset"
    )
    total_quantity = models.PositiveIntegerField(default=0)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default="due")
    in_voice = models.CharField(max_length=20, choices=INVOICE_CHOICES, default="---")
    payment_date = models.CharField(max_length=20, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=0)
    purchase_date = models.DateField(blank=True, null=True)
    system_configuration = models.CharField(max_length=80, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    serial_number = models.CharField(max_length=50, null=True, blank=True)
    invoice_number = models.CharField(max_length=30, null=True, blank=True)
    ram = models.CharField(max_length=30, null=True, blank=True, choices=RAM, default="")
    ssd = models.CharField(max_length=30, null=True, blank=True, choices=SSD, default="")
    processor = models.CharField(max_length=30, null=True, blank=True, choices=PROCESSOR, default="")
    operating_system = models.CharField(max_length=30, null=True, blank=True, choices=OS, default="")
    storage = models.CharField(max_length=30, null=True, blank=True, choices=STORAGE, default="")
    is_assign = models.BooleanField(default=False)

    def payment(self):
        if self.payment_status == 'done':
            payment_comp = str(datetime.datetime.now())
            return payment_comp
        else:
            payment_comp = '---'
            return payment_comp

    def save(self, *args, **kwargs):
        self.payment_date = self.payment()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.asset_type}  {self.asset_brand}({self.ram} {self.ssd} {self.processor} {self.operating_system} {self.storage} {self.serial_number})"


class Vendor(BaseModel):
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    email = models.EmailField(max_length=30, null=True, blank=True, unique=True)
    mobile_number = models.IntegerField()
    address = models.TextField(null=True, blank=True)
    is_vendor = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Employee(BaseModel):

    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    email = models.EmailField(max_length=30, null=True, blank=True, unique=True)
    employee_id = models.CharField(max_length=30, null=True, blank=True, unique=True)
    date_of_joining = models.DateField(null=True, blank=True)
    mobile_number = models.IntegerField()
    technology_name = models.CharField(
        max_length=20,
        choices=TECHNOLOGY_CHOICES,
        null=True, blank=True
    )
    is_have_asset = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f" {self.first_name} {self.last_name} {self.technology_name}"


class AssignAsset(BaseModel):
    employee = models.ForeignKey(
        Employee, on_delete=models.SET_NULL, null=True, related_name="assign_employee"
    )

    asset = models.ForeignKey(
        Asset,
        on_delete=models.SET_NULL,
        null=True,
        related_name="assign_asset",
        default=1,
    )
    date_of_assign = models.DateField(null=True, blank=True)
    # have_asset = models.BooleanField(default=True)
    # serial_number = models.CharField(max_length=80)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.asset}"


class ClientAsset(BaseModel):
    RAM = [
        ("4GB", "4GB"),
        ("6GB", "6GB"),
        ("8GB", "8GB"),
        ("16GB", "16GB"),
        ("32GB", "32GB"),
        ("64GB", "64GB"),
    ]
    SSD = [
        ("120", "120"),
        ("250", "250"),
        ("256", "256"),
        ("500", "500"),
    ]
    PROCESSOR = [
        ("i3", "i3"),
        ("i5", "i5"),
        ("i7", "i7"),
        ("i9", "i9"),
        ("i10", "i10"),
    ]
    OS = [
        ("UBUNTU", "ubuntu"),
        ("MAC OS", "mac os"),
        ("WINDOW", "window"),
        ("HACKINTOSH", "hackintosh"),
    ]
    STORAGE = [
        ("16", "16"),
        ("32", "32"),
        ("64", "64"),
        ("128", "128"),
        ("256", "256"),
        ("512", "512"),
    ]

    client_name = models.CharField(max_length=50)
    project = models.CharField(max_length=50)
    configuration = models.CharField(max_length=250)
    asset_brand = models.CharField(max_length=80)
    asset_type = models.ForeignKey(
        AssetType, on_delete=models.SET_NULL, null=True, related_name="asset_type"
    )
    employee = models.ForeignKey(
        Employee, on_delete=models.SET_NULL, null=True, related_name="employee"
    )
    project_owner = models.CharField(max_length=50)

    asset_quantity = models.IntegerField(default=1)

    is_active = models.BooleanField(default=True)

    is_dispatch = models.BooleanField(default=False)

    date_of_dispatch = models.DateField(null=True, blank=True)

    description = models.TextField(null=True, blank=True)

    serial_number = models.CharField(max_length=50, default="")
    ram = models.CharField(max_length=30, null=True, blank=True, choices=RAM, default="")
    ssd = models.CharField(max_length=30, null=True, blank=True, choices=SSD, default="")
    processor = models.CharField(max_length=30, null=True, blank=True, choices=PROCESSOR, default="")
    operating_system = models.CharField(max_length=30, null=True, blank=True, choices=OS, default="")
    storage = models.CharField(max_length=30, null=True, blank=True, choices=STORAGE, default="")

    def __str__(self):
        return f"{self.asset_brand} {self.asset_type} "
