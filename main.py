import pandas as pd
import matplotlib.pyplot as plt
f = input("Enter the file name: ")
def analyze_sales(file_path):
    # Load CSV
    df = pd.read_csv(file_path)

    # --- BASIC SUMMARY ---
    summary = {
        "Total Orders": df["Order ID"].nunique(),
        "Total Items Sold": df["Item Quantity"].sum(),
        "Total Revenue (Invoice Amount)": df["Final Invoice Amount (Price after discount+Shipping Charges)"].sum(),
        "Total Discount Given": df["Total Discount"].sum(),
        "Total Tax Collected": df["IGST Amount"].sum() + df["CGST Amount"].sum() + df["SGST Amount (Or UTGST as applicable)"].sum(),
        "Total TCS Deducted": df["Total TCS Deducted"].sum(),
        "Total TDS Deducted": df["TDS Amount"].sum(),
        "States Covered": df["Customer's Delivery State"].nunique(),
        "Top State by Orders": df["Customer's Delivery State"].value_counts().idxmax(),
        "Most Sold Product": df["Product Title/Description"].value_counts().idxmax()
    }

    print("\n--- SALES SUMMARY ---")
    for k, v in summary.items():
        print(f"{k}: {v}")

    # --- RETURNS ANALYSIS ---
    returns = df[df["Event Type"] == "Return"]
    if not returns.empty:
        returns_summary = {
            "Total Returns": len(returns),
            "Returned Items": returns["Item Quantity"].sum(),
            "Return Rate (%)": round((len(returns) / len(df)) * 100, 2),
            "Return Value (Invoice Amount)": returns["Final Invoice Amount (Price after discount+Shipping Charges)"].sum(),
            "Top State by Returns": returns["Customer's Delivery State"].value_counts().idxmax(),
            "Most Returned Product": returns["Product Title/Description"].value_counts().idxmax()
        }

        print("\n--- RETURNS SUMMARY ---")
        for k, v in returns_summary.items():
            print(f"{k}: {v}")
    else:
        print("\nNo returns found in this dataset.")

    # --- CHARTS ---
    # Orders by state
    orders_by_state = df["Customer's Delivery State"].value_counts()
    orders_by_state.plot(kind="bar", figsize=(8,6), title="Orders by State")
    plt.xlabel("State")
    plt.ylabel("Orders")
    plt.tight_layout()
    plt.show()

    # Revenue trend by date
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    revenue_by_date = df.groupby("Order Date")["Final Invoice Amount (Price after discount+Shipping Charges)"].sum()
    revenue_by_date.plot(marker="o", figsize=(8,6), title="Revenue Trend by Date")
    plt.xlabel("Date")
    plt.ylabel("Revenue (₹)")
    plt.tight_layout()
    plt.show()

    # Top 5 products by quantity sold
    top_products = df.groupby("Product Title/Description")["Item Quantity"].sum().sort_values(ascending=False).head(5)
    top_products.plot(kind="barh", figsize=(8,6), title="Top 5 Products by Quantity Sold")
    plt.xlabel("Quantity Sold")
    plt.ylabel("Product")
    plt.tight_layout()
    plt.show()

# Run the analysis (change file path as needed)
if __name__ == "__main__":
    analyze_sales(f)