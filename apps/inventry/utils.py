# Python Imports
from collections import defaultdict

# Django Imports
from django.db.models import Sum

# Project Imports
from .models import (
    AssetType, Asset, Employee, AssignAsset, ClientAsset
)


def get_total_number_of_employees():
    return Employee.objects.count()


def get_asset_type_names_list() -> list:
    asset_types = AssetType.objects.all()
    return [asset_type.asset_name for asset_type in asset_types]


def get_asset_item_list() -> list:
    assettype_list = get_asset_type_names_list()
    asset_item_list = []
    for asset_name in assettype_list:
        asset_query = Asset.objects.filter(
            asset_type__asset_name=asset_name).aggregate(total_assets=Sum("quantity"))
        all_assets_query = Asset.objects.filter(
            asset_type__asset_name=asset_name).annotate(total=Sum("quantity"))
       
        for asset in all_assets_query:
            assetbrand = asset.asset_brand
            assetname = asset.asset_type.asset_name
            assetquantity = asset.quantity
            specification = f'{asset.system_configuration}'
            assetprice = asset.price
            assetpurchasedate = asset.purchase_date
            asset_item_list.append(
                {
                    "assetname": assetname, "brand": assetbrand, "quantity": assetquantity,
                    "assetprice": assetprice, "assetpurchasedate": assetpurchasedate,
                   
                }
            )
    return asset_item_list


def get_asset_record() -> dict:
    assettype_list = get_asset_type_names_list()
    asset_record = {}
    for asset_name in assettype_list:
        asset_query = Asset.objects.filter(asset_type__asset_name=asset_name).aggregate(
            total_assets=Sum("quantity")
        )
        quantity = asset_query.get("total_assets")
        if quantity:
            asset_record[asset_name] = quantity
    return asset_record


def get_total_asset_quantity() -> int:
    return Asset.objects.all().count()


def get_total_client_asset_quantity() -> int:
    return ClientAsset.objects.all().count()


def get_today_assigned_asset(today_date):
    return AssignAsset.objects.filter(created_at=today_date)


def get_yesterday_assigned_asset(yesterday_date):
    return AssignAsset.objects.filter(created_at=yesterday_date)


def get_total_asset():
    return Asset.objects.all()


def get_employee_id(employee_id):
    emp_id = Employee.objects.filter(employee_id=employee_id).first()
    return emp_id


def get_assign_asset(employee_obj):
    asset_assign = AssignAsset.objects.filter(employee=employee_obj)
    for obj in asset_assign:
        a = obj.asset.quantity+1
        obj.asset.quantity = a
        obj.asset.save()
    asset_assign.delete()


def group_and_sum_asset_counts():
    try:
        asset_typ = Asset.objects.values_list('asset_brand', flat=True).distinct()
        asset_list = []
        for brand_name in asset_typ:
            obj = Asset.objects.filter(asset_brand=brand_name, is_assign=False)
            for data in obj:
                d = {}
                if data.asset_type.asset_name and data.asset_brand in d:
                    d["asset_type"] = data.asset_type.asset_name
                    d["asset_brand"] = data.asset_brand
                    d['count'] += 1
                else:
                    d["asset_type"] = data.asset_type.asset_name
                    d["asset_brand"] = data.asset_brand
                    d['count'] = 1
                asset_list.append(d)
        asset_dict = defaultdict(int)
        for asset in asset_list:
            key = (asset['asset_type'], asset['asset_brand'])
            asset_dict[key] += asset['count']
        output = [{'asset_type': key[0], 'asset_brand': key[1], 'count': asset_dict[key]} for key in asset_dict]
        return output
    except Exception:
        pass


def dashboard_data():
        asset_typ = Asset.objects.all().values_list('asset_brand', flat=True).distinct()
        asset_list = []
        for brand_name in asset_typ:    
            obj = Asset.objects.filter(asset_brand=brand_name)
            for data in obj:
                remaining = 0
                d = {}
                if data.asset_type.asset_name and data.asset_brand in d:
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
        return result        


def vendor_details_info(id):
    asset_typ = Asset.objects.all().filter(vendor=id).values_list('asset_brand', flat=True).distinct()
    asset_list = []
    for brand_name in asset_typ:
        obj = Asset.objects.filter(asset_brand=brand_name, vendor = id)
        for data in obj:
            remaining = 0
            d = {}
            if data.asset_type.asset_name and data.asset_brand in d:
                d["asset_type"] = data.asset_type.asset_name
                d["asset_brand"] = data.asset_brand
                d["asset_price"] += data.price
                d['count'] += 1
            else:
                d["asset_type"] = data.asset_type.asset_name
                d["asset_brand"] = data.asset_brand
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
    return result        








































"""" Get Data According total assets brand for Vendor """
            # asset_list = []
            # for brand_name in asset_typ:
            #     obj = Asset.objects.filter(asset_brand=brand_name, vendor = id)
            #     for data in obj:
            #         remaining = 0
            #         d = {}
            #         if data.asset_type.asset_name and data.asset_brand in d:
            #             d["asset_type"] = data.asset_type.asset_name
            #             d["asset_brand"] = data.asset_brand
            #             d["asset_price"] += data.price
            #             d['count'] += 1
            #         else:
            #             d["asset_type"] = data.asset_type.asset_name
            #             d["asset_brand"] = data.asset_brand
            #             d["asset_price"] = data.price
            #             d['count'] = 1
            #         if data.is_assign:
            #             remaining = 0
            #             d['remaining'] = remaining
            #         else:
            #             remaining += 1 
            #             d['remaining'] = remaining      
            #         asset_list.append(d)

            # result = []
            # for asset in asset_list:
            #     found = False
            #     for res in result:
            #         if res['asset_type'] == asset['asset_type'] and res['asset_brand'] == asset['asset_brand']:
            #             res['count'] += 1
            #             res['asset_price'] += asset['asset_price']
            #             res['remaining'] += asset['remaining']
            #             found = True
            #             break
            #     if not found:
            #         result.append(asset)