import csv
import sys
import argparse
import subprocess
from re import sub
from tabulate import tabulate

TRANSACTIONS = {'Restaurants': 0, 'Groceries': 0}

prog_desc = '''This program calculates the total amount of spending vs. income as a percentage in a given month based on 
CSV files from Mint. Additionally, this program calculates the percentage of spending per category vs. income based on additional
Mint CSV files. This program has three required arguments: a CSV file containing a list of expenses and amounts, a CSV file
containing a list of food specific expenses and amounts, and a CSV file containing a list of incomes and amounts. All these files
can be retrieved from the Trends tab on Mint. Built for Linux, but could be adapted to Windows.'''

parser = argparse.ArgumentParser(description=prog_desc)
parser.add_argument('expense_filepath', help='The file path to the Mint CSV file containing all expenses to analyze.')
parser.add_argument('food_expense_filepath', help='The file path to the Mint CSV file containing all food related expenses to analyze.')
parser.add_argument('income_filepath', help='The file path to the Mint CSV file containing all income to analyze.')
args = parser.parse_args()


def food_transaction_type(transaction):
    """
    Gets type of transaction from food expense CSV.
    
    :param transaction: The category name of the transaction. 
    :return: Returns Groceries if the category is groceries, returns retaurants otherwise. 
    """
     
    if transaction == 'Groceries':
        return 'Groceries'
    else:
        return 'Restaurants'
    
def open_csv_file(filepath):
    """
    Opens csv file
    
    :param filepath: full path to the file
    :return: Returns csvreader object
    """
    
    filename = open(filepath, 'r')
    filename.next()
    return csv.reader(filename)

def load_expenses():
    """
    Opens all three CSV files and adds their transactions to the dictionary TRANSACTIONS
    """
    
    csv_file = open_csv_file(args.expense_filepath)
    for row in csv_file:
        if row[0] != 'Food & Dining':
            TRANSACTIONS[row[0]] = float(sub(r'[^\d.]', '', row[1]))
    
    csv_file = open_csv_file(args.food_expense_filepath)
    for row in csv_file:
        if row[0] != 'Total':
            TRANSACTIONS[food_transaction_type(row[0])] += float(sub(r'[^\d.]', '', row[1]))
            
    csv_file = csv.reader(subprocess.check_output(['tail', '-1', args.income_filepath]))
    data = list(csv_file)[2][0]
    TRANSACTIONS['Income'] = float(sub(r'[^\d.]', '', data))
    
def print_income_vs_spending():
    """
    Prints Income vs. Spending table
    """
    
    percent_spent = '{0:.2f}'.format(round((TRANSACTIONS['Total']/TRANSACTIONS['Income'])*100,2))
    income_vs_spending_table = [["Income vs. Spending", "Amount"], ["Spending", TRANSACTIONS['Total']], ["Income", TRANSACTIONS['Income']], ["Percent Spent Income", percent_spent]]
    print tabulate(income_vs_spending_table, tablefmt="grid", headers="firstrow")

def print_spending_table():
    """
    Prints spending table
    """
    
    spending_table = [["Category Spending vs. Income", "Amount", "Percent of Income"]]

    transaction_list = []
    for key, value in TRANSACTIONS.iteritems():
        transaction_list.append([key, value])
        transaction_list.sort(key=lambda x: float(x[1]), reverse=True)

    for item in transaction_list:
        if item[0] != 'Income' and item[0] != 'Total':
            spending_table.append([item[0], item[1], '{0:.2f}'.format(round((item[1]/TRANSACTIONS['Income'])*100, 2))])
    
    print tabulate(spending_table, tablefmt="grid", headers="firstrow")
            
def main():
    load_expenses()
    print_income_vs_spending()
    print_spending_table()          

if __name__ == '__main__':
    main()




