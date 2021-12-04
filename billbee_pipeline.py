import pandas as pd
from scripts.processing import *
from scripts.billbee_api import call_billbee
from scripts.google_sheets import GOOGLE_SHEETS

SPREADSHEET_ID = '1jre8imIUz61QqArOqwYCrRF5JXuKZ1dv-ub1U-SU8uo'

json_data = call_billbee("orders")
data = json_data['Data']

df = pd.DataFrame(data)
df = df.fillna('')

shipping_df = df["ShippingIds"].apply(extract_shipping).apply(pd.Series)
df = pd.concat([shipping_df, df], axis=1)
seller_df = df["Seller"].apply(lambda x: {key: x[key] for key in ['Platform', 'BillbeeShopName', 'BillbeeShopId']}).apply(pd.Series)
df = pd.concat([df, seller_df], axis=1)
customer_df = df["Customer"].apply(lambda x: {"Customer" + key: x[key] for key in ['Id', 'Name', 'Email']}).apply(pd.Series)
df = pd.concat([df, customer_df], axis=1)
product_df = df["OrderItems"].apply(extract_product).apply(pd.Series)
product_df = pd.concat([df["Id"], product_df], axis=1)
product_df = product_df.set_index("Id").apply(pd.Series.explode).reset_index()
df = df.merge(product_df, on='Id', how='inner')

df["InvoiceAddress"] = df["InvoiceAddress"].apply(extract_adress)
df["ShippingAddress"] = df["ShippingAddress"].apply(extract_adress)
df["Tags"] = df["Tags"].apply(lambda tags:", ".join(tags))

drops = ["ShippingIds", "SellerComment", "Comments", "InvoiceAddress", "ShippingAddress", "OrderItems", "ShippingAddress", "OrderItems", "Seller", "Customer", "Payments", "History"]
df = df.drop(columns=drops)

print(df)

GOOGLE_SHEETS.write_pandas_to_sheet(df, SPREADSHEET_ID)