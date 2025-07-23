import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

# 📄 Check inventory file
INVENTORY_FILE = "real_time_inventory.csv"

if not os.path.exists(INVENTORY_FILE):
    raise FileNotFoundError(f"❌ Inventory file '{INVENTORY_FILE}' not found. Run the inventory system first.")

# 📦 Load inventory data
df = pd.read_csv(INVENTORY_FILE)

# 🚨 Define target: whether restock is needed
df["restock_needed"] = df["stock_level"] < df["restock_threshold"]

# 🧹 Handle missing or zero sales_rate (optional: assume 0 if missing)
if "sales_rate" not in df.columns:
    raise ValueError("❌ Column 'sales_rate' not found in inventory file.")
df["sales_rate"] = df["sales_rate"].fillna(0)

# 🎯 Features and labels
X = df[["stock_level", "sales_rate", "restock_threshold"]]
y = df["restock_needed"]

# 🤖 Model training
model = RandomForestClassifier(random_state=42)
model.fit(X, y)

# 💾 Save the model
joblib.dump(model, "inventory_model.pkl")
print("✅ Model trained and saved as inventory_model.pkl")