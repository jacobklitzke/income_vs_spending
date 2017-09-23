# income_vs_spending

This program calculates the total amount of spending vs. income as a
percentage in a given month based on CSV files from Mint. Additionally, this
program calculates the percentage of spending per category vs. income based on additional Mint CSV files. This program has three required arguments: a CSV file containing a list of expenses and amounts, a CSV file containing a list of food specific expenses and amounts, and a CSV file containing a list of incomes and amounts. All these files can be retrieved from the Trends tab on Mint. Built for Linux, but could be adapted to Windows.

```
usage: budget.py [-h] expense_filepath food_expense_filepath income_filepath

positional arguments:
  expense_filepath      The file path to the Mint CSV file containing all
                        expenses to analyze.
  food_expense_filepath
                        The file path to the Mint CSV file containing all food
                        related expenses to analyze.
  income_filepath       The file path to the Mint CSV file containing all
                        income to analyze.

optional arguments:
  -h, --help            show this help message and exit
```

