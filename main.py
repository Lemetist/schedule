import gspread
from google.oauth2.service_account import Credentials

scopes = [
    "https://www.googleapis.com/auth/spreadsheets"
]
creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
client = gspread.authorize(creds)

sheet_id = "1A4XPDa6e6VeAxS2rHeO7Yx1ECTjOn8Q7baAaVHLVB-Q"
sheet = client.open_by_key(sheet_id)


def schedule_dataz():
    Monday = sheet.sheet1.get('DV8:DX13')
    Tuesday = sheet.sheet1.get('DV14:DX19')
    Wednesday = sheet.sheet1.get('DV20:DX25')
    Thursday = sheet.sheet1.get('DV26:DX31')
    Friday =  sheet.sheet1.get('DV32:DX37')
    Saturday = sheet.sheet1.get('DV38:DX43')
    return Monday, Tuesday, Wednesday, Thursday, Friday, Saturday

