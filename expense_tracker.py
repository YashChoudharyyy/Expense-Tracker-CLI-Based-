import time 
import datetime
import calendar
from expenses import Expense


def main():
    print(f"Loading Expense Tracker!")
    expenses_file = "expenses.csv"
    budget = 5000
    
    while True:
        print("Hello User, what would you like me to do for you?\n1. Add an Expense!\n2. Check Remaining budget\n3. Exit!")
        user_input = int(input("Enter your choice : "))
        
        if user_input not in range (4) or user_input == 0:
            print("invalid input, Please Retry")
            input("Enter to continue...")
            continue
        if user_input == 1:
            expense = get_user_expense_input() # Get user input for various expenses
            write_expense_into_file(expense, expenses_file) # Write the expenses in the file
        elif user_input == 2:
            summarize_expenses(expenses_file, budget) # summarizes the expenses in the file by category 
        elif user_input == 3:
            break

def get_user_expense_input():
    print(f"Getting User Expense!")
    expense_name = input(f"Please enter the expense name : ")
    expense_amount = float(input(f"Please enter the expense amount : "))
    
    expense_categories = [
        "Food",
        "Health & Hygiene",
        "Academic",
        "Travel",
        "Miscellaneous"
    ]
    
    while True:
        print("Please select the category of the expense : ")
        for i, category_name in enumerate(expense_categories):
            print(f"{i+1}.{category_name}")
            
        value_range = f"[ 1 - {len(expense_categories)} ]"
        user_input_category = int(input(f"Choose the cateogory {value_range} : ")) - 1
                    
        if i in range(len(expense_categories)):
            selected_category = expense_categories[user_input_category]
            new_expense = Expense(
                category=selected_category,
                name=expense_name,
                amount=expense_amount,
            )
            return new_expense
        else:
            print("The category you've entered is invalid, you stupid monkey!")
            input("Enter to continue...")
            continue
              
        break
    
def write_expense_into_file(expense: Expense, expenses_file):
    print(f"Saving User Expense : {expense} !")
    with open(expenses_file, "a") as f:
        f.write (f"{expense.name} , {expense.amount} , {expense.category}\n")
    
def summarize_expenses(expenses_file, budget):
    print(f"Summarizing User Expense!")
    expenses: list[Expense] = []
    with open(expenses_file, "r") as f:
        lines = f.readlines()
        for line in lines:
            expense_name, expense_amount, expense_category = line.strip().split(",")
            cleaned_amount = expense_amount.strip().replace("Rs", "").strip()
            line_expense = Expense(
                name=expense_name,
                amount=float(cleaned_amount),
                category=expense_category
            )
            expenses.append(line_expense)

    amount_by_category = {}
    for expense in expenses:
        key = expense.category
        if key in amount_by_category:
            amount_by_category[key] += expense.amount
        else:
            amount_by_category[key] = expense.amount
            
    print("Expenses by category :")
    for key, amount in amount_by_category.items():
        print(f"{key} : {amount:.2f}Rs")
        
    total_spent = sum([x.amount for x in expenses])
    print(f"Total Budget Spent: {total_spent:.2f}Rs")
    
    remaining_budget = budget - total_spent
    print(f"Budget Remaining: {remaining_budget:.2f}Rs")
    
    now = datetime.datetime.now()
    days_in_month = calendar.monthrange(now.year, now.month)[1]
    remaining_days = days_in_month - now.day
    print(f"Remaining days in the current month : {remaining_days}")
    
    daily_budget = remaining_budget / remaining_days
    print(green(f"Recommended budget per day : {daily_budget:.2f}Rs"))
    input("Enter to continue...")
    
def green(text):
    return f"\033[92m{text}\033[0m"

if __name__ == "__main__":
    main()