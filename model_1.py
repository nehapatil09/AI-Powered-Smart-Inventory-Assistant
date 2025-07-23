import pandas as pd
from datetime import datetime
import os

# ⚙️ Configuration
INVENTORY_FILE = "real_time_inventory.csv"
TRANSACTIONS_FILE = "transactions.csv"
RESTOCK_THRESHOLD = 20

# 📦 Initial Inventory Setup
inventory = {
    1: {"name": "Milk", "stock": 100},
    2: {"name": "Flour", "stock": 90},
    3: {"name": "Sugar", "stock": 80},
    4: {"name": "Curd", "stock": 70},
    5: {"name": "Bread", "stock": 60},
    6: {"name": "Biscuit", "stock": 50},
    7: {"name": "Cold drinks", "stock": 40},
}

# 📋 Transactions will be recorded here
transactions = []


def show_inventory():
    print("\n📦 Current Inventory:")
    print("-" * 40)
    for pid, item in inventory.items():
        print(f"{pid}. {item['name']} - {item['stock']} in stock")
    print("-" * 40)


def process_transactions():
    # Show today’s date so user enters correct date
    today_str = datetime.now().strftime('%d/%m')
    print(f"\n🧾 Enter sales transactions (type 'done' to finish):")
    print(f"✅ Today’s date is: {today_str}")
    print("➡️ Format: product_ID quantity dd/mm (e.g., 1 5", today_str, ")")
    while True:
        user_input = input("➡️ ").strip()
        if user_input.lower() == "done":
            break
        try:
            pid_str, qty_str, date_str = user_input.split()
            # validate inputs
            pid = int(pid_str)
            qty = int(qty_str)
            datetime.strptime(date_str, "%d/%m")  # validate date
            if pid not in inventory:
                print("❌ Invalid product ID.")
                continue
            if qty <= 0 or inventory[pid]["stock"] < qty:
                print(f"⚠️ Not enough stock for {inventory[pid]['name']}.")
                continue
            inventory[pid]["stock"] -= qty
            print(f"✅ Sold {qty} of {inventory[pid]['name']} on {date_str}")
            transactions.append((pid, qty, date_str))
        except Exception as e:
            print("⚠️ Invalid input. Please enter: ID QUANTITY DATE")


def export_transactions():
    if transactions:
        tx_data = []
        # If file exists, load previous transactions
        if os.path.exists(TRANSACTIONS_FILE):
            prev_df = pd.read_csv(TRANSACTIONS_FILE)
            tx_data = prev_df.to_dict(orient='records')
        # Append current session transactions
        for pid, qty, date_str in transactions:
            tx_data.append({
                "date": date_str,
                "product_id": pid,
                "product_name": inventory[pid]["name"],
                "quantity_sold": qty
            })
        df_tx = pd.DataFrame(tx_data)
        df_tx.to_csv(TRANSACTIONS_FILE, index=False)
        print(f"📁 Transactions saved to '{TRANSACTIONS_FILE}'")
    else:
        print("ℹ️ No transactions recorded this session.")


def export_inventory():
    today_str = datetime.now().strftime('%d/%m')
    sales_rate_map = {pid: 0 for pid in inventory}  # default 0 for all

    # 🔷 If transactions file exists, calculate today’s sales per product
    if os.path.exists(TRANSACTIONS_FILE):
        tx_df = pd.read_csv(TRANSACTIONS_FILE)
        # filter only today’s transactions
        tx_today = tx_df[tx_df['date'] == today_str]
        if not tx_today.empty:
            sales_today = tx_today.groupby('product_id')['quantity_sold'].sum()
            for pid, qty in sales_today.items():
                sales_rate_map[pid] = qty
        else:
            print(f"ℹ️ No sales recorded for today ({today_str}).")

    # 🔷 Save inventory with dynamic sales_rate_today
    data = []
    for pid, item in inventory.items():
        data.append({
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "product_id": pid,
            "product_name": item["name"],
            "stock_level": item["stock"],
            "restock_threshold": RESTOCK_THRESHOLD,
            "sales_rate": sales_rate_map[pid]
        })
    df = pd.DataFrame(data)
    df.to_csv(INVENTORY_FILE, index=False)
    print(f"\n📁 Inventory saved to '{INVENTORY_FILE}'")
    return df


# 🚀 Main program
def main():
    print("🛒 Welcome to the Inventory Billing System")
    show_inventory()
    process_transactions()
    export_transactions()
    export_inventory()


# ▶️ Run
if __name__ == "__main__":
    main()
