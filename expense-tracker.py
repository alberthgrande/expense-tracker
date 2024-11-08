import argparse
import json
import os
import csv
import pandas as pd
from datetime import datetime

EXPENSES_FILE = "expenses.json"


def load_expenses():
    """Load expenses from JSON file."""
    if os.path.exists(EXPENSES_FILE):
        with open(EXPENSES_FILE, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    return []


def save_expenses(expenses):
    """Save expenses to the JSON file."""
    with open(EXPENSES_FILE, "w") as file:
        json.dump(expenses, file, indent=4)
        print(f"Expenses saved: {expenses}")


def add_expenses(description, amount, category=None):
    """Add and expenses"""
    expenses = load_expenses()
    expense_id = len(expenses) + 1  # Generate new ID
    expense = {
        "id": expense_id,
        "description": description,
        "amount": amount,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "category": category,
    }
    expenses.append(expense)
    save_expenses(expenses)
    print(f"Expense added successfully (ID: {expense_id})")


def list_expenses():
    """List all expenses."""
    expenses = load_expenses()
    # Load data into a DataFrame
    df = pd.DataFrame(expenses)
    print("\n", df.to_string(index=False))


# print("ID   Date       Description   Amount   Category")
# for expense in expenses:
#     print(
#         f"{expense['id']}   {expense['date']}   {expense['description']}   ${expense['amount']:.2f}   {expense.get('category', 'N/A')}"
#     )


def delete_expenses(expenses_id):
    """Delete an expense by its ID."""
    expenses = load_expenses()
    expense = next((exp for exp in expenses if exp["id"] == expenses_id), None)

    if expense:
        expenses.remove(expense)
        save_expenses(expenses)
        print(f"Expense deleted successfully")
    else:
        print(f"Error: Expense with ID {expenses_id} not found")


def summary_expenses(month=None):
    """Show a summary of expenses."""
    expenses = load_expenses()
    if month:
        expenses = [
            expens
            for expens in expenses
            if datetime.strptime(expens["date"], "%Y-%m-%d").month == month
        ]
    total = sum(expens["amount"] for expens in expenses)

    if month:
        print(f"Total expenses for month {month}: ${total:.2f}")
    else:
        print(f"Total expenses: ${total:.2f}")


def export_csv_expenses():
    """Export expenses to a CSV file."""
    expenses = load_expenses()
    with open("expenses.csv", "w", newline="") as file:
        writer = csv.DictWriter(
            file, fieldnames=["id", "description", "amount", "date", "category"]
        )
        writer.writeheader()
        writer.writerows(expenses)
    print("Expenses exported to expenses.csv")


def main():
    parser = argparse.ArgumentParser(description="Expense Tracker")

    subparsers = parser.add_subparsers(dest="command")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new expense")
    add_parser.add_argument(
        "--description", required=True, help="Description of the expense"
    )
    add_parser.add_argument("--amount", type=float, help="Amount of the expense")
    add_parser.add_argument("--category", help="Category of expense")

    # List command
    list_parser = subparsers.add_parser("list", help="List all expenses")

    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete an expense")
    delete_parser.add_argument(
        "--id", type=int, required=True, help="ID of the expense to delete"
    )

    # Summary command
    summary_parser = subparsers.add_parser("summary", help="View summary of expense")
    summary_parser.add_argument(
        "--month", type=int, help="View summary for a specific month (1-12)"
    )

    # Export command
    export_parser = subparsers.add_parser(
        "export", help="Export expenses to a CSV file"
    )

    args = parser.parse_args()

    if args.command == "add":
        add_expenses(args.description, args.amount, args.category)
    elif args.command == "list":
        list_expenses()
    elif args.command == "delete":
        delete_expenses(args.id)
    elif args.command == "summary":
        summary_expenses(args.month)
    elif args.command == "export":
        export_csv_expenses()
    else:
        print("Command not found")


if __name__ == "__main__":
    main()
