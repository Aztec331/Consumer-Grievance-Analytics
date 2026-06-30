# ==========================================================
# Consumer Grievance Analytics System
# Automated PDF Report Generator
#
# Author: Aditya Babar
# ==========================================================

import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# ----------------------------------------------------------
# Create reports folder if it doesn't exist
# ----------------------------------------------------------
os.makedirs("reports", exist_ok=True)

# ----------------------------------------------------------
# Load cleaned dataset
# ----------------------------------------------------------
data_path = "data/cleaned_consumer_grievances.csv"
df = pd.read_csv(data_path)

print("=" * 60)
print("DATASET LOADED SUCCESSFULLY")
print("=" * 60)
print(f"Rows    : {df.shape[0]}")
print(f"Columns : {df.shape[1]}")

# ----------------------------------------------------------
# Create PDF Report
# ----------------------------------------------------------
pdf_path = "reports/complaint_analysis_report.pdf"

with PdfPages(pdf_path) as pdf:

    # ======================================================
    # PAGE 1 - Top Complaint Categories
    # ======================================================

    category_counts = df["Complaint Category"].value_counts()

    plt.figure(figsize=(10, 6))

    category_counts.plot(
        kind="bar",
        color="steelblue",
        edgecolor="black"
    )

    plt.title("Top Complaint Categories", fontsize=16, fontweight="bold")
    plt.xlabel("Complaint Category")
    plt.ylabel("Number of Complaints")
    plt.xticks(rotation=45)

    for i, value in enumerate(category_counts):
        plt.text(i, value + 2, str(value), ha="center")

    plt.grid(axis="y", linestyle="--", alpha=0.4)

    plt.tight_layout()
    pdf.savefig()
    plt.close()

    # ======================================================
    # PAGE 2 - Monthly Complaint Trend
    # ======================================================

    monthly = (
        df.groupby("Month_Year")
        .size()
        .reset_index(name="Complaint Count")
    )

    monthly["Rolling Average"] = (
        monthly["Complaint Count"]
        .rolling(3)
        .mean()
    )

    plt.figure(figsize=(10, 6))

    plt.plot(
        monthly["Month_Year"],
        monthly["Complaint Count"],
        marker="o",
        linewidth=2,
        label="Monthly Complaints"
    )

    plt.plot(
        monthly["Month_Year"],
        monthly["Rolling Average"],
        marker="s",
        linestyle="--",
        linewidth=2,
        label="3-Month Rolling Average"
    )

    plt.title("Monthly Complaint Volume Trend", fontsize=16, fontweight="bold")
    plt.xlabel("Month-Year")
    plt.ylabel("Number of Complaints")
    plt.xticks(rotation=45)
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.legend()

    plt.tight_layout()
    pdf.savefig()
    plt.close()

    # ======================================================
    # PAGE 3 - Resolution Status Distribution
    # ======================================================

    status_counts = df["Status"].value_counts()

    plt.figure(figsize=(8, 8))

    plt.pie(
        status_counts,
        labels=status_counts.index,
        autopct="%1.1f%%",
        startangle=90,
        explode=(0.05, 0),
        shadow=True
    )

    plt.title(
        "Resolution Status Distribution",
        fontsize=16,
        fontweight="bold"
    )

    plt.axis("equal")

    pdf.savefig()
    plt.close()

    # ======================================================
    # PAGE 4 - Key Policy Insights
    # ======================================================

    total = len(df)
    resolved = (df["Status"] == "Resolved").sum()
    resolution_rate = (resolved / total) * 100
    avg_days = df["Resolution Time (Days)"].mean()
    top_category = df["Complaint Category"].value_counts().idxmax()
    busiest_month = monthly.loc[
        monthly["Complaint Count"].idxmax(),
        "Month_Year"
    ]

    fig = plt.figure(figsize=(8.27, 11.69))
    plt.axis("off")

    plt.text(
        0.5,
        0.95,
        "Key Policy Insights",
        fontsize=22,
        fontweight="bold",
        ha="center"
    )

    insights = [
        f"• Total Complaints: {total}",
        f"• Resolved Complaints: {resolved}",
        f"• Resolution Rate: {resolution_rate:.1f}%",
        f"• Average Resolution Time: {avg_days:.2f} days",
        f"• Most Common Complaint Category: {top_category}",
        f"• Month with Highest Complaints: {busiest_month}"
    ]

    y = 0.82

    for item in insights:
        plt.text(
            0.08,
            y,
            item,
            fontsize=15
        )
        y -= 0.09

    plt.text(
        0.08,
        0.15,
        "Generated Automatically using Python & Matplotlib",
        fontsize=11,
        style="italic"
    )

    pdf.savefig(fig)
    plt.close(fig)

print("=" * 60)
print("REPORT GENERATED SUCCESSFULLY")
print("=" * 60)
print(f"Saved to: {pdf_path}")