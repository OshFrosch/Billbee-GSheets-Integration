def extract_shipping(ShippingIds):
    shipping = {
    "ShippingId": "",
    "Shipper": "",
    "TrackingUrl": ""
    }
    for ship in ShippingIds:
        for att in shipping:
            if ship.get(att, None):
                shipping[att] = ship[att]
    return shipping

def extract_adress(adress):
    adr = ""
    for loc in ["FirstName", "LastName", "Street", "HouseNumber", "Zip", "City", "Country"]:
        adr += adress[loc] + " "
    return adr

def extract_product(products):
    product_lists = {k: [] for k in ["Product", "Quantity", "TotalPrice", "ProductWeight", "ProductBillbeeId"]}
    for product in products:
        product_lists["Product"].append(product["Product"]["Title"])
        product_lists["ProductWeight"].append(product["Product"]["Weight"])
        product_lists["ProductBillbeeId"].append(product["Product"]["BillbeeId"])
        product_lists["Quantity"].append(product["Quantity"])
        product_lists["TotalPrice"].append(product["TotalPrice"])
    return product_lists