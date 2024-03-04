#Python Imports

# Projects Imports
from .models import (
    Asset,
    Employee,
    Vendor,
    AssetType,
    AssignAsset,
    ClientAsset,
)
# Django Imports
from django.core.exceptions import ValidationError
from django import forms

# Third Party Imports

class EmployeeForm(forms.ModelForm):
    def __init__(
        self,
        *args,
        **kwargs,
    ):
        super(EmployeeForm, self).__init__(*args, **kwargs)
        instance = getattr(self, "instance", None)
        if instance and instance.pk:
            self.fields["employee_id"].widget.attrs["readonly"] = True

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

    first_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control"})
    )
    employee_id = forms.IntegerField(
        widget=forms.NumberInput(attrs={"class": "form-control"})
    )
    date_of_joining = forms.DateField(
        widget=forms.DateInput(attrs={"class": "form-control"})
    )
    mobile_number = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}) 
    )
    technology_name = forms.ModelChoiceField(
        queryset=Employee.objects.all(), empty_label="Select assets")

    technology_name = forms.ChoiceField(choices=TECHNOLOGY_CHOICES)

    class Meta:
        model = Employee
        
        fields = [
            "first_name",
            "last_name",
            "email",
            "employee_id",
            "date_of_joining",
            "mobile_number",
            "technology_name",
        ]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        email_match = Employee.objects.filter(email=email).exclude(pk=self.instance.pk)
        if self.instance and self.instance.pk and not email_match:
            return email
        else:
            return email

    def clean_employee_id(self):
        employee_id = self.cleaned_data.get("employee_id")
        employee_id_match = Employee.objects.filter(employee_id=employee_id).exclude(
            pk=self.instance.pk
        )
        if self.instance and self.instance.pk and not employee_id_match:
            return self.instance.employee_id
        else:
            # raise forms.ValidationError("employee id already exists")
            return employee_id

    def clean_mobile_number(self):

        phone_no = self.cleaned_data.get("mobile_number", None)
        ph_length = str(phone_no)
        try:

            min_length = 10
            max_length = 12

            if len(ph_length) < min_length:
                raise ValidationError("Please enter correct mobile number")
            if len(ph_length) > max_length:
                raise ValidationError("Please enter correct mobile number")

        except (ValueError, TypeError):
            raise ValidationError("Please enter a valid phone number")
        return phone_no


class AssetTypeForm(forms.ModelForm):
    class Meta:
        model = AssetType
        fields = ["asset_name"]

    def clean_asset_name(self):
        asset_name = self.cleaned_data.get("asset_name")
        asset_type = AssetType.objects.filter(asset_name__icontains=asset_name)
        if asset_type:
            raise forms.ValidationError("This asset already exists")
        return asset_name    


class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ["first_name", "last_name", "email", "mobile_number", "address"]

    def clean_mobile_number(self):
        phone_no = self.cleaned_data.get("mobile_number", None)
        ph_length = str(phone_no)
        try:

            min_length = 10
            max_length = 12

            if len(ph_length) < min_length:
                raise ValidationError("Please enter correct mobile number")
            if len(ph_length) > max_length:
                raise ValidationError("Please enter correct mobile number")

        except (ValueError, TypeError):
            raise ValidationError("Please enter a valid phone number")
        return phone_no


class AssetForm(forms.ModelForm):
    active_vendor_list = Vendor.objects.filter(is_active=True)

    asset_type = forms.ModelChoiceField(
        queryset=AssetType.objects.all(), empty_label="Select assets"
    )
    vendor = forms.ModelChoiceField(
        queryset=Vendor.objects.filter(is_active=True), empty_label="Select vendor"
    )

    asset_brand = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    price = forms.IntegerField(
        widget=forms.NumberInput(attrs={"class": "form-control"})
    )
    purchase_date = forms.DateField(
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "type": "date",
                "required": "false",
            }
        )
    )

    system_configuration = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    serial_number = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    invoice_number = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    INVOICE_CHOICES = (
        ("", "Select Bill Status"),
        ("yes", "yes"),
        ("no", "no"),
    )

    in_voice = forms.ChoiceField(choices=INVOICE_CHOICES)

    PAYMENT_CHOICES = (
        ("", "Select Payment Status"),
        ("due", "due"),
        ("done", "done"),
    )

    RAM = (
        ("", "Select RAM"),
        ("4GB", "4GB"),
        ("6GB", "6GB"),
        ("8GB", "8GB"),
        ("16GB", "16GB"),
        ("32GB", "32GB"),
        ("64GB", "64GB"),
    )
    SSD = (
        ("", "Select SSD"),
        ("120", "120"),
        ("250", "250"),
        ("256", "256"),
        ("500", "500"),
    )
    PROCESSOR = (
        ("", "Select Processor"),
        ("i3", "i3"),
        ("i5", "i5"),
        ("i7", "i7"),
        ("i9", "i9"),
        ("i10", "i10"),
    )
    OS = (
        ("", "Select OS"),
        ("UBUNTU", "ubuntu"),
        ("MAC OS", "mac os"),
        ("WINDOW", "window"),
        ("HACKINTOSH", "hackintosh"),
    )
    STORAGE = (
        ("", "Select Storage"),
        ("16", "16"),
        ("32", "32"),
        ("64", "64"),
        ("128", "128"),
        ("256", "256"),
        ("512", "512"),
    )

    class Meta:
        model = Asset

        fields = [
            "asset_type",
            "asset_brand",
            "price",
            "vendor",
            "purchase_date",
            "system_configuration",
            "serial_number",
            "payment_status",
            "in_voice",
            "invoice_number"
        ]

    asset_type = forms.ModelChoiceField(
        queryset=AssetType.objects.all(), empty_label="Select assets",
    )
    vendor = forms.ModelChoiceField(
        queryset=Vendor.objects.all(), empty_label="Select vendor"
    )
    asset_brand = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    price = forms.IntegerField(
        widget=forms.NumberInput(attrs={"class": "form-control"})
    )
    payment_status = forms.ChoiceField(choices=PAYMENT_CHOICES)

    in_voice = forms.ChoiceField(choices=INVOICE_CHOICES)

    purchase_date = forms.DateField(
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "type": "date",
                "required": "false",
            }
        )
    )
    system_configuration = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    serial_number = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    invoice_number = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    ram = forms.ChoiceField(choices=RAM)

    ssd = forms.ChoiceField(choices=SSD)

    processor = forms.ChoiceField(choices=PROCESSOR)

    operating_system = forms.ChoiceField(choices=OS)

    storage = forms.ChoiceField(choices=STORAGE)

    class Meta:
        model = Asset
        fields = [
            "asset_type",
            "asset_brand",
            "price",
            "ram",
            "ssd",
            "processor",
            "operating_system",
            "storage",
            "vendor",
            "system_configuration",
            "serial_number",
            "payment_status",
            "purchase_date",
            "in_voice",
            "invoice_number",
        ]

    def __init__(self, *args, **kwargs):
        super(AssetForm, self).__init__(*args, **kwargs)
        self.fields['system_configuration'].required = False
        self.fields['purchase_date'].required = False
        self.fields['invoice_number'].required = False
        self.fields['serial_number'].required = False
        self.fields['ram'].required = False
        self.fields['ssd'].required = False
        self.fields['processor'].required = False
        self.fields['operating_system'].required = False
        self.fields['storage'].required = False


class AssignedAssetForm(forms.Form):

    asset = forms.ModelMultipleChoiceField(
        queryset=Asset.objects.filter(is_assign=False),
    )
    employee = forms.ModelChoiceField(
        queryset=Employee.objects.all(),
        to_field_name="email",
        empty_label="Select Employee",
    )

    date_of_assign = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "class": "form-control",
                "type": "date",
            }
        )
    )
    # serial_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = AssignAsset
        fields = ["asset", "employee", "date_of_assign"]


class ClientForm(forms.ModelForm):
    RAM = (
        ("", "Select RAM"),
        ("4GB", "4GB"),
        ("6GB", "6GB"),
        ("8GB", "8GB"),
        ("16GB", "16GB"),
        ("32GB", "32GB"),
        ("64GB", "64GB"),
    )
    SSD = (
        ("", "Select SSD"),
        ("120", "120"),
        ("250", "250"),
        ("256", "256"),
        ("500", "500"),
    )
    PROCESSOR = (
        ("", "Select Processor"),
        ("i3", "i3"),
        ("i5", "i5"),
        ("i7", "i7"),
        ("i9", "i9"),
        ("i10", "i10"),
    )
    OS = (
        ("", "Select OS"),
        ("UBUNTU", "ubuntu"),
        ("MAC OS", "mac os"),
        ("WINDOW", "window"),
        ("HACKINTOSH", "hackintosh"),
    )
    STORAGE = (
        ("", "Select Storage"),
        ("16", "16"),
        ("32", "32"),
        ("64", "64"),
        ("128", "128"),
        ("256", "256"),
        ("512", "512"),
    )

    client_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    project = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    configuration = forms.CharField(
        required=False, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    asset_brand = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    asset_type = forms.ModelChoiceField(queryset=AssetType.objects.all())

    serial_number = forms.CharField(
        required=False, widget=forms.TextInput(attrs={"class": "form-control"}), label="Asset Serial Number"
    )

    project_owner = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    date_of_dispatch = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "class": "form-control",
                "type": "date",
            }
        ), required=False
    )
    description = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}), required=False
    )
    employee = forms.ModelChoiceField(queryset=Employee.objects.all())

    ram = forms.ChoiceField(choices=RAM, required=False)

    ssd = forms.ChoiceField(choices=SSD, required=False)

    processor = forms.ChoiceField(choices=PROCESSOR, required=False)

    operating_system = forms.ChoiceField(choices=OS, required=False)

    storage = forms.ChoiceField(choices=STORAGE, required=False)

    class Meta:
        model = ClientAsset
        fields = [
            "client_name",
            "project",
            "project_owner",
            "employee",
            "asset_brand",
            "asset_type",
            "serial_number",
            "configuration",
            "ram",
            "ssd",
            "processor",
            "operating_system",
            "storage",
            "is_dispatch",
            "date_of_dispatch",
            "description"
        ]


class AssignClientForm(forms.ModelForm):
    class Meta:
        model = ClientAsset
        fields = ["project", "configuration", "asset_brand"]

class AssignedAssetsForm(forms.ModelForm):

    # def __init__(self, asset, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     queryset = Asset.objects.filter(is_assign=False) 
    #     query = Asset.objects.filter(id = asset.asset.id)
    #     querysets = queryset.union(query)
    #     self.fields["asset"].queryset = querysets

    asset = forms.ModelMultipleChoiceField(
        queryset=Asset.objects.all())

    employee = forms.ModelChoiceField(
        queryset=Employee.objects.all()
    )

    date_of_assign = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "class": "form-control",
                "type": "date",
            }
        )
    )

    class Meta:
        model = AssignAsset
        fields = ["asset", "employee", "date_of_assign"]
