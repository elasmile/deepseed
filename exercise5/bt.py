import datetime
import json
import os

# ----------------- Utility Functions ----------------- #
def format_currency(amount):
    return f"${amount:,.2f}"

def validate_date(input_str):
    try:
        return datetime.datetime.strptime(input_str, "%Y-%m")
    except ValueError:
        print("❌ Invalid date format. Use YYYY-MM.")
        return None

def bar_chart(percentage, width=25):
    filled = int(percentage * width)
    return '█' * filled + '░' * (width - filled)

# ----------------- Data Store ----------------- #
DATA_FILE = "budget_data.json"
BUDGET_LIMITS = {
    "food": 400,
    "transport": 300,
    "housing": 800,
    "entertainment": 200
}

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

# ----------------- Core Logic ----------------- #
def add_transaction(data):
    date_str = input("Enter month (YYYY-MM): ").strip()
    dt = validate_date(date_str)
    if not dt:
        return
    month_key = dt.strftime("%Y-%m")

    t_type = input("Type (income/expense): ").strip().lower()
    if t_type not in ["income", "expense", "expenses"]:
        print("❌ Type must be 'income' or 'expense'")
        return

    category = input("Enter category: ").lower()
    try:
        amount = float(input("Enter amount: "))
    except ValueError:
        print("❌ Amount must be a number.")
        return

    if month_key not in data:
        data[month_key] = {"income": {}, "expenses": {}}

    section = "income" if t_type == "income" else "expenses"
    data[month_key][section][category] = data[month_key][section].get(category, 0) + amount
    save_data(data)
    print(f"✅ Added {format_currency(amount)} to {section} → {category}.")

def show_summary(data):
    date_str = input("Enter month (YYYY-MM): ").strip()
    dt = validate_date(date_str)
    if not dt:
        return
    month_key = dt.strftime("%Y-%m")

    if month_key not in data:
        print("No records for this month.")
        return

    income = data[month_key].get("income", {})
    expenses = data[month_key].get("expenses", {})
    total_income = sum(income.values())
    total_expense = sum(expenses.values())
    net = total_income - total_expense
    savings_pct = (net / total_income * 100) if total_income else 0

    print(f"\n=== PERSONAL BUDGET TRACKER ===\nMonth: {dt.strftime('%B %Y')}")
    print("\n💰 FINANCIAL SUMMARY")
    print(f"Total Income:  {format_currency(total_income)}")
    print(f"Total Expenses:{format_currency(total_expense)}")
    print(f"Net Savings:   {format_currency(net)} ({savings_pct:.1f}%)")

    print("\n📊 EXPENSE BREAKDOWN")
    for cat, amt in sorted(expenses.items(), key=lambda x: x[1], reverse=True):
        pct = (amt / total_expense) if total_expense else 0
        print(f"{cat.title():<12} {bar_chart(pct)} {format_currency(amt)} ({pct*100:.1f}%)")

    print("\n⚠️ BUDGET ALERTS:")
    alert_found = False
    for cat, limit in BUDGET_LIMITS.items():
        spent = expenses.get(cat, 0)
        if spent > limit:
            pct = (spent / limit) * 100
            over = spent - limit
            print(f"{cat.title()}: {format_currency(over)} over budget ({pct:.0f}% of limit)")
            alert_found = True
    if not alert_found:
        print("None 🎉")

def analyze_trends(data):
    print("\n📈 SPENDING TREND ANALYSIS")
    months = sorted(data.keys())
    trends = {}

    for cat in BUDGET_LIMITS:
        trends[cat] = []
        for m in months:
            spent = data[m].get("expenses", {}).get(cat, 0)
            trends[cat].append((m, spent))

    for cat, values in trends.items():
        if len(values) < 2:
            continue
        print(f"\nCategory: {cat.title()}")
        for i in range(1, len(values)):
            prev_month, prev_amt = values[i - 1]
            curr_month, curr_amt = values[i]
            change = curr_amt - prev_amt
            direction = "↑" if change > 0 else ("↓" if change < 0 else "→")
            print(f"{prev_month} → {curr_month}: {direction} {format_currency(change)}")

def export_summary(data):
    date_str = input("Enter month (YYYY-MM) to export: ").strip()
    dt = validate_date(date_str)
    if not dt:
        return
    month_key = dt.strftime("%Y-%m")

    if month_key not in data:
        print("No data for this month.")
        return

    filename = f"budget_summary_{month_key}.txt"
    with open(filename, "w") as f:
        f.write(f"BUDGET SUMMARY - {dt.strftime('%B %Y')}\n")
        income = data[month_key].get("income", {})
        expenses = data[month_key].get("expenses", {})
        total_income = sum(income.values())
        total_expense = sum(expenses.values())
        net = total_income - total_expense
        savings_pct = (net / total_income * 100) if total_income else 0

        f.write(f"Total Income:  {format_currency(total_income)}\n")
        f.write(f"Total Expenses:{format_currency(total_expense)}\n")
        f.write(f"Net Savings:   {format_currency(net)} ({savings_pct:.1f}%)\n\n")
        f.write("EXPENSE BREAKDOWN:\n")
        for cat, amt in sorted(expenses.items(), key=lambda x: x[1], reverse=True):
            pct = (amt / total_expense) if total_expense else 0
            f.write(f"- {cat.title()}: {format_currency(amt)} ({pct*100:.1f}%)\n")
    print(f"📄 Summary exported to {filename}")

# ----------------- Main Menu ----------------- #
def main():
    data = load_data()
    while True:
        print("\n=== PERSONAL BUDGET TRACKER ===")
        print("1. Add Income/Expense")
        print("2. Show Monthly Summary")
        print("3. Analyze Spending Trends")
        print("4. Export Summary to File")
        print("5. Exit")
        choice = input("Choose an option: ").strip()
        if choice == '1':
            add_transaction(data)
        elif choice == '2':
            show_summary(data)
        elif choice == '3':
            analyze_trends(data)
        elif choice == '4':
            export_summary(data)
        elif choice == '5':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice.")

if __name__ == "__main__":
    main()
