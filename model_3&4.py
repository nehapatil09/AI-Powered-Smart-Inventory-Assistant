import pandas as pd
import joblib
import smtplib
from email.mime.text import MIMEText
import os

# --- Email Configuration ---
SENDER_EMAIL = "nehasunilpatil08@gmail.com"
SENDER_PASSWORD = "dsgkgcrnrhatgmwl"
RECEIVER_EMAIL = "mihirvachhani2004@gmail.com"  # Replace with your email

def send_email_alert(message):
    subject = "📦 Inventory Restock Alert"
    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        print("\n📧 Email alert sent successfully!")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

# --- Load Model & Data ---
MODEL_FILE = "inventory_model.pkl"
INVENTORY_FILE = "real_time_inventory.csv"

if not os.path.exists(MODEL_FILE):
    print(f"❌ Model file '{MODEL_FILE}' not found. Run training first.")
    exit()

if not os.path.exists(INVENTORY_FILE):
    print(f"❌ Inventory file '{INVENTORY_FILE}' not found. Run billing system first.")
    exit()

model = joblib.load(MODEL_FILE)
df = pd.read_csv(INVENTORY_FILE)

# 🧹 Keep only known items
df = df[df["product_id"].isin([1, 2, 3, 4, 5, 6, 7])].copy()

# --- Prepare Features & Predict ---
required_cols = ["stock_level", "sales_rate", "restock_threshold"]
for col in required_cols:
    if col not in df.columns:
        print(f"❌ Missing column '{col}' in inventory file.")
        exit()

features = df[required_cols]
df["restock_pred"] = model.predict(features)

# --- Print Report & Prepare Email Body ---
print("\n🔍 Restock Prediction Report:\n")
email_body = ""
for _, row in df.iterrows():
    if row["restock_pred"]:
        status = "❗ YES - Restock Needed"
        email_body += f"{row['product_name']} (Stock: {row['stock_level']}) needs restocking.\n"
    else:
        status = "✅ NO - Stock OK"
    print(f"{row['product_name']} (Stock: {row['stock_level']}) → {status}")

# --- Send Email if Restock Needed ---
if email_body:
    email_body = "The following items require restocking:\n\n" + email_body
    send_email_alert(email_body)
else:
    print("\n✅ No items need restocking. No email sent.")