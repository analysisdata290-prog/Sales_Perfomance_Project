# Sales ETL Pipeline

Automated ETL pipeline that extracts sales data from Google Sheets, transforms it, and loads it into Supabase PostgreSQL for interactive dashboards.

## 📊 Overview
This project automates the daily extraction, transformation, and loading (ETL) of sales data from Google Sheets to Supabase PostgreSQL. The pipeline runs automatically at 5:00 PM daily, ensuring the sales dashboard always displays up-to-date information.

## 🏗️ Architecture
```
Google Sheets → Python ETL → Supabase PostgreSQL → SQL Views → Power BI → Interactive Dashboard
```

## 📁 Data Sources
The pipeline reads from two Google Sheets tabs:
- **Summary:** Weekly sales summary (sales volume, customers, meetings)
- **Annual Map:** Daily granular data (contacts, leads, meetings, contracts)

## 🔄 Data Flow
1. **Extract:** Python script reads data from Google Sheets
2. **Transform:** Data is cleaned and standardized
3. **Load:** Data is uploaded to Supabase tables (`summary` and `annual_map`)
4. **Visualize:** Power BI connects to SQL Views

## 🛠️ Technologies
- Python 3.10+ | Pandas | Requests | Supabase | GitHub Actions

## 🚀 Setup
```bash
git clone https://github.com/*****/sales-etl-pipeline.git
cd sales-etl-pipeline
pip install -r requirements.txt
```

Create a `.env` file:
```env
SUPABASE_URL=******
SUPABASE_SERVICE_KEY=*****
SALES_SHEET_ID=*****
```

Run the script:
```bash
python sales_etl.py
```

## ⏰ Scheduling
The pipeline runs automatically at **5:00 PM Egypt Time (3:00 PM UTC)** daily via GitHub Actions.

## 📊 Database Schema

**Table: `summary`**
| Column | Type | Description |
|--------|------|-------------|
| date_range | TEXT | Weekly date range |
| total_sales_value | NUMERIC | Total sales value |
| no_of_customers | INTEGER | Number of customers |
| no_of_data_customers | INTEGER | Data channel customers |
| no_of_leads_customers | INTEGER | Leads channel customers |
| data_sales_volume | NUMERIC | Sales from data channel |
| leads_sales_volume | NUMERIC | Sales from leads channel |
| next_week_sales_forecast | NUMERIC | Forecast for next week |
| no_of_data_meetings | INTEGER | Data channel meetings |
| no_of_leads_meetings | INTEGER | Leads channel meetings |

**Table: `annual_map`**
| Column | Type | Description |
|--------|------|-------------|
| date | DATE | Daily date |
| daily_contacts | INTEGER | Daily contacts |
| leads | INTEGER | Leads generated |
| meetings | INTEGER | Meetings scheduled |
| meetings_done | INTEGER | Meetings completed |
| contracts | INTEGER | Contracts signed |
| contracts_value | NUMERIC | Contract value |
| paid_clients | INTEGER | Paid clients |
| total_sales | NUMERIC | Total daily sales |

## 📈 Portfolio Dashboard
This ETL pipeline powers the **Sales Performance Dashboard**, visualizing:
- Data vs Leads Sales Comparison
- Sales Funnel Analysis
- Monthly Performance Trends
- KPI Monitoring

## 📁 Project Structure
```
sales-etl-pipeline/
├── .github/workflows/sales_etl.yml
├── sales_etl.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## 📬 Contact
- **Portfolio:** [رابط Google Sites]
- **LinkedIn:** [رابط LinkedIn]
- **GitHub:** [رابط GitHub]
