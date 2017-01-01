import csv
import re
from pylab import *
from collections import namedtuple
from locations import Locations


class FinanceManager:

    CategoryTotal = namedtuple('CategoryTotal', 'category total')

    figure(1, figsize=(6, 6))
    ax = axes([0.1, 0.1, 0.8, 0.8])

    def __init__(self):
        self.matt_lunches_total = 0
        self.gas_total = 0
        self.locations = Locations.locations
        self.csv_path = None

    @staticmethod
    def parse_csv_row(row_data):
        return {
            'date': row_data[0],
            'trans_type': row_data[1],
            'name': row_data[2],
            'memo': row_data[3],
            'amount': re.sub('[-]', '', row_data[4])  # Remove the negative since we just want the absolute value of the transaction
        }

    @staticmethod
    def calc_amount_by_locations(locations, values):

        for location in locations['location']:
            for name in location['names']:
                if name.upper() in values['name']:
                    date = values['date'].split("/")
                    # print("FOUND \"%s\" in %s: %s @ %s" % (name.upper(), values['name'], values['amount'], date))
                    location['amount'] += float(values['amount'])
                    return
        if values['name'].upper() != 'NAME':
            print ("NOT FOUND %s: $%s" % (values['name'].upper(), values['amount']))
            max_idx = len(locations['location'])-1
            locations['location'][max_idx]['amount'] += float(values['amount'])

        return

    @staticmethod
    def plot_bar_graph(n_categories, totals, budgets, category_titles):

        overspend = []
        underspend = []

        for idx in range(0, len(totals)):
            difference = totals[idx] - budgets[idx]
            if difference > 0:
                overspend.append(difference)
                underspend.append(0)
            else:
                overspend.append(0)
                underspend.append(budgets[idx] + difference)

        n = n_categories
        ind = np.arange(n)  # the x locations for the groups
        width = 0.35  # the width of the bars: can also be len(x) sequence

        p1 = plt.bar(ind, budgets, width, color='y')
        p2 = plt.bar(ind, overspend, width, color='r', bottom=budgets)
        p3 = plt.bar(ind, underspend, width, color='g')

        plt.ylabel('Dollars ($)')
        plt.xticks(ind + width / 2., category_titles)
        plt.yticks(np.arange(0, 600, 25))
        plt.legend((p1[0], p2[0], p3[0]), ('Budget', 'Overspent', 'Underspent'))

        plt.show()

    def calc_finances(self):
        with open(self.csv_path, 'r') as expenses:
            reader = csv.reader(expenses)
            value = 0
            for row in reader:

                # Break up the data according to how it's laid out in the CSV
                row_values = self.parse_csv_row(row)

                # Calculate the totals based on individual lists
                FinanceManager.calc_amount_by_locations(Locations.locations, row_values)

            labels = []
            fracs = []
            budget = []
            # Print out the totals for each list
            for location in Locations.locations['location']:
                value += location['amount']
                labels.append(location['category'])
                fracs.append(location['amount'])
                budget.append(location['budget'])
                print("%s: $%.02f" % (location['category'], location['amount']))
            pie(fracs, autopct='%1.1f%%', labels=labels, shadow=True, startangle=90)
            show()
            self.plot_bar_graph(len(fracs), fracs, budget, labels)
            print("Overall Total: $%.02f" % value)
