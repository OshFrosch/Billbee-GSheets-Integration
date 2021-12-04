import pandas as pd
from scripts.google_sheets import GOOGLE_SHEETS

SPREADSHEET_ID = '1jre8imIUz61QqArOqwYCrRF5JXuKZ1dv-ub1U-SU8uo'

df = pd.DataFrame({'num_legs': [2, 4, 8, 0], 
                   'num_wings': [2, 0, 0, 0],
                   'num_specimen_seen': [10, 2, 1, 8]},
                   index=['falcon', 'dog', 'spider', 'fish'])

GOOGLE_SHEETS.write_pandas_to_sheet(df, SPREADSHEET_ID)