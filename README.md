# Zomato Restaurant Data Analytics & Business Intelligence Project

A comprehensive Data Analytics and Business Intelligence end-to-end project analyzing **780 restaurant records** to uncover key insights into pricing, customer ratings, votes, online ordering, and table booking availability.

---

## 📊 Executive Summary & Key KPIs

| Key Performance Indicator | Value |
| :--- | :---: |
| **Total Restaurants Analyzed** | **780** |
| **Average Rating** | **3.69 / 5** |
| **Total Customer Votes** | **253,772** |
| **Average Cost for Two** | **₹458** |
| **Median Cost for Two** | **₹440** |
| **Median Rating** | **3.80 / 5** |

### Key Findings
* **Dining Dominance**: Dining restaurants represent **70.0%** of all restaurants in the dataset.
* **Online Ordering Impact**: Restaurants offering online ordering show an average rating difference of **+0.34 points** compared to non-online ordering establishments.
* **Table Booking Impact**: Establishments providing table reservations show an average rating difference of **+0.51 points**.
* **Engagement Correlation**: Customer votes have a **0.49 correlation** with restaurant ratings, proving stronger than cost correlation (**0.25**).

---

## 📁 Repository Structure

```
Zomato/
├── README.md                             # Project documentation
├── .gitignore                            # Git ignore rules
├── data/
│   ├── clean/
│   │   └── Zomato_cleaned.csv            # Cleaned & processed dataset (780 records)
│   └── raw/
│       └── Zomato.csv                    # Raw initial dataset (1,000 records)
├── notebooks/
│   ├── data_cleaning.ipynb               # Data cleaning & preprocessing notebook
│   ├── data_validations.ipynb            # Data integrity validation checks
│   └── EDA.ipynb                         # Exploratory Data Analysis notebook
├── powerbi/
│   ├── zomato.pbix                       # Interactive Power BI dashboard file
│   └── zomato_dashboard_screenshot.png   # Preview screenshot of the dashboard
├── reports/
│   ├── Zomato_Analysis_Report.pdf        # Automated final PDF report
│   ├── Zomato_Analysis_Report.md         # Final Markdown report
│   └── generate_report.py                # Automated Python report generator script
├── sql/
│   ├── business_queries.sql              # 16+ analytical SQL business queries
│   └── zomato_database.sql               # Database DDL schema & table creation
└── visualization/                        # Exported EDA visualization charts (PNG)
    ├── average_rating.png
    ├── Correlation_Heatmap.png
    ├── Cost_Distribution.png
    ├── Cost_vs_Rating.png
    ├── Online_ordering_Distribution.png
    ├── Ordering_vs_Rating.png
    ├── restaurant_Distribution.png
    ├── restaurant_type_count.png
    ├── Restaurants_by_Votes.png
    ├── Table_Booking_Distribution.png
    └── TableBooking_vs_Rating.png
```

---

## 🛠️ Technology Stack & Tools

* **Programming Language**: Python 3.x
* **Data Processing & Analysis**: Pandas, NumPy
* **Data Visualization**: Matplotlib, Seaborn
* **Database & SQL**: MySQL / PostgreSQL compatible DDL & Analytical SQL Queries
* **Business Intelligence Dashboard**: Power BI
* **PDF Report Automation**: ReportLab

---

## 🚀 Getting Started & Execution

### 1. Prerequisites
Ensure Python 3.8+ is installed on your system along with the required libraries:

```bash
pip install pandas numpy matplotlib seaborn reportlab
```

### 2. Running Data Cleaning & EDA Notebooks
Open Jupyter Notebook or VS Code to run the notebooks in order:
1. `notebooks/data_cleaning.ipynb`
2. `notebooks/data_validations.ipynb`
3. `notebooks/EDA.ipynb`

### 3. Automated PDF & Markdown Report Generation
To regenerate the full PDF and Markdown reports automatically:

```bash
python reports/generate_report.py
```

#### Optional Flags:
- Skip Data Cleaning section: `python reports/generate_report.py --skip-cleaning`
- Skip EDA section: `python reports/generate_report.py --skip-eda`
- Skip both Data Cleaning & EDA: `python reports/generate_report.py --skip-eda-cleaning`

---

## 💡 Business Recommendations

1. **Adopt Online Ordering**: Restaurants currently lacking online ordering should onboard digital food platforms to boost visibility and customer feedback.
2. **Implement Table Reservations**: Dine-in restaurants can drive customer satisfaction (+0.51 rating uplift) by introducing reservation options.
3. **Focus on Engagement over Pricing**: Because votes correlate strongly with high ratings (0.49), restaurants should actively encourage customer reviews and feedback.
