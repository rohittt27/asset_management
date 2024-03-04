# Python Imports

# Django Imports
from django.urls import path

# Project Imports
from apps.inventry import views


# URLs for dashboard-related views
dashboard_urls = [

    path("", views.DashboardView.as_view(), name="dashboard"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("change/password/", views.ChangePasswordView.as_view(), name="change-password"),
    path("remainig_asset/", views.RemainingAssetView.as_view(), name="remainig_asset"),
]


# URLs for employee-related views
employee_urls = [

    path("employee/list/", views.EmployeeListView.as_view(), name="employee-list"),
    path("employee/create/", views.EmployeeCreateView.as_view(), name="employee-create"),
    path("client/update/<int:id>/", views.ClientUpdateView.as_view(), name="client-update"),
    path("client/delete/<int:id>/", views.ClientDeleteView.as_view(), name="client-delete"),
    path("employee/delete/<str:employee_id>/", views.EmployeeDeleteView.as_view(), name="employee_delete"),
    path("employee_update/<str:employee_id>/", views.EmployeeUpdateView.as_view(), name="employee_update"),
    path('employee_details/<str:employee_id>/', views.EmployeeDetailsView.as_view(), name="employee_details"),
    ]


# URLs for vendor-related views
vendor_urls = [

    path('vendor/create/', views.VendorCreationView.as_view(), name='vendor-create'),
    path('vendor/list/', views.VendorListView.as_view(), name='vendor-list'),
    path("vendor/update/<int:id>/", views.VendorUpdateView.as_view(), name="vendor-update"),
    path("vendor/delete/<int:id>/", views.VendorDeleteView.as_view(), name="vendor-delete"),
    path('vendor_details/<int:id>/', views.VendorDetailsView.as_view(), name="vendor_details"),

]

# URLs for assets-related views
assets_urls = [

    path("asset/create/", views.AssetCreateView.as_view(), name="asset-create"),
    path("asset/list", views.AssetListView.as_view(), name="asset-list"),
    path("asset/edit/<int:asset_id>", views.AssetUpdateView.as_view(), name="asset-edit"),
    path("asset/delete/<int:asset_id>", views.AssetDeleteView.as_view(), name="asset_delete"),
    path("asset/details/<int:asset_id>", views.AssetDetailsView.as_view(), name="asset_details"),
    path("asset/detail/<str:asset_name>", views.TotalAssetDetailsView.as_view(), name="asset_detail"),
    path("total/assets/detail/", views.TotalDashboardAssetDetailsView.as_view(), name="total_asset_detail"),
    path("total/remaining/assets/detail/", views.TotalRemainingAssetDetailsView.as_view(), name="total_remaining_asset_detail"),
    path("assets/detail/<str:asset_name>", views.TotalReaminingAssetDetailsView.as_view(), name="asset_remaining_detail"),
    path("asset/detail/vendor/<str:asset_name>/<int:vendor_id>/", views.VendorTotalAssetDetailsView.as_view(), name="vendor_asset_detail"),
]

# URLs for assets_assign-related views
assign_assets_urls = [

    path("assign/asset/create/", views.CreateAssignAssetView.as_view(), name="assign-asset-create"),
    path("assign/asset/detail/<str:employee>/<int:asset>", views.AssignAssignDetailView.as_view(), name="assign-asset-detail"),
    path("assign/assets/list/", views.AssignAssetListView.as_view(), name="assign-assets-list"),
    path("assignassets/delete/<int:asset_id>/<str:employee_id>/", views.AssignAssetDeleteView.as_view(), name="assign-asset-delete"),
    path("assignassets/edit/<int:asset_id>/", views.AssignAssetEditView.as_view(), name="assign-asset-edit"),
    path("assets_record_list/<asset>/", views.Asset_ListDetail.as_view(), name="assets_record_list"),
    path("remaining/assets/list/", views.RemainingAssetListView.as_view(), name="remaining-assets-list"),
]   


# URLs for assets_type-related views
asset_type_urls = [

    path("asset/type/create", views.AssetTypeCreationView.as_view(), name="asset-type-create"),
    path("asset/type/list", views.AssetTypeListView.as_view(), name="asset-type-list"),
    path("asset/type/delete/<int:asset_type_id>", views.AssetTypeDeleteView.as_view(), name="asset-type-delete"),
]

# URLs for client-related views
client_urls = [

    path("client/create/", views.ClientCreateView.as_view(), name="client-create"),
    path("client/list/", views.ClientList.as_view(), name="client-list"),
    path("assignassets/count/<str:employee>", views.assign_asset_count, name="assign-asset-count")
    # path("client/assign/asset/", views.AssignAssetClientView.as_view(), name="client-assign-asset"),
]    


urlpatterns = client_urls + asset_type_urls + dashboard_urls + employee_urls + vendor_urls + assign_assets_urls + assets_urls
    
  