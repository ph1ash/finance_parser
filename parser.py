from finance_parser import FinanceManager
from locations import Locations

fb = FinanceManager()
fb.csv_path = '/home/phlash/Downloads/export (3).csv'
fb.calc_finances()
# print Locations.locations['location'][0]['names']


