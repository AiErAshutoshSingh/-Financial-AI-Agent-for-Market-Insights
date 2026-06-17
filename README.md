

# AI-Powered Personal Finance Assistant 

An end-to-end AI-powered Personal Finance Assistant built using **Streamlit, LangChain, ChromaDB, SQLite, Pandas, Plotly, ReportLab, and Yahoo Finance**. The application helps users manage expenses, analyze investments, interact with financial documents using Retrieval-Augmented Generation (RAG), generate financial reports, and receive personalized financial insights through an interactive dashboard.

---

# Features

## AI Finance Assistant

* Chat with your financial data.
* Ask questions about expenses, investments, and uploaded documents.
* AI-generated financial insights and recommendations.
* Context-aware responses using RAG.

##  Expense Tracker

* Upload expense CSV files.
* Automatic expense categorization and analysis.
* Interactive transaction management.
* Spending summaries and insights.
  
## Financial Dashboard

* KPI cards and financial metrics.
* Expense distribution analysis.
* Monthly and category-wise trends.
* Interactive visualizations.

##  Stock Market Analysis

* Real-time stock market data.
* Market capitalization analysis.
* PE Ratio and valuation metrics.
* Candlestick and trend charts.
* Risk and performance analysis.

##  Financial Document Intelligence (RAG)

* Upload financial PDFs.
* Intelligent document search.
* Question answering over uploaded documents.
* Context-aware financial insights.

## Financial Report Generation

* Expense reports.
* Investment summaries.
* Financial health reports.
* Downloadable PDF reports.

##  Data Management

* Persistent vector database storage.
* SQLite-based data management.
* Historical financial records.
* User activity tracking.

---

# System Architecture

```text
User
 │
 ▼
Streamlit Application
 │
 ├── Expense Tracker
 ├── Dashboard
 ├── Stock Analysis
 ├── Finance Assistant
 ├── PDF Reports
 └── RAG Document Search
 │
 ▼
AI Processing Layer
 │
 ├── LangChain
 ├── ChromaDB
 ├── SQLite
 ├── Financial Analytics
 └── Document Retrieval
 │
 ▼
Insights & Recommendations
```

---

# 🛠️ Technology Stack

## Frontend

* Streamlit

## AI & RAG

* LangChain
* Retrieval-Augmented Generation (RAG)

## Vector Database

* ChromaDB
* Sentence Transformers

## Data Processing

* Pandas
* NumPy

## Visualization

* Plotly

## Financial Data

* Yahoo Finance (yFinance)

## Database

* SQLite

## Report Generation

* ReportLab

---

# Project Structure

```text
Finance_Assistant/

│
├── app.py
│
├── pages/
│   ├── AI_Assistant.py
│   ├── Expense_Tracker.py
│   ├── Dashboard.py
│   ├── Stock_Analysis.py
│   ├── Finance_RAG.py
│   ├── Reports.py
│   └── Settings.py
│
├── uploads/
├── vector_db/
├── reports/
├── database/
├── data/
│
├── requirements.txt
├── .env
└── README.md
```

---

# ⚙️ Installation

## 1. Clone Repository

```bash
git clone <your-repository-url>
cd Finance_Assistant
```

## 2. Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python -m venv venv
source venv/bin/activate
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Run the Application

```bash
streamlit run app.py
```

The application will launch locally:

```text
http://localhost:8501
```

---

# 📊 Example Use Cases

### Expense Analysis

```text
How much did I spend on Food last month?
```

### Financial Insights

```text
Which category has the highest spending?
```

### Investment Analysis

```text
Analyze TCS stock performance.
```

### Financial Document Q&A

```text
Summarize my uploaded annual report.
```

### Personalized Recommendations

```text
How can I improve my savings?
```

```text
Where am I overspending?
```

```text
Can I increase my monthly investments?
```

---

# 📈 Future Enhancements

* Portfolio Tracker
* Voice-Based Financial Assistant
* User Authentication
* AI Investment Advisor
* Financial News Analysis
* Portfolio Risk Assessment
* Automated Report Scheduling
* Mobile Responsive Interface
* Cloud Deployment
* Multi-User Support

---

# Skills Demonstrated

This project showcases:

* Artificial Intelligence Applications
* Retrieval-Augmented Generation (RAG)
* Financial Data Analytics
* Data Visualization
* Vector Databases
* PDF Processing
* Streamlit Development
* End-to-End AI Product Development
* Financial Intelligence Systems

---
