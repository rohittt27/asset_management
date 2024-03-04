# Python Imports

# Django Imports
from django.contrib import admin

# Projects Imports
from .models import User, Vendor, Asset, Employee, AssignAsset, AssetType, ClientAsset

# Third Party Imports
from import_export.admin import ImportExportModelAdmin



admin.site.register(User)

@admin.register(AssetType)
class AssetTypeAdmin(ImportExportModelAdmin):
    pass

@admin.register(Employee)
class EmployeeAdmin(ImportExportModelAdmin):
    pass


@admin.register(AssignAsset)
class AssignAssetAdmin(ImportExportModelAdmin):
    pass


@admin.register(Vendor)
class VendorAdmin(ImportExportModelAdmin):
    # list_display = ('id', 'first_name', 'last_name')
    pass


@admin.register(Asset)
class AssetAdmin(ImportExportModelAdmin):
    pass


@admin.register(ClientAsset)
class ClientAdmin(ImportExportModelAdmin):
    pass