
import json
import os
from datetime import datetime

FILE_NAME = "expenses.json"

class ExpenseTracker:
    def __init__(self):
        self.expenses = []
        self.load()

    def load(self):
        if os.path.exists(FILE_NAME):
            with open(FILE_NAME, "r") as f:
                try:
                    self.expenses = json.load(f)
                except:
                    self.expenses = []

    def save(self):
        with open(FILE_NAME, "w") as f:
            json.dump(self.expenses, f, indent=4)

    def add(self):
        print("\n--- Add Expense ---")
        date = input("Date (YYYY-MM-DD, blank=today): ").strip()
        if not date:
            date = datetime.today().strftime("%Y-%m-%d")
        category = input("Category: ").strip().title()
        desc = input("Description: ").strip()
        try:
            amount = float(input("Amount: "))
        except ValueError:
            print("Invalid amount.")
            return
        self.expenses.append({
            "date": date,
            "category": category,
            "description": desc,
            "amount": amount
        })
        self.save()
        print("Expense added.")

    def view(self):
        print("\n--- Expenses ---")
        if not self.expenses:
            print("No expenses found.")
            return
        total = 0
        for i,e in enumerate(self.expenses,1):
            print(f"{i}. {e['date']} | {e['category']:<12} | ₹{e['amount']:<8.2f} | {e['description']}")
            total += e["amount"]
        print("-"*60)
        print(f"Total: ₹{total:.2f}")

    def delete(self):
        self.view()
        if not self.expenses:
            return
        try:
            idx = int(input("Expense number to delete: "))
            self.expenses.pop(idx-1)
            self.save()
            print("Deleted.")
        except:
            print("Invalid selection.")

    def edit(self):
        self.view()
        if not self.expenses:
            return
        try:
            idx = int(input("Expense number to edit: ")) - 1
            e = self.expenses[idx]
        except:
            print("Invalid selection.")
            return

        print("Press Enter to keep existing value.")
        d = input(f"Date [{e['date']}]: ").strip() or e["date"]
        c = input(f"Category [{e['category']}]: ").strip().title() or e["category"]
        ds = input(f"Description [{e['description']}]: ").strip() or e["description"]
        a = input(f"Amount [{e['amount']}]: ").strip()
        if a:
            try:
                a = float(a)
            except:
                print("Invalid amount.")
                return
        else:
            a = e["amount"]

        e.update(date=d, category=c, description=ds, amount=a)
        self.save()
        print("Updated.")

    def search(self):
        key = input("Keyword/category: ").lower()
        found = False
        for e in self.expenses:
            if key in e["category"].lower() or key in e["description"].lower():
                print(f"{e['date']} | {e['category']} | ₹{e['amount']:.2f} | {e['description']}")
                found = True
        if not found:
            print("No matching records.")

    def summary(self):
        if not self.expenses:
            print("No expenses.")
            return
        cat = {}
        total = 0
        highest = max(self.expenses, key=lambda x:x["amount"])
        lowest = min(self.expenses, key=lambda x:x["amount"])
        for e in self.expenses:
            cat[e["category"]] = cat.get(e["category"],0)+e["amount"]
            total += e["amount"]
        print("\n--- Summary ---")
        for k,v in cat.items():
            print(f"{k:<15}: ₹{v:.2f}")
        print(f"\nTotal Spending : ₹{total:.2f}")
        print(f"Highest Expense: ₹{highest['amount']:.2f} ({highest['description']})")
        print(f"Lowest Expense : ₹{lowest['amount']:.2f} ({lowest['description']})")

def menu():
    app = ExpenseTracker()
    while True:
        print("""
==========================
      EXPENSE TRACKER
==========================
1. Add Expense
2. View Expenses
3. Edit Expense
4. Delete Expense
5. Search Expense
6. Summary
7. Exit
""")
        ch = input("Choose: ").strip()
        if ch=="1":
            app.add()
        elif ch=="2":
            app.view()
        elif ch=="3":
            app.edit()
        elif ch=="4":
            app.delete()
        elif ch=="5":
            app.search()
        elif ch=="6":
            app.summary()
        elif ch=="7":
            print("Goodbye!")
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    menu()


