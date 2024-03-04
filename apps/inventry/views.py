# Python Imports
from datetime import timedelta, date
from datetime import datetime

# Django Imports
from django.views import View
from django.contrib.auth.models import auth
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.hashers import check_password
from django.views.generic.list import ListView
from django.urls import reverse
from django.db.models import Sum
from django.forms.models import model_to_dict
from django.utils.timezone import make_aware
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin

# Project Imports
from .forms import(
    AssetForm,
    EmployeeForm,
    VendorForm,
    AssignedAssetForm,
    AssetTypeForm,ClientForm,
    AssignedAssetsForm
)
from .models import *
from .utils import (
    get_total_number_of_employees,
    get_asset_item_list,
    get_today_assigned_asset,
    get_yesterday_assigned_asset,
    get_total_asset_quantity,
    get_total_client_asset_quantity,
    group_and_sum_asset_counts,
    dashboard_data,
    vendor_details_info,
)

# Third Party Imports


class DashboardView(LoginRequiredMixin,View):
    """
    A view that renders the dashboard page, which displays various statistics and data related to assets and employees.

    Methods:
    -------
    get(self, request):
        Retrieves the necessary data and renders the dashboard template with the context.
    
    Attributes:
    ----------
    template_name : str
        The name of the template to be rendered.

    Parameters:
    ----------
    request : HttpRequest
        The HTTP request object.

    Returns:
    -------
    HttpResponse
        The HTTP response object containing the rendered dashboard template.
    """

    template_name = "dashboard/dashboard.html"

    def get(self, request):
        today_date = date.today()
        yesterday_date = today_date - timedelta(1)
    
        context = {
                "today": get_today_assigned_asset(today_date),
                "yesterday": get_yesterday_assigned_asset(yesterday_date),
                "total_asset_quantity": get_total_asset_quantity(),
                "all_assets": get_asset_item_list(),
                "total_employee": get_total_number_of_employees(),
                "total_asset_type": len(Asset.objects.all()),
                "asset_type_query": dashboard_data(),
                "total_remaining_asset": Asset.objects.filter(is_assign=False).count(),
                'total_client_asset': get_total_client_asset_quantity(),
                'remaining_assets': group_and_sum_asset_counts(),
                'total_price' : Asset.objects.aggregate(Sum('price'))['price__sum'],
                'total_remaining_price' : Asset.objects.filter(is_assign=False).aggregate(Sum('price'))['price__sum']
            }
        return render(request, self.template_name, context)


class LoginView(View):
    """
    A view for handling user authentication.

    GET requests display the login form if the user is not already authenticated.
    POST requests validate user credentials and either log the user in and redirect to the dashboard,
    or display an error message and render the login form again.

    Template: 'dashboard/login_page.html'
    """

    template_name = "dashboard/login_page.html"
    def get(self, request):
        """
        Render the login form if the user is not already authenticated.

        Returns:
            A rendered HTML template with the login form.
        """

        if request.user.is_authenticated:
            return redirect("dashboard")
        else:
            return render(request, self.template_name)

    def post(self, request):
        """
        Validate user credentials and handle the login form submission.

        If the form is submitted with valid credentials, log the user in and redirect to the dashboard.
        Otherwise, display an error message and render the login form again.

        Returns:
            A redirect to the dashboard if login is successful, or a rendered HTML template with the
            login form and error message if the credentials are invalid.
        """

        if request.method == "POST":
            username = request.POST["username"]
            password = request.POST["password"]

            user = auth.authenticate(username=username, password=password)

            if user is not None:
                auth.login(request, user)
                messages.success(request, "Login Successfully")
                return redirect("dashboard/")
            else:
                messages.warning(request, "Invalid Credentail")
                return render(request, self.template_name)


class SignoutView(LoginRequiredMixin,View):
    """
    A view for handling user sign out.

    GET requests log the user out and redirect to the home page.

    """
     
    def get(self, request):
        """
        Log the user out and redirect to the home page.

        Returns:
            A redirect to the home page after the user is logged out.
        """

        logout(request)
        return redirect("/")


class RemainingAssetView(LoginRequiredMixin, View):
    """
    A view for displaying the remaining assets.
    """
    template_name = "dashboard/remaining_assert.html"

    def get(self, request):
        """
        Render the remaining asset template.

        Returns:
            A rendered remaining asset template.
        """
        return render(request, self.template_name)


class ProfileView(LoginRequiredMixin, View):
    """
    A view for displaying the user profile.
    """
    template_name = "dashboard/user_profile.html"

    def get(self, request):
        """
        Render the user profile template.

        Returns:
            A rendered user profile template.
        """
        current_user = request.user
        context = {"user": current_user}
        return render(request, self.template_name, context)


class AssetCreateView(LoginRequiredMixin, View):
    """
    A view for creating new assets.
    """
    template_name = "inventory/asset.html"
    form_class = AssetForm

    def get(self, request):
        """
        Render the asset creation form template.

        Returns:
            A rendered asset creation form template.
        """
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        """
        Handle the submission of the asset creation form.

        Returns:
            A redirect to the asset list page on success, or a re-rendered
            asset creation form on error.
        """
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Asset successfully created.")
            return redirect(reverse("asset-list"))
        else:
            return render(request, self.template_name, {"form": form})

class AssetTypeCreationView(LoginRequiredMixin,View):

    """
    A view for creating new asset types.

    Attributes:
        template_name (str): The name of the HTML template to use.
        form_class (class): The form to use for creating new asset types.
    """
    template_name = "inventory/asset_type.html"
    form_class = AssetTypeForm

    def get(self, request):
        """
        Handle GET requests to the view.

        Returns:
            A rendered HTML template containing the form for creating a new asset type.
        """

        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        """
        Handle POST requests to the view.

        If the form data is valid and the asset type does not already exist, create a new asset type and redirect
        the user to the list of all asset types. Otherwise, display an error message and render the form again.

        Returns:
            A redirect to the list of all asset types, or a rendered HTML template containing the form and error message.
        """

        try:
            form = self.form_class(request.POST)

            if form.is_valid():
                form.save()
                messages.success(
                    request, f"AssetsType created successfully"
                )
                return redirect("asset-type-list")
            else:
                messages.warning(request, "this asset is already exist")
            return render(request, self.template_name, {"form": form})
        except Exception as e:
            messages.error(request, e)
            return render(request, self.template_name, {"form": form})


class AssetListView(LoginRequiredMixin,View):
    """
    A view to display a list of all assets or filter them by asset type name.
    
    """
    template_name = "inventory/asset_list.html"

    def get(self, request):
        """
        Handles GET requests to display the list of all assets.

        Returns:
            A rendered HttpResponse instance containing the list of assets.
        """

        asset_list = Asset.objects.all()
        context = {"asset_list": asset_list}
        return render(request, self.template_name, context)
    
    def post(self, request):
        """
        Handles POST requests to filter the list of assets by asset type name.

        Args:
            request: A HttpRequest instance.

        Returns:
            A rendered HttpResponse instance containing the filtered list of assets.
        """
        name = request.POST.get("name")
        asset = Asset.objects.filter(asset_type__asset_name__contains=name)
        context = {"asset_list": asset}
        return render(request, self.template_name, context)


class AssetDeleteView(LoginRequiredMixin, View):
    """
    View for deleting an asset.
    """

    template_name = "inventory/asset_list.html"

    def get(self, request, asset_id):
        """
        Handles GET requests for deleting an asset.
        
        Parameters:
        - request: HTTP request object.
        - asset_id: ID of the asset to be deleted.
        
        Returns:
        - Redirects to the asset list page.
        """
        try:
            asset = Asset.objects.get(id=asset_id)
            if AssignAsset.objects.filter(asset=asset.id).exists():
                assign = AssignAsset.objects.get(asset=asset.id)
                assign.delete()
            asset.delete()
            messages.success(request, "Asset deleted successfully.")
        except Asset.DoesNotExist:
            messages.error(request, "Asset not found.")
        except AssignAsset.DoesNotExist:
            messages.error(request, "Assigned asset not found.")
        except Exception as e:
            messages.error(request, str(e))
        
        return redirect("asset-list")


class AssetUpdateView(LoginRequiredMixin,View):
    """
    View to update an asset instance.
    """
    template_name = "inventory/asset_edit.html"

    def get(self, request, asset_id):
        """
        Handles GET requests to retrieve the asset to be updated and renders the edit form.

        Args:
            request (HttpRequest): The HTTP request object.
            asset_id (int): The ID of the asset to be updated.

        Returns:
            HttpResponse: The HTTP response containing the edit form for the asset.
        """
        try:
            asset = Asset.objects.get(id=asset_id)
            if asset.payment_status == 'done':
                form = AssetForm(instance=asset)
            else:
                form = AssetForm()
        except Asset.DoesNotExist:
            messages.error(request, f"Asset with ID {asset_id} does not exist.")
            return redirect("asset-list")
        return render(request, self.template_name, {"form": form})
    
    def post(self, request, asset_id):
        """
        Handles POST requests to update the asset instance.

        Args:
            request (HttpRequest): The HTTP request object.
            asset_id (int): The ID of the asset to be updated.

        Returns:
            HttpResponse: The HTTP response containing either the updated asset list or the edit form with errors.
        """
        try:
            asset = Asset.objects.get(id=asset_id)
            form = AssetForm(request.POST, instance=asset)
            if form.is_valid():
                form.save()
                messages.success(request, f"Asset with ID {asset_id} has been updated.")
                return redirect("asset-list")
        except Asset.DoesNotExist:
            messages.error(request, f"Asset with ID {asset_id} does not exist.")
            return redirect("asset-list")
        except Exception as e:
            messages.error(request, f"An error occurred while updating asset with ID {asset_id}: {str(e)}")
        return render(request, self.template_name, {"form": form})


class EmployeeListView(LoginRequiredMixin, View):
    """
    View to display the list of active employees.
    """
    template_name = "inventory/employee_table.html"

    def get(self, request):
        """
        Handles GET requests to retrieve and display the list of active employees.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: The HTTP response containing the rendered employee table template and the list of active employees.
        """

        employee_list = Employee.objects.filter(is_active=True)
        context = {"employee_list": employee_list}
        return render(request, self.template_name, context)


class AssignAssetListView(LoginRequiredMixin,View):
    """
    View to display the list of AssignAsset list
    """
    template_name =  "inventory/assign_assets.html"
    def get(self, request):
        """
        Handles GET requests to retrieve and display the list of AssignAssets 

        Args:
            request (HttpRequest): The HTTP request object

         Retruns:
           HttpResponse: The HTTP response containing the rendered assign assets  templates and the list of assign assets  
        """
        assing_assets_list = AssignAsset.objects.all()
        context = {"assing_assets_list": assing_assets_list}
        return render(request,self.template_name, context)

  
  

class EmployeeCreateView(LoginRequiredMixin,View):
    """
    View for creating a new employee. Requires login authentication.
    
    """
    template_name = "inventory/employee_table.html"
    form_class = EmployeeForm


    def get(self, request):
        """
        Handle GET request to display empty employee creation form.
        """

        form = self.form_class()
        return render(request, "inventory/employee_create.html", {"form": form})

    def post(self, request):
        """
        Handle POST request to create a new employee.

        """
        try:
            form = self.form_class(request.POST)

            if form.is_valid():
                
                emp = form.save()
                
                messages.success(
                    request, f"Employee {emp.first_name}  is created successfully."
                )
                return redirect("employee-list")
            else:
                form = EmployeeForm(request.POST)
                messages.error(request, form.errors)
                return redirect('employee-create'
                )
        except Exception as e:
            messages.error(request, e)
            return render(
                request, "inventory/employee_create.html", {"form": self.form_class()}
            )


class VendorCreationView(LoginRequiredMixin,View):
    """
    View for creating a new Vendor object.

    Attributes:
        template_name (str): The path to the HTML template for this view.
        form_class (VendorForm): The form class used to create and validate Vendor objects.
    """
    template_name = "inventory/vendor.html"
    form_class = VendorForm

    def get(self, request):
        """
        Render a blank form for creating a new Vendor object.

        Returns:
            A rendered HTML template containing a blank form for creating a new Vendor object.
        """

        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        """
        Handle form submission for creating a new Vendor object.

        Args:
            request (HttpRequest): The request object containing the submitted form data.

        Returns:
            A redirect to the list view of all Vendor objects on successful form submission,
            or a re-rendered form with validation errors displayed on failed form submission.
        """
        try:
            form = self.form_class(request.POST)
            if form.is_valid():
                vendor = form.save()
                messages.success(
                    request, f"Vendor {vendor.first_name}  is created successfully."
                )
                return redirect("vendor-list")
            else:
                form = VendorForm(request.POST)
                messages.error(request, form.errors)

                return render(
                    request, self.template_name, {"form": self.form_class()}
                )
        except Exception as e:
            form = self.form_class()
            messages.error(request, e)
            return render(request, self.template_name, {"form", form})


class VendorListView(LoginRequiredMixin,View):
    """
    View for displaying a table of all active Vendor objects.

    Attributes:
        template_name (str): The path to the HTML template for this view.
    """
     
    template_name = "inventory/vendor_table.html"

    def get(self, request):
        """
        Retrieve all active Vendor objects and render them in a table.

        Returns:
            A rendered HTML template containing a table of all active Vendor objects.
        """

        vendor_list = Vendor.objects.all().order_by("created_at").exclude(is_active=False)
        context = {"vendor_list": vendor_list}
        return render(request, self.template_name, context)


class ChangePasswordView(LoginRequiredMixin, View):
    """
    View for allowing users to change their password.

    """
    def post(self, request):
        """
        Handle form submission for changing the user's password.

        Args:
            request (HttpRequest): The request object containing the submitted form data.

        Returns:
            A redirect to the user's profile page with a success or error message.
        """
        current_password = request.POST.get("password")
        new_password = request.POST.get("newpassword")
        retype_new_password = request.POST.get("renewpassword")
        current_user = request.user

        if check_password(current_password, current_user.password):
            if new_password == retype_new_password:
                current_user.set_password(new_password)
                current_user.save()
                messages.success(request, "Password successfully changed.")
            else:
                messages.warning(request, "New password and retype password do not match.")
        else:
            messages.warning(request, "Current password is invalid.")
        
        return redirect("/dashboard/profile")


class Asset_ListDetail(LoginRequiredMixin, View):
    """
    View for displaying a filter Assets data based on assets names.

    Attributes:
        template_name (str): The path to the HTML template for this view.
    """
    def get(self, request, asset):
        context = {}
        asset_name = asset
        assets = Asset.objects.filter(asset_type__asset_name=asset_name)
        context = {"asset_data": assets}
        return render(request, "dashboard/assets_records_list.html", context)


class AssignAssignDetailView(LoginRequiredMixin, View):
    """
    View for displaying a single AssignAsset record.

    Attributes:
        template_name (str): The path to the HTML template for this view.
    """
    template_name = "inventory/emp_assets_assign.html"

    def get(self, request, employee, asset):
        """
        Retrieve and render a single AssignAsset record for the specified employee and asset.

        Args:
            request (HttpRequest): The request object containing the employee and asset IDs.
            employee_id (int): The ID of the employee to retrieve the record for.
            asset_id (int): The ID of the asset to retrieve the record for.

        Returns:
            A rendered HTML template containing a single AssignAsset record for the specified employee and asset.
        """
        emp_records = AssignAsset.objects.filter(employee_id=employee, id=asset)
        return render(request, self.template_name, {'emp_records': emp_records})


class AssetTypeListView(LoginRequiredMixin, View):
    """
    View for displaying a list of all AssetType objects.

    Attributes:
        template_name (str): The path to the HTML template for this view.
    """
    template_name = "inventory/asset_type_table.html"

    def get(self, request, *args, **kwargs):
        """
        Retrieve a list of all AssetType objects and render them as an HTML table.

        Args:
            request (HttpRequest): The request object.

        Returns:
            A rendered HTML template containing a list of all AssetType objects.
        """
        asset_types = AssetType.objects.all()
        return render(request, self.template_name, {"page_obj": asset_types})


class AssetTypeDeleteView(LoginRequiredMixin, View):
    """
    View for deleting an AssetType object.

    Attributes:
        template_name (str): The path to the HTML template for this view.
    """
    template_name = "inventory/asset_type_table.html"

    def get(self, request, asset_type_id):
        """
        Delete an AssetType object.

        Args:
            request (HttpRequest): The request object.
            asset_type_id (int): The ID of the AssetType object to delete.

        Returns:
            If the deletion is successful, redirect to the AssetType list page.
            Otherwise, render the asset type table page with an error message.
        """
        try:
            asset_type = AssetType.objects.get(id=asset_type_id)
            asset_type.delete()
            messages.success(request, "Asset type deleted successfully.")
            return redirect("asset-type-list")
        except AssetType.DoesNotExist:
            messages.error(request, "Asset type not found.")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")

        return render(request, self.template_name)

class AssignAssetDeleteView(LoginRequiredMixin, View):
    """
    View to delete an assigned asset for a specific employee.
    """

    template_name = "inventory/assign_assets.html"

    def get(self, request, employee_id, asset_id):
        """
        Handle GET requests to delete an assigned asset.

        Parameters:
            request (HttpRequest): The HTTP request object.
            employee_id (int): The ID of the employee for whom the asset was assigned.
            asset_id (int): The ID of the asset that was assigned.

        Returns:
            HttpResponseRedirect: Redirects to the 'assign-assets-list' URL pattern.

        Raises:
            Http404: If the assigned asset does not exist.
        """
        try:
            assign_asset = AssignAsset.objects.get(employee__id=employee_id,asset__id=asset_id)
            assest = assign_asset.asset
            assest.is_assign=False
            assest.save()
            assign_asset.delete()
            messages.success(request, "Assigned asset deleted successfully.")
            return redirect('assign-assets-list')
        except AssignAsset.DoesNotExist:
             messages.error(request, "Asset type not found.")
        except Exception as e:
            messages.error(request, str(e))

        return redirect("assign-assets-list")


class AssignAssetEditView(LoginRequiredMixin, View):
    """
    View to Edit AssignAsset for specific asset
    """ 
    template_name = "inventory/assign_asset_edit.html"
    
    def get(self,request, asset_id):
        """
        Renders the assigned asset edit form.

        Parameters
        ----------
        request : HttpRequest
            The HTTP request object.
        asset_id : int
            The ID of the assigned asset to edit.

        Returns
        -------
        HttpResponse
            The HTTP response object that contains the assigned asset edit form.
        """
        try:
            asset = AssignAsset.objects.get(id=asset_id)
            form = AssignedAssetsForm(initial=model_to_dict(asset))
            return render(request, self.template_name, {"form": form})
        except AssignAsset.DoesNotExist:
            messages.error(request, f"Assigned asset with ID {asset_id} does not exist.")
            return redirect("assigned-assets-list")

    def post(self, request, asset_id):
        try:
            assign_asset = AssignAsset.objects.get(id = asset_id)
            assets = request.POST.get("asset")
            employee = request.POST.get("employee")
            date = request.POST.get("date_of_assign")
            employee_obj = Employee.objects.get(id = employee)
            asset_obj = Asset.objects.get(id = assets)
            alreay_assigned = AssignAsset.objects.filter(asset=assets).exclude(id=asset_id).exists()

            if not alreay_assigned:
                assign_asset.employee = employee_obj
                assign_asset.asset = asset_obj
                assign_asset.date_of_assign = make_aware(datetime.strptime(date, '%Y-%m-%d'))
                assign_asset.save()
                return redirect("/dashboard/assign/assets/list/")
            else:
                messages.success(
                    request, "Employee already assigned this asset."
                )
                return redirect("assign-assets-list")

        except Exception as e:
            return redirect('assign-assets-list')

class EmployeeDeleteView(LoginRequiredMixin, View):
    def get(self, request, employee_id):
        """
        Handle GET requests to delete an Employee.

        Args:
            request (HttpRequest): The HTTP request object.
            employee_id (int): The ID of the Employee to delete.

        Returns:
            HttpResponseRedirect: Redirects to the 'employee-list' URL.

        """
        try:
            employee_obj = Employee.objects.get(employee_id=employee_id)
            assets_assign = AssignAsset.objects.filter(employee=employee_obj.id)
            if assets_assign:
                Asset.objects.filter(id=assets_assign.asset.id).update(is_assign=False)
                assets_assign.delete()
            employee_obj.delete()
            messages.success(request, "Employee deleted successfully.")
        except Employee.DoesNotExist:
            messages.error(request, "Employee does not exist.")
        except Exception as e:
            messages.error(request, str(e))

        return redirect("employee-list")
        
class EmployeeUpdateView(LoginRequiredMixin, View):
    """
    View to update Employee based on employee ID.
    """
    template_name = "inventory/emp_update.html"
    def get(self, request, employee_id):
        """
        Handle GET requests to update Employee
        """
        emp_details = Employee.objects.filter(employee_id=employee_id).first()
        form = EmployeeForm(initial=model_to_dict(emp_details))
        return render(request, self.template_name, {"form": form})
    
    def post(self, request, employee_id):
        """
        Handles the submission of the employee update form.

        Args:
            request (HttpRequest): The HTTP request object.
            employee_id (int): The ID of the employee to update.

        Returns:
            HttpResponseRedirect: A redirect to the employee list page if the form is valid, else a re-rendering of the form.
        """
        try:
            emp = Employee.objects.filter(employee_id=employee_id).first()
            form = EmployeeForm(request.POST, instance=emp)

            if form.is_valid():
                form.save()
                return redirect("employee-list")
            return render(request, self.template_name, {"form": form})
        except Exception as e:
            messages.error(e)
            return redirect("employee-list")


class VendorUpdateView(LoginRequiredMixin, View):
    """
    View to Update Vendor records
    """
    template_name = "inventory/vendor_update.html"
    def get(self, request, id):
        """
        Handle GET request to display the form for updating a vendor's information.

        Parameters:
        - request: the HTTP request object
        - id: the ID of the vendor to be updated

        Returns:
        - a rendered HTTP response with the vendor update form
        """
        vendor = Vendor.objects.filter(id=id).first()
        form = VendorForm(initial=model_to_dict(vendor))
        return render(request, self.template_name, {"form": form})

    def post(self, request, id):
        """
        Handle POST request to update a vendor's information.

        Parameters:
        - request: the HTTP request object
        - id: the ID of the vendor to be updated

        Returns:
        - a redirect to the vendor list if the vendor is successfully updated, or a render of the form with errors if the form is invalid
        """
        try:
            vendor = Vendor.objects.filter(id=id).first()
            form = VendorForm(request.POST, instance=vendor)

            if form.is_valid():
                form.save()
                return redirect("vendor-list")
            return render(request, self.template_name, {"form": form})
        except Exception as e:
            messages.error(e)
            return redirect("vendor-list")


class EmployeeDetailsView(LoginRequiredMixin, View):
    """
    View to show Details of Employee
    """
    template_name = "inventory/employee_details.html"
    def get(self, request,employee_id):
        """
        HTTP GET method to display details of an employee's assigned assets and client assets.

        Args:
        request (HttpRequest): The HTTP request object.
        employee_first_name (str): The first name of the employee whose assets to display.

        Returns:
        Rendered HTML template with the details of the employee's assigned assets and client assets.
        """

        try:
            employee = Employee.objects.get(id=employee_id)
            employee_asset = AssignAsset.objects.filter(employee=employee)
            emp_clientasset = ClientAsset.objects.filter(employee=employee).select_related('asset_type')

            context = {
                "emp": employee,
                "employee_asset": employee_asset,
                "emp_clientasset": emp_clientasset,
            }
            return render(request, self.template_name, context)

        except Employee.DoesNotExist:
            messages.error(request, "Employee not found.")
            return redirect("employee-list")


class VendorDetailsView(LoginRequiredMixin, View):
    """
    View to display vendor details along with their assets and assigned assets.

    Attributes:
        template_name (str): The name of the template used to render the view.

    Methods:
        get: Retrieve vendor details and related data from the database and render the view.
    """
    template_name = "inventory/vendor_details.html"

    def get(self, request, id):
        """
        Retrieve vendor details and related data from the database and render the view.

        Args:
            request (HttpRequest): The HTTP request object.
            id (int): The ID of the vendor to retrieve.

        Returns:
            HttpResponse: The rendered view with context data.
        """
        vendor_details = Vendor.objects.get(id=id)
        vendor_asset = Asset.objects.filter(vendor=id)
        vendor_assign_asset=Asset.objects.filter(vendor=id,is_assign=True)
        asset_id_list = []
        for data in vendor_assign_asset:
            asset_id_list.append(data.id)
        assign_asset_details = AssignAsset.objects.filter(asset__in=asset_id_list)
        asset_result = vendor_details_info(id)
        context = {
            "vendor": vendor_details,
            "vendor_asset": vendor_asset,
            "output":asset_result,
            "assign_asset_details": assign_asset_details,
        }
        return render(request, self.template_name, context)


class VendorDeleteView(LoginRequiredMixin, View):
    """
        Deletes a vendor instance and redirects to the vendor list page.

        Args:
            request (HttpRequest): the HTTP request object.
            id (int): the id of the vendor instance to be deleted.

        Returns:
            HttpResponse: a redirect response to the vendor list page.

        Raises:
            Exception: if the vendor instance could not be deleted.
    """
    def get(self, request, id):
        try:
            vendor = Vendor.objects.get(id=id)
            vendor.is_active = False
            vendor.delete()
            return redirect("vendor-list")
        except Exception as e:
            messages.error(e)


class CreateAssignAssetView(LoginRequiredMixin, View):

    template_name = "dashboard/create.html"
    def get(self, request):
        form = AssignedAssetForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        try:
            form = AssignedAssetForm(request.POST)
            if form.is_valid():
                assets = form.cleaned_data.get("asset")
                employee = form.cleaned_data.get("employee")
                date = form.cleaned_data.get("date_of_assign")
                for asset in assets:
                    alreay_assigned = AssignAsset.objects.filter(
                        asset=asset, employee=employee
                    ).exists()
                    if not alreay_assigned:
                        assigned = AssignAsset.objects.create(
                            asset=asset, employee=employee,date_of_assign = date
                        )
                        asset.is_assign = True
                        assigned.save()
                        asset.save()
                        return redirect("assign-assets-list")
                    else:
                        messages.success(
                            request, "Employee already assigned this asset."
                        )
                        return redirect("/dashboard/assign/asset/create/")

                messages.success(request, "Employee data saved")
                return redirect("/dashboard/assign/assets/list/")
            else:
                return render(request, self.template_name, {"form": form})
        except Exception as e:
            return redirect("/dashboard/assign/asset/create/")


class ClientList(LoginRequiredMixin, ListView):
    """
        A view that displays a list of client assets on a web page. 

        Requires the user to be authenticated. 

        Attributes:
        template_name (str): The name of the template file used to render the HTML content.

        Methods:
        get(self, request): Retrieves the list of client assets from the database and passes it to the context 
        dictionary before rendering the HTML response.
    """ 
    template_name = "inventory/client.html"

    def get(self, request):
        client_list = ClientAsset.objects.all()
        context =  {'object_list':client_list}
        return render(request,self.template_name, context)


class ClientCreateView(LoginRequiredMixin, View):
    template_name = "inventory/client_create.html"

    def get(self, request):
        form = ClientForm()
        asset_type = AssetType.objects.all()
        employee = Employee.objects.all()
        context = {"form": form, 'asset_type':asset_type, 'employee':employee}
        return render(request,self.template_name , context)
    
    def post(self, request):
        client_name = request.POST['client']
        pro = request.POST.get('project')
        config = request.POST['configuration']
        Asset_brand = request.POST['asset_brand']
        Asset_type = request.POST['asset_type']
        Assetname = AssetType.objects.get(asset_name=Asset_type)
        emp = request.POST['employee']
        employee = Employee.objects.get(email=emp)
        pro_owner = request.POST['project_owner']
        serial_number = request.POST['serial_number']
        ram = request.POST['ram']
        ssd = request.POST['ssd']
        processor = request.POST['processor']
        operating_system = request.POST['operating_system']
        storage = request.POST['storage']
        dispatch = request.POST.get('dispatch')
        if dispatch is None:
            dispatch = False
        else:
            dispatch = True
            
        date_of_dispatch = request.POST['date_of_dispatch']
        if date_of_dispatch == '':
            date_of_dispatch = None
        description = request.POST['description']
        if description == '':
            description = None
        obj = ClientAsset(client_name=client_name, project=pro, configuration=config, asset_brand=Asset_brand,
                          asset_type=Assetname, employee=employee, project_owner=pro_owner,
                          is_dispatch=dispatch, date_of_dispatch=date_of_dispatch, description=description,
                          serial_number=serial_number, ram=ram, ssd=ssd, processor=processor, operating_system=operating_system,
                          storage=storage)
        
        if obj.is_dispatch == True:
            obj.is_active = False
        obj.save()    
        return redirect("client-list")


class ClientUpdateView(LoginRequiredMixin, View):
    """
    A view for updating client asset details.

    Requires the user to be authenticated.

    Methods:
        get(self, request, id): Renders the form with the client asset's current details.
        post(self, request, id): Updates the client asset with the submitted form data and saves it to the database.
    """
    template_name = "inventory/client_update.html"

    def get(self, request, id):
        client_details = ClientAsset.objects.filter(id=id).first()
        form = ClientForm(initial=model_to_dict(client_details))
        return render(request, self.template_name, {"form": form})

    def post(self, request, id):
        try:
            client = ClientAsset.objects.filter(id=id).first()
            form = ClientForm(request.POST, instance=client)
            if form.is_valid():
                form.save()
                if client.is_dispatch:
                    client.is_active =False
                else:
                    client.is_active = True    
                client.save()    
                return redirect("client-list")
            return render(request, self.template_name, {"form": form})
        except Exception as e:
            messages.error(request,e)
            return redirect("client-update",id=id)

class ClientDeleteView(LoginRequiredMixin, View):
    def get(self, request, id):
        """
        Handles GET requests and to Delete ClientAssets 

        Returns:
            request redirect to the client-list
        """
        try:
            client = ClientAsset.objects.get(id=id)
            client.delete()
            return redirect("client-list")
        except Exception as e:
            res = {"error": str(e)}
            messages.error(e)
            return redirect("client-list")

class AssetDetailsView(LoginRequiredMixin, View):
    template_name = "inventory/asset_details.html"
    def get(self, request, asset_id):
        """
        Handles GET requests and returns the HTTP response with the asset details
            Based on assets ID.

        Args:
            request (HttpRequest): The HTTP request object.
            asset_name (str): The name of the asset type.

        Returns:
            HttpResponse: The HTTP response with the asset details.
        """
        asset_details = Asset.objects.all().filter(id=asset_id)
        context =  {"asset_details": asset_details}
        return render(request, self.template_name, context)


class RemainingAssetListView(LoginRequiredMixin, View):
    template_name = "inventory/remaining_assest_list.html"
    def get(self,request):
        """
        Handles GET requests and returns the HTTP response with the asset details.

        Args:
            request (HttpRequest): The HTTP request object.
            asset_name (str): The name of the asset type.

        Returns:
            HttpResponse: The HTTP response with the asset details.
        """
        remaining_assets = Asset.objects.filter(is_assign=False)
        context = {"remaining_assets": remaining_assets}
        return render(request, self.template_name, context)


class TotalAssetDetailsView(LoginRequiredMixin, View):
    template_name = "inventory/total_asset_detail.html"
    def get(self, request, asset_name):
        """
        Handles GET requests and returns the HTTP response with the asset details.

        Args:
            request (HttpRequest): The HTTP request object.
            asset_name (str): The name of the asset type.

        Returns:
            HttpResponse: The HTTP response with the asset details.
        """
        asset_details = Asset.objects.filter(asset_type__asset_name = asset_name)
        context = {"asset_details": asset_details}
        return render(request, self.template_name, context)


class VendorTotalAssetDetailsView(LoginRequiredMixin, View):
    template_name = "inventory/total_asset_detail.html"

    def get(self, request, asset_name, vendor_id):
        """
        Handles GET requests and returns the HTTP response with the asset details.

        Args:
            request (HttpRequest): The HTTP request object.
            asset_name (str): The name of the asset type.
            vendor_id (int): The ID of the vendor.

        Returns:
            HttpResponse: The HTTP response with the asset details.
        """
        asset_details = Asset.objects.filter(asset_type__asset_name = asset_name,vendor__id = vendor_id).select_related("asset_type", "vendor")
        context = {"asset_details": asset_details}
        return render(request, self.template_name, context)


class TotalDashboardAssetDetailsView(LoginRequiredMixin, View):
    """
    A view for displaying the total assets by asset type and brand.

    Requires the user to be authenticated.

    Attributes:
        template_name (str): The name of the template file used to render the HTML content.

    Methods:
        get(self, request): Retrieves the total assets by asset type and brand and passes it to the context 
        dictionary before rendering the HTML response.
    """
    template_name = "inventory/dashboard_total_assets.html"

    def get(self, request):
        asset_typ = Asset.objects.all().values_list('asset_brand', flat=True).distinct()
        
        asset_list = []
        for brand_name in asset_typ:    
            obj = Asset.objects.filter(asset_brand=brand_name)
            for data in obj:
                remaining = 0
                d = {}
                if data.asset_type.asset_name in d:
                    d["asset_type"] = data.asset_type.asset_name
                    d["asset_price"] += data.price
                    d['count'] += 1
                else:
                    d["asset_type"] = data.asset_type.asset_name
                    d["asset_price"] = data.price
                    d['count'] = 1
                if data.is_assign:
                    remaining = 0
                    d['remaining'] = remaining
                else:
                    remaining += 1 
                    d['remaining'] = remaining      
                asset_list.append(d)

        result = []
        for asset in asset_list:
            found = False
            for res in result:
                if res['asset_type'] == asset['asset_type']:
                    res['count'] += 1
                    res['asset_price'] += asset['asset_price']
                    res['remaining'] += asset['remaining']
                    found = True
                    break
            if not found:
                result.append(asset)
        context = {"asset_details": result}        
        return render(request, self.template_name, context)


class TotalRemainingAssetDetailsView(LoginRequiredMixin, View):
    """
    A view for displaying the total remaining assets by asset type and brand.

    Requires the user to be authenticated.

    Attributes:
        template_name (str): The name of the template file used to render the HTML content.

    Methods:
        get(self, request): Retrieves the total remaining assets by asset type and brand and passes it to the context 
        dictionary before rendering the HTML response.
    """
    template_name = "inventory/total_remaining_assets.html"

    def get(self, request):
        asset_typ = Asset.objects.all().values_list('asset_brand', flat=True).distinct()
        asset_list = []
        for brand_name in asset_typ:    
            obj = Asset.objects.filter(asset_brand=brand_name,is_assign=False)
            for data in obj:
                remaining = 0
                d = {}
                if data.asset_type.asset_name in d:
                    d["asset_type"] = data.asset_type.asset_name
                    d["asset_price"] += data.price
                    d['count'] += 1
                else:
                    d["asset_type"] = data.asset_type.asset_name
                    d["asset_price"] = data.price
                    d['count'] = 1
                if data.is_assign:
                    remaining = 0
                    d['remaining'] = remaining
                else:
                    remaining += 1 
                    d['remaining'] = remaining      
                asset_list.append(d)
        asset_details = []
        for asset in asset_list:
            found = False
            for res in asset_details:
                if res['asset_type'] == asset['asset_type']:
                    res['count'] += 1
                    res['asset_price'] += asset['asset_price']
                    res['remaining'] += asset['remaining']
                    found = True
                    break
            if not found:
                asset_details.append(asset)
        context = {"asset_details": asset_details}        
        return render(request,self.template_name, context)


class TotalReaminingAssetDetailsView(LoginRequiredMixin, View):

    template_name = "inventory/total_asset_detail.html"
    def get(self, request, asset_name):
        """
        View to display the total remaining assets of a specific asset type.

        Args:
            asset_name (str): The name of the asset type to filter the assets by.

        Returns:
            A rendered HTML template displaying a table of the remaining assets of the specified asset type.
        """
        asset_details = Asset.objects.filter(asset_type__asset_name = asset_name,is_assign=False)
        context = {"asset_details": asset_details}
        return render(request, self.template_name, context)


def assign_asset_count(request,employee):
    """
    Returns a JSON response containing a list of dictionaries with details of assets assigned to a given employee.

    Args:
        request: HttpRequest object.
        employee: Email address of the employee to get asset details for.

    Returns:
        JsonResponse containing a list of dictionaries with asset details.
    """
    assets = AssignAsset.objects.filter(employee__email=employee)
    list_asset = []
    for details in assets:
        assets_dict = {}
        assets_dict['brand'] = details.asset.asset_brand
        assets_dict['type'] = details.asset.asset_type.asset_name
        assets_dict['ram'] = details.asset.ram
        assets_dict['processor'] = details.asset.processor
        assets_dict['operating_system'] = details.asset.operating_system
        assets_dict['system_configuration'] = details.asset.system_configuration
        list_asset.append(assets_dict)
    return JsonResponse({'assets_dict': list_asset})
