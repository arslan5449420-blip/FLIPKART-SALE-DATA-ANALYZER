import pandas as pd
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
import os

f = input("Enter the file name (with .csv): ")

def generate_pdf_report(summary_text, chart_paths, output_filename="sales_report.pdf"):
    """Generate a PDF with summary text and chart images."""
    doc = SimpleDocTemplate(output_filename, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("<b>Flipkart Sales Data Report</b>", styles["Title"]))
    story.append(Spacer(1, 12))
    story.append(Paragraph(summary_text.replace("\n", "<br/>"), styles["Normal"]))
    story.append(Spacer(1, 12))

    for path in chart_paths:
        if os.path.exists(path):
            story.append(Image(path, width=400, height=250))
            story.append(Spacer(1, 12))

    doc.build(story)
    print(f"\n✅ PDF report saved as: {output_filename}")


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

    summary_text = "\n--- SALES SUMMARY ---\n"
    for k, v in summary.items():
        summary_text += f"{k}: {v}\n"

    print(summary_text)

    # --- RETURNS ANALYSIS ---
    returns_summary = ""
    returns = df[df["Event Type"] == "Return"]
    if not returns.empty:
        returns_summary += "\n--- RETURNS SUMMARY ---\n"
        r_summary = {
            "Total Returns": len(returns),
            "Returned Items": returns["Item Quantity"].sum(),
            "Return Rate (%)": round((len(returns) / len(df)) * 100, 2),
            "Return Value (Invoice Amount)": returns["Final Invoice Amount (Price after discount+Shipping Charges)"].sum(),
            "Top State by Returns": returns["Customer's Delivery State"].value_counts().idxmax(),
            "Most Returned Product": returns["Product Title/Description"].value_counts().idxmax()
        }
        for k, v in r_summary.items():
            returns_summary += f"{k}: {v}\n"
        print(returns_summary)
    else:
        returns_summary = "\nNo returns found in this dataset."
        print(returns_summary)

    # --- CHARTS ---
    chart_paths = []

    # Orders by state
    orders_by_state = df["Customer's Delivery State"].value_counts()
    plt.figure(figsize=(8,6))
    orders_by_state.plot(kind="bar", title="Orders by State")
    plt.xlabel("State")
    plt.ylabel("Orders")
    plt.tight_layout()
    chart1_path = "orders_by_state.png"
    plt.savefig(chart1_path)
    chart_paths.append(chart1_path)
    plt.close()

    # Revenue trend by date
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    revenue_by_date = df.groupby("Order Date")["Final Invoice Amount (Price after discount+Shipping Charges)"].sum()
    plt.figure(figsize=(8,6))
    revenue_by_date.plot(marker="o", title="Revenue Trend by Date")
    plt.xlabel("Date")
    plt.ylabel("Revenue (₹)")
    plt.tight_layout()
    chart2_path = "revenue_trend.png"
    plt.savefig(chart2_path)
    chart_paths.append(chart2_path)
    plt.close()

    # Top 5 products
    top_products = df.groupby("Product Title/Description")["Item Quantity"].sum().sort_values(ascending=False).head(5)
    plt.figure(figsize=(8,6))
    top_products.plot(kind="barh", title="Top 5 Products by Quantity Sold")
    plt.xlabel("Quantity Sold")
    plt.ylabel("Product")
    plt.tight_layout()
    chart3_path = "top_products.png"
    plt.savefig(chart3_path)
    chart_paths.append(chart3_path)
    plt.close()

    # Combine summaries for PDF
    full_summary_text = summary_text + "\n" + returns_summary

    # Generate PDF
    generate_pdf_report(full_summary_text, chart_paths)


# Run the analysis
if __name__ == "__main__":
    analyze_sales(f)