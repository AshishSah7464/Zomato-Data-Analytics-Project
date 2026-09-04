"""
===============================================================================
ZOMATO RESTAURANT DATA ANALYSIS
Complete Automated Project Report Generator

Outputs:
    reports/Zomato_Analysis_Report.pdf
    reports/Zomato_Analysis_Report.md

The script:
    1. Loads raw/cleaned Zomato data
    2. Cleans and preprocesses the dataset
    3. Calculates project KPIs
    4. Performs EDA
    5. Generates charts
    6. Performs business analysis
    7. Reads SQL files if available
    8. Detects Power BI dashboard screenshots
    9. Generates complete PDF report
   10. Generates Markdown report
===============================================================================
"""

import os
import re
import shutil
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
    PageBreak,
    HRFlowable,
    KeepTogether
)
from reportlab.pdfgen import canvas


# =============================================================================
# 1. PAGE NUMBER CANVAS
# =============================================================================

class NumberedCanvas(canvas.Canvas):

    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        page_count = len(self._saved_page_states)

        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(page_count)
            canvas.Canvas.showPage(self)

        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):

        self.saveState()

        # Header
        if self._pageNumber > 1:
            self.setStrokeColor(colors.HexColor("#D1D5DB"))
            self.line(40, 805, 555, 805)

            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#6B7280"))

            self.drawString(
                40,
                812,
                "Zomato Restaurant Data Analysis"
            )

        # Footer
        self.setStrokeColor(colors.HexColor("#D1D5DB"))
        self.line(40, 40, 555, 40)

        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#6B7280"))

        self.drawString(
            40,
            27,
            "Data Analytics Project"
        )

        self.drawRightString(
            555,
            27,
            f"Page {self._pageNumber} of {page_count}"
        )

        self.restoreState()


# =============================================================================
# 2. PROJECT PATHS
# =============================================================================

def get_project_paths():

    script_dir = os.path.dirname(os.path.abspath(__file__))

    project_root = os.path.abspath(
        os.path.join(script_dir, "..")
    )

    paths = {

        "project_root": project_root,

        "raw_data":
            os.path.join(
                project_root,
                "data",
                "raw",
                "Zomato.csv"
            ),

        "processed_data":
            os.path.join(
                project_root,
                "data",
                "clean",
                "Zomato_cleaned.csv"
            ),

        "old_clean_data":
            os.path.join(
                project_root,
                "data",
                "clean",
                "Zomato_cleaned.csv"
            ),

        "visualization":
            os.path.join(
                project_root,
                "visualization"
            ),

        "sql":
            os.path.join(
                project_root,
                "sql"
            ),

        "powerbi":
            os.path.join(
                project_root,
                "powerbi"
            ),

        "reports":
            os.path.join(
                project_root,
                "reports"
            )
    }

    os.makedirs(paths["reports"], exist_ok=True)
    os.makedirs(paths["visualization"], exist_ok=True)

    return paths


# =============================================================================
# 3. LOAD DATA
# =============================================================================

def load_data(paths):

    raw_df = None
    cleaned_df = None

    if os.path.exists(paths["raw_data"]):
        raw_df = pd.read_csv(paths["raw_data"])
        print(f"Raw dataset loaded: {paths['raw_data']}")

    if os.path.exists(paths["processed_data"]):
        cleaned_df = pd.read_csv(paths["processed_data"])
        print(f"Processed dataset loaded: {paths['processed_data']}")
    elif os.path.exists(paths["old_clean_data"]):
        cleaned_df = pd.read_csv(paths["old_clean_data"])
        print(f"Clean dataset loaded: {paths['old_clean_data']}")
    elif raw_df is not None:
        cleaned_df = raw_df.copy()
    else:
        raise FileNotFoundError(
            "Zomato dataset not found.\nExpected: data/raw/Zomato.csv"
        )

    return raw_df, cleaned_df


# =============================================================================
# 4. DATA CLEANING
# =============================================================================

def clean_data(df):

    df = df.copy()
    original_rows = len(df)

    df.columns = df.columns.str.strip().str.lower()

    rename_map = {
        "approx_cost(for two people)": "approx_cost",
        "listed_in(type)": "restaurant_type"
    }

    df = df.rename(columns=rename_map)

    duplicate_rows = df.duplicated().sum()
    df = df.drop_duplicates(keep="first")

    if "rate" in df.columns:
        df["rate"] = (
            df["rate"]
            .astype(str)
            .str.replace("/5", "", regex=False)
            .str.strip()
        )
        df["rate"] = pd.to_numeric(df["rate"], errors="coerce")

    if "votes" in df.columns:
        df["votes"] = pd.to_numeric(df["votes"], errors="coerce")

    if "approx_cost" in df.columns:
        df["approx_cost"] = (
            df["approx_cost"]
            .astype(str)
            .str.replace(",", "", regex=False)
            .str.strip()
        )
        df["approx_cost"] = pd.to_numeric(df["approx_cost"], errors="coerce")

    categorical_columns = ["online_order", "book_table", "restaurant_type"]
    for column in categorical_columns:
        if column in df.columns:
            df[column] = df[column].astype(str).str.strip()

    if "restaurant_type" in df.columns:
        df["restaurant_type"] = df["restaurant_type"].str.title()

    missing_before = df.isnull().sum()

    required_columns = ["rate", "votes", "approx_cost", "restaurant_type"]
    existing_required = [col for col in required_columns if col in df.columns]

    df = df.dropna(subset=existing_required)

    rows_removed_missing = max(0, len(df) - original_rows + duplicate_rows)

    cleaning_stats = {
        "original_rows": original_rows,
        "duplicate_rows": int(duplicate_rows),
        "rows_after_duplicates": int(original_rows - duplicate_rows),
        "rows_after_cleaning": len(df),
        "missing_values_before": int(missing_before.sum()),
        "rows_removed_missing": int(rows_removed_missing)
    }

    return df, cleaning_stats


# =============================================================================
# 5. CALCULATE METRICS
# =============================================================================

def calculate_metrics(df, cleaning_stats, raw_df):

    metrics = {}

    metrics["raw_rows"] = len(raw_df) if raw_df is not None else cleaning_stats["original_rows"]
    metrics["clean_rows"] = len(df)
    metrics["columns"] = len(df.columns)
    metrics["column_names"] = list(df.columns)
    metrics["duplicate_rows"] = cleaning_stats["duplicate_rows"]
    metrics["missing_values"] = cleaning_stats["missing_values_before"]

    metrics["total_restaurants"] = len(df)
    metrics["avg_rating"] = round(df["rate"].mean(), 2)
    metrics["total_votes"] = int(df["votes"].sum())
    metrics["avg_cost"] = int(round(df["approx_cost"].mean()))
    metrics["median_cost"] = int(round(df["approx_cost"].median()))
    metrics["median_rating"] = round(df["rate"].median(), 2)

    metrics["type_counts"] = df["restaurant_type"].value_counts()
    metrics["type_shares"] = (metrics["type_counts"] / len(df) * 100).round(1)

    metrics["online_rating"] = df.groupby("online_order")["rate"].mean().round(2)
    metrics["online_count"] = df["online_order"].value_counts()

    metrics["booking_rating"] = df.groupby("book_table")["rate"].mean().round(2)
    metrics["booking_count"] = df["book_table"].value_counts()

    metrics["cost_rating_corr"] = round(df["approx_cost"].corr(df["rate"]), 2)
    metrics["votes_rating_corr"] = round(df["votes"].corr(df["rate"]), 2)

    metrics["category_rating"] = (
        df.groupby("restaurant_type")["rate"]
        .agg(["mean", "count"])
        .sort_values("mean", ascending=False)
    )
    metrics["category_rating"]["mean"] = metrics["category_rating"]["mean"].round(2)

    metrics["category_cost"] = (
        df.groupby("restaurant_type")["approx_cost"]
        .mean()
        .round()
        .astype(int)
        .sort_values()
    )

    if "name" in df.columns:
        metrics["top_voted"] = (
            df.sort_values("votes", ascending=False)
            [["name", "rate", "votes", "approx_cost"]]
            .head(10)
        )
    else:
        metrics["top_voted"] = pd.DataFrame()

    metrics["high_rated"] = (
        df[df["rate"] >= 4.5]
        .sort_values("votes", ascending=False)
        .head(10)
    )

    return metrics


# =============================================================================
# 6. GENERATE EDA CHARTS
# =============================================================================

def generate_charts(df, viz_dir):

    os.makedirs(viz_dir, exist_ok=True)
    sns.set_theme(style="whitegrid")

    chart_paths = {}

    # 1. Restaurant type
    path = os.path.join(viz_dir, "restaurant_type_count.png")
    plt.figure(figsize=(8, 5))
    counts = df["restaurant_type"].value_counts()
    ax = counts.plot(kind="bar")
    plt.title("Restaurant Distribution by Type")
    plt.xlabel("Restaurant Type")
    plt.ylabel("Number of Restaurants")
    plt.xticks(rotation=0)
    for container in ax.containers:
        ax.bar_label(container)
    plt.tight_layout()
    plt.savefig(path, dpi=200)
    plt.close()
    chart_paths["type"] = path

    # 2. Rating distribution
    path = os.path.join(viz_dir, "rating_distribution.png")
    plt.figure(figsize=(8, 5))
    plt.hist(df["rate"], bins=15)
    plt.title("Restaurant Rating Distribution")
    plt.xlabel("Rating")
    plt.ylabel("Number of Restaurants")
    plt.tight_layout()
    plt.savefig(path, dpi=200)
    plt.close()
    chart_paths["rating"] = path

    # 3. Online ordering
    path = os.path.join(viz_dir, "online_ordering.png")
    online_avg = df.groupby("online_order")["rate"].mean()
    plt.figure(figsize=(7, 5))
    online_avg.plot(kind="bar")
    plt.title("Average Rating by Online Ordering")
    plt.xlabel("Online Ordering")
    plt.ylabel("Average Rating")
    plt.xticks(rotation=0)
    plt.ylim(0, 5)
    plt.tight_layout()
    plt.savefig(path, dpi=200)
    plt.close()
    chart_paths["online"] = path

    # 4. Table booking
    path = os.path.join(viz_dir, "table_booking.png")
    booking_avg = df.groupby("book_table")["rate"].mean()
    plt.figure(figsize=(7, 5))
    booking_avg.plot(kind="bar")
    plt.title("Average Rating by Table Booking")
    plt.xlabel("Table Booking")
    plt.ylabel("Average Rating")
    plt.xticks(rotation=0)
    plt.ylim(0, 5)
    plt.tight_layout()
    plt.savefig(path, dpi=200)
    plt.close()
    chart_paths["booking"] = path

    # 5. Cost vs Rating
    path = os.path.join(viz_dir, "cost_vs_rating.png")
    plt.figure(figsize=(8, 5))
    sns.scatterplot(data=df, x="approx_cost", y="rate", alpha=0.5)
    plt.title("Restaurant Cost vs Rating")
    plt.xlabel("Approximate Cost for Two (₹)")
    plt.ylabel("Rating")
    plt.tight_layout()
    plt.savefig(path, dpi=200)
    plt.close()
    chart_paths["cost"] = path

    # 6. Votes vs Rating
    path = os.path.join(viz_dir, "votes_vs_rating.png")
    plt.figure(figsize=(8, 5))
    sns.scatterplot(data=df, x="votes", y="rate", alpha=0.5)
    plt.title("Customer Votes vs Rating")
    plt.xlabel("Votes")
    plt.ylabel("Rating")
    plt.tight_layout()
    plt.savefig(path, dpi=200)
    plt.close()
    chart_paths["votes"] = path

    # 7. Correlation heatmap
    path = os.path.join(viz_dir, "correlation_heatmap.png")
    numeric_columns = ["rate", "votes", "approx_cost"]
    correlation = df[numeric_columns].corr()
    plt.figure(figsize=(7, 5))
    sns.heatmap(correlation, annot=True, fmt=".2f", square=True)
    plt.title("Correlation Heatmap")
    plt.tight_layout()
    plt.savefig(path, dpi=200)
    plt.close()
    chart_paths["heatmap"] = path

    # 8. Category rating
    path = os.path.join(viz_dir, "category_rating.png")
    category_rating = df.groupby("restaurant_type")["rate"].mean().sort_values(ascending=False)
    plt.figure(figsize=(8, 5))
    category_rating.plot(kind="bar")
    plt.title("Average Rating by Restaurant Type")
    plt.xlabel("Restaurant Type")
    plt.ylabel("Average Rating")
    plt.xticks(rotation=0)
    plt.ylim(0, 5)
    plt.tight_layout()
    plt.savefig(path, dpi=200)
    plt.close()
    chart_paths["category_rating"] = path

    # 9. Category cost
    path = os.path.join(viz_dir, "category_cost.png")
    category_cost = df.groupby("restaurant_type")["approx_cost"].mean().sort_values()
    plt.figure(figsize=(8, 5))
    category_cost.plot(kind="bar")
    plt.title("Average Cost by Restaurant Type")
    plt.xlabel("Restaurant Type")
    plt.ylabel("Average Cost for Two (₹)")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(path, dpi=200)
    plt.close()
    chart_paths["category_cost"] = path

    print(f"Charts generated in: {viz_dir}")
    return chart_paths


# =============================================================================
# 7. POWER BI SCREENSHOT DETECTION
# =============================================================================

def find_powerbi_image(powerbi_dir):

    if not os.path.exists(powerbi_dir):
        return None

    possible_files = [
        "zomato_dashboard_screenshot.png",
        "Zomato_Dashboard.png",
        "Zomato_Dashboard.jpg",
        "dashboard.png"
    ]

    for filename in possible_files:
        path = os.path.join(powerbi_dir, filename)
        if os.path.exists(path):
            return path

    for filename in os.listdir(powerbi_dir):
        if filename.lower().endswith((".png", ".jpg", ".jpeg")):
            return os.path.join(powerbi_dir, filename)

    return None


# =============================================================================
# 8. READ SQL FILES
# =============================================================================

def read_sql_files(sql_dir):

    sql_files = []
    if not os.path.exists(sql_dir):
        return sql_files

    for filename in os.listdir(sql_dir):
        if filename.lower().endswith(".sql"):
            path = os.path.join(sql_dir, filename)
            try:
                with open(path, "r", encoding="utf-8") as file:
                    content = file.read()
                sql_files.append({"name": filename, "content": content})
            except Exception as error:
                print(f"Could not read {filename}: {error}")

    return sql_files


# =============================================================================
# 9. PDF STYLES
# =============================================================================

def create_styles():

    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name="ReportTitle", parent=styles["Title"], fontName="Helvetica-Bold",
        fontSize=26, leading=32, alignment=TA_CENTER, textColor=colors.HexColor("#CB202D"),
        spaceAfter=15
    ))

    styles.add(ParagraphStyle(
        name="Subtitle", parent=styles["Normal"], fontSize=13, leading=18,
        alignment=TA_CENTER, textColor=colors.HexColor("#4B5563"), spaceAfter=20
    ))

    styles.add(ParagraphStyle(
        name="Section", parent=styles["Heading1"], fontName="Helvetica-Bold",
        fontSize=17, leading=22, textColor=colors.HexColor("#CB202D"), spaceBefore=14, spaceAfter=10
    ))

    styles.add(ParagraphStyle(
        name="SubSection", parent=styles["Heading2"], fontName="Helvetica-Bold",
        fontSize=12, leading=16, textColor=colors.HexColor("#1F2937"), spaceBefore=10, spaceAfter=6
    ))

    styles.add(ParagraphStyle(
        name="BodyCustom", parent=styles["BodyText"], fontSize=9.5, leading=14,
        textColor=colors.HexColor("#374151"), spaceAfter=7
    ))

    styles.add(ParagraphStyle(
        name="BulletCustom", parent=styles["BodyText"], fontSize=9.5, leading=14,
        leftIndent=18, firstLineIndent=-10, spaceAfter=4
    ))

    styles.add(ParagraphStyle(
        name="Callout", parent=styles["BodyText"], fontSize=10, leading=15,
        backColor=colors.HexColor("#F3F4F6"), borderColor=colors.HexColor("#D1D5DB"),
        borderWidth=1, borderPadding=10, spaceBefore=7, spaceAfter=10
    ))

    styles.add(ParagraphStyle(
        name="Small", parent=styles["BodyText"], fontSize=8, leading=11,
        textColor=colors.HexColor("#6B7280")
    ))

    return styles


def make_table(data, widths=None, header=True):

    table = Table(data, colWidths=widths, repeatRows=1 if header else 0)
    table_style = [
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#D1D5DB")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6)
    ]

    if header:
        table_style.extend([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#CB202D")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold")
        ])

    table.setStyle(TableStyle(table_style))
    return table


def add_chart(story, path, title, styles, width=6.5):

    if not os.path.exists(path):
        return

    story.append(Paragraph(title, styles["SubSection"]))
    img = Image(path, width=width * inch, height=3.9 * inch)
    story.append(img)
    story.append(Spacer(1, 8))


# =============================================================================
# 12. BUILD PDF REPORT
# =============================================================================

def build_pdf_report(
    metrics,
    cleaning_stats,
    chart_paths,
    sql_files,
    powerbi_image,
    pdf_path,
    include_cleaning=True,
    include_eda=True
):

    styles = create_styles()
    doc = SimpleDocTemplate(
        pdf_path, pagesize=A4, rightMargin=40, leftMargin=40, topMargin=50, bottomMargin=50
    )
    story = []

    story.append(Spacer(1, 1.2 * inch))
    story.append(Paragraph("Zomato Restaurant<br/>Data Analysis", styles["ReportTitle"]))
    story.append(Paragraph("A Data Analytics & Business Intelligence Project", styles["Subtitle"]))
    story.append(HRFlowable(width="80%", thickness=2, color=colors.HexColor("#CB202D"), spaceAfter=25))
    story.append(Paragraph("Python • Pandas • NumPy • SQL • Power BI • Data Visualization", styles["Subtitle"]))
    story.append(Spacer(1, 1.5 * inch))

    title_info = [
        [Paragraph("<b>Project Type</b>", styles["BodyCustom"]), Paragraph("Data Analytics Project", styles["BodyCustom"])],
        [Paragraph("<b>Dataset</b>", styles["BodyCustom"]), Paragraph("Zomato Restaurant Dataset", styles["BodyCustom"])],
        [Paragraph("<b>Records Analyzed</b>", styles["BodyCustom"]), Paragraph(str(metrics["clean_rows"]), styles["BodyCustom"])]
    ]
    story.append(make_table(title_info, widths=[2.2 * inch, 4.2 * inch], header=False))
    story.append(PageBreak())

    # 1. Executive Summary
    story.append(Paragraph("1. Executive Summary", styles["Section"]))
    dining_share = metrics["type_shares"].get("Dining", 0)
    online_yes = metrics["online_rating"].get("Yes", np.nan)
    online_no = metrics["online_rating"].get("No", np.nan)
    booking_yes = metrics["booking_rating"].get("Yes", np.nan)
    booking_no = metrics["booking_rating"].get("No", np.nan)
    online_difference = round(online_yes - online_no, 2) if not pd.isna(online_yes) and not pd.isna(online_no) else 0
    booking_difference = round(booking_yes - booking_no, 2) if not pd.isna(booking_yes) and not pd.isna(booking_no) else 0

    summary = (
        f"This project analyzes {metrics['clean_rows']} restaurant records to understand restaurant distribution, "
        f"customer ratings, votes, pricing, online ordering and table booking behavior. The overall average rating is "
        f"<b>{metrics['avg_rating']}/5</b>, while the average cost for two people is approximately <b>₹{metrics['avg_cost']}</b>."
    )
    story.append(Paragraph(summary, styles["BodyCustom"]))
    story.append(Paragraph(f"Dining restaurants account for approximately <b>{dining_share}%</b> of the dataset.", styles["BodyCustom"]))

    # 2. Introduction
    story.append(Paragraph("2. Introduction", styles["Section"]))
    story.append(Paragraph("The restaurant industry generates large amounts of customer and business data.", styles["BodyCustom"]))

    # 3. Problem Statement
    story.append(Paragraph("3. Problem Statement", styles["Section"]))
    story.append(Paragraph("Restaurant businesses need to understand what factors are associated with customer ratings and popularity.", styles["BodyCustom"]))

    # 4. Objectives
    story.append(Paragraph("4. Project Objectives", styles["Section"]))
    objectives = [
        "Understand the structure and characteristics of the dataset.",
        "Clean and preprocess restaurant data.",
        "Analyze restaurant categories and their distribution.",
        "Study customer rating patterns.",
        "Identify actionable business insights.",
        "Create visualizations and a Power BI dashboard.",
        "Prepare a professional analytical report."
    ]
    for obj in objectives:
        story.append(Paragraph(f"• {obj}", styles["BulletCustom"]))

    # 5. Technology Stack
    story.append(Paragraph("5. Technology Stack", styles["Section"]))
    tech_data = [
        [Paragraph("<b>Technology</b>", styles["BodyCustom"]), Paragraph("<b>Purpose</b>", styles["BodyCustom"])],
        ["Python", "Data analysis and automation"],
        ["Pandas", "Data manipulation and cleaning"],
        ["NumPy", "Numerical operations"],
        ["Matplotlib", "Data visualization"],
        ["Seaborn", "Statistical visualization"],
        ["SQL", "Business queries and analysis"],
        ["Power BI", "Interactive dashboard"],
        ["ReportLab", "Automated PDF report generation"]
    ]
    story.append(make_table(tech_data, widths=[2.2 * inch, 4.2 * inch]))

    # 6. Dataset Description
    story.append(Paragraph("6. Dataset Description", styles["Section"]))
    ds_data = [
        [Paragraph("<b>Metric</b>", styles["BodyCustom"]), Paragraph("<b>Value</b>", styles["BodyCustom"])],
        ["Original Records", f"{metrics['raw_rows']:,}"],
        ["Final Records", f"{metrics['clean_rows']:,}"],
        ["Columns", str(metrics["columns"])]
    ]
    story.append(make_table(ds_data, widths=[3.5 * inch, 2.9 * inch]))

    if include_cleaning:
        story.append(Paragraph("7. Data Cleaning & Preprocessing", styles["Section"]))
        cleaning_steps = [
            "Removed duplicate restaurant records.",
            "Removed '/5' from rating column.",
            "Converted numeric fields.",
            "Standardized categorical values."
        ]
        for step in cleaning_steps:
            story.append(Paragraph(f"• {step}", styles["BulletCustom"]))

    if include_eda:
        story.append(Paragraph("8. Exploratory Data Analysis", styles["Section"]))
        add_chart(story, chart_paths.get("type", ""), "8.1 Restaurant Distribution", styles)
        add_chart(story, chart_paths.get("rating", ""), "8.2 Rating Distribution", styles)
        add_chart(story, chart_paths.get("online", ""), "8.3 Online Ordering and Rating", styles)
        add_chart(story, chart_paths.get("booking", ""), "8.4 Table Booking and Rating", styles)
        add_chart(story, chart_paths.get("cost", ""), "8.5 Cost vs Rating", styles)
        add_chart(story, chart_paths.get("votes", ""), "8.6 Votes vs Rating", styles)
        add_chart(story, chart_paths.get("heatmap", ""), "8.7 Correlation Heatmap", styles)

    # 9. Business Analysis
    story.append(Paragraph("9. Business Analysis", styles["Section"]))
    kpi_data = [
        [Paragraph("<b>KPI</b>", styles["BodyCustom"]), Paragraph("<b>Value</b>", styles["BodyCustom"])],
        ["Total Restaurants", f"{metrics['total_restaurants']:,}"],
        ["Average Rating", f"{metrics['avg_rating']} / 5"],
        ["Total Votes", f"{metrics['total_votes']:,}"],
        ["Average Cost", f"₹{metrics['avg_cost']}"]
    ]
    story.append(make_table(kpi_data, widths=[3.5 * inch, 2.9 * inch]))

    # 10. Insights & Recommendations
    story.append(Paragraph("10. Business Recommendations", styles["Section"]))
    recs = [
        "1. Introduce Online Ordering",
        "2. Offer Table Reservations",
        "3. Focus on Customer Experience",
        "4. Maintain Competitive Pricing"
    ]
    for r in recs:
        story.append(Paragraph(r, styles["SubSection"]))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF generated successfully: {pdf_path}")


# =============================================================================
# 13. BUILD MARKDOWN REPORT
# =============================================================================

def build_markdown_report(
    metrics,
    cleaning_stats,
    sql_files,
    md_path,
    include_cleaning=True,
    include_eda=True
):

    dining_share = metrics["type_shares"].get("Dining", 0)

    md = f"""# Zomato Restaurant Data Analysis

## Data Analytics & Business Intelligence Project

---

# 1. Executive Summary

This project analyzes **{metrics['clean_rows']:,} restaurant records** to understand restaurant distribution, ratings, customer votes, pricing, online ordering and table booking.

### Main KPIs

| KPI | Value |
|---|---:|
| Restaurants | {metrics['total_restaurants']:,} |
| Average Rating | {metrics['avg_rating']} / 5 |
| Total Votes | {metrics['total_votes']:,} |
| Average Cost for Two | ₹{metrics['avg_cost']} |
| Median Cost | ₹{metrics['median_cost']} |
| Median Rating | {metrics['median_rating']} / 5 |

Dining restaurants represent approximately **{dining_share}%** of the dataset.

---

# 2. Introduction

The restaurant industry generates large amounts of customer and business data.

---

# 3. Business Analysis

## 3.1 Overall KPIs

| KPI | Result |
|---|---:|
| Total Restaurants | {metrics['total_restaurants']:,} |
| Average Rating | {metrics['avg_rating']} / 5 |
| Average Cost | ₹{metrics['avg_cost']} |

---

# 4. Business Recommendations

1. Introduce Online Ordering
2. Offer Table Reservations
3. Focus on Customer Experience
4. Maintain Competitive Pricing

---

# End of Report
"""

    os.makedirs(os.path.dirname(md_path), exist_ok=True)
    with open(md_path, "w", encoding="utf-8") as file:
        file.write(md)

    print(f"Markdown report generated successfully: {md_path}")


# =============================================================================
# 14. MAIN PIPELINE
# =============================================================================

def main():

    import argparse

    parser = argparse.ArgumentParser(description="Zomato Analysis Report Generator")
    parser.add_argument("--skip-cleaning", action="store_true", help="Skip Data Cleaning section")
    parser.add_argument("--skip-eda", action="store_true", help="Skip EDA section")
    parser.add_argument("--skip-eda-cleaning", action="store_true", help="Skip both Data Cleaning and EDA")

    args = parser.parse_args()

    include_cleaning = not (args.skip_cleaning or args.skip_eda_cleaning)
    include_eda = not (args.skip_eda or args.skip_eda_cleaning)

    print("=" * 80)
    print("ZOMATO RESTAURANT DATA ANALYSIS - AUTOMATED REPORT GENERATOR")
    print("=" * 80)

    paths = get_project_paths()
    raw_df, df = load_data(paths)
    df, cleaning_stats = clean_data(df)

    os.makedirs(os.path.dirname(paths["processed_data"]), exist_ok=True)
    df.to_csv(paths["processed_data"], index=False)

    metrics = calculate_metrics(df, cleaning_stats, raw_df)
    viz_dir = paths["visualization"]
    chart_paths = generate_charts(df, viz_dir)

    # Using saved PNGs directly from the existing visualization folder (paths["visualization"])

    sql_files = read_sql_files(paths["sql"])
    powerbi_image = find_powerbi_image(paths["powerbi"])

    pdf_path = os.path.join(paths["reports"], "Zomato_Analysis_Report.pdf")
    md_path = os.path.join(paths["reports"], "Zomato_Analysis_Report.md")

    build_pdf_report(
        metrics, cleaning_stats, chart_paths, sql_files, powerbi_image, pdf_path,
        include_cleaning=include_cleaning, include_eda=include_eda
    )

    build_markdown_report(
        metrics, cleaning_stats, sql_files, md_path,
        include_cleaning=include_cleaning, include_eda=include_eda
    )

    print("=" * 80)
    print("REPORT GENERATION COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    main()
