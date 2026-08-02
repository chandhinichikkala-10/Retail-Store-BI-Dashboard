import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Retail Store BI Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>

#MainMenu{
visibility:hidden;
}

footer{
visibility:hidden;
}

header{
visibility:hidden;
}

.block-container{
padding-top:1rem;
padding-bottom:2rem;
padding-left:2rem;
padding-right:2rem;
}

[data-testid="stMetric"]{
background:#ffffff;
border-radius:15px;
padding:18px;
box-shadow:0px 4px 15px rgba(0,0,0,0.10);
border-left:8px solid #1565C0;
}

div[data-testid="metric-container"]{
background:white;
border-radius:15px;
padding:15px;
box-shadow:0px 5px 12px rgba(0,0,0,0.12);
}

section[data-testid="stSidebar"]{
background:#0F172A;
}

section[data-testid="stSidebar"] *{
color:white;
}

h1{
font-family:Arial;
}

</style>
""",unsafe_allow_html=True)

# =====================================================
# HEADER
# =====================================================

st.markdown("""
<h1 style='text-align:center;
color:#1565C0;
font-size:42px;'>

🏪 Retail Store Business Intelligence Dashboard

</h1>

<p style='text-align:center;
font-size:18px;
color:gray;'>

Sales • Revenue • Profit • Inventory • Customer Analytics

</p>

""",unsafe_allow_html=True)

st.markdown("---")

# =====================================================
# LOAD DATA
# =====================================================

from pathlib import Path

DATA_FILE = Path(__file__).parent.parent / "Retail_Store_Sales.csv"
df = pd.read_csv(DATA_FILE)
df["Order_Date"] = pd.to_datetime(df["Order_Date"])

df["Month"] = df["Order_Date"].dt.strftime("%B")

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title("📌 Dashboard Filters")

selected_region = st.sidebar.multiselect(
"Select Region",
options=df["Region"].unique(),
default=df["Region"].unique()
)

selected_category = st.sidebar.multiselect(
"Select Category",
options=df["Category"].unique(),
default=df["Category"].unique()
)

selected_month = st.sidebar.multiselect(
"Select Month",
options=df["Month"].unique(),
default=df["Month"].unique()
)

df = df[
(df["Region"].isin(selected_region))
&
(df["Category"].isin(selected_category))
&
(df["Month"].isin(selected_month))
]

st.sidebar.markdown("---")

st.sidebar.success("Dashboard Updated")

# =====================================================
# KPI CALCULATIONS
# =====================================================

total_revenue = df["Revenue"].sum()

total_profit = df["Profit"].sum()

total_orders = df["Order_ID"].count()

total_quantity = df["Quantity_Sold"].sum()

average_rating = round(df["Customer_Rating"].mean(),2)

profit_margin = round(
(total_profit/total_revenue)*100,
2
)

top_product = (
df.groupby("Product_Name")["Revenue"]
.sum()
.idxmax()
)
# =====================================================
# KPI SECTION
# =====================================================

st.markdown("## 📊 Key Performance Indicators")

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:

    st.metric(
        label="💰 Total Revenue",
        value=f"₹ {total_revenue:,.0f}"
    )

with kpi2:

    st.metric(
        label="📈 Total Profit",
        value=f"₹ {total_profit:,.0f}"
    )

with kpi3:

    st.metric(
        label="📦 Total Orders",
        value=f"{total_orders}"
    )

with kpi4:

    st.metric(
        label="🛒 Quantity Sold",
        value=f"{total_quantity}"
    )

st.write("")

kpi5, kpi6, kpi7 = st.columns(3)

with kpi5:

    st.metric(
        label="⭐ Customer Rating",
        value=f"{average_rating} / 5"
    )

with kpi6:

    st.metric(
        label="📉 Profit Margin",
        value=f"{profit_margin}%"
    )

with kpi7:

    st.metric(
        label="🏆 Best Selling Product",
        value=top_product
    )

st.markdown("---")

# =====================================================
# DASHBOARD SUMMARY
# =====================================================

left,right = st.columns([3,2])

with left:

    st.info("""
### 📌 Dashboard Overview

This dashboard provides a complete overview of the retail business performance.

✔ Revenue Analysis

✔ Profit Analysis

✔ Inventory Monitoring

✔ Customer Satisfaction

✔ Regional Sales Analysis

✔ Product Performance

✔ Payment Mode Analysis

""")

with right:

    st.success(f"""

### 📅 Report Summary

**Total Revenue**

₹ {total_revenue:,.0f}

**Total Profit**

₹ {total_profit:,.0f}

**Orders**

{total_orders}

**Average Rating**

{average_rating}

""")

st.markdown("---")
# =====================================================
# MONTHLY SALES TREND
# =====================================================

month_order = [
    "January","February","March","April","May","June",
    "July","August","September","October","November","December"
]

monthly_sales = (
    df.groupby("Month")["Revenue"]
    .sum()
    .reset_index()
)

monthly_sales["Month"] = pd.Categorical(
    monthly_sales["Month"],
    categories=month_order,
    ordered=True
)

monthly_sales = monthly_sales.sort_values("Month")

fig_month = px.line(
    monthly_sales,
    x="Month",
    y="Revenue",
    markers=True,
    title="📈 Monthly Sales Trend"
)

fig_month.update_layout(
    template="plotly_white",
    height=420,
    title_x=0.25,
    hovermode="x unified"
)

fig_month.update_traces(
    line_color="#1565C0",
    line_width=4,
    marker=dict(size=8)
)

# =====================================================
# SALES BY CATEGORY
# =====================================================

category_sales = (
    df.groupby("Category")["Revenue"]
    .sum()
    .reset_index()
)

fig_category = px.pie(
    category_sales,
    names="Category",
    values="Revenue",
    hole=0.45,
    title="🥧 Sales by Category",
    color_discrete_sequence=px.colors.qualitative.Set3
)

fig_category.update_layout(
    template="plotly_white",
    height=420,
    title_x=0.25
)

# =====================================================
# DISPLAY FIRST ROW
# =====================================================

left_chart, right_chart = st.columns(2)

with left_chart:
    st.plotly_chart(
        fig_month,
        use_container_width=True
    )

with right_chart:
    st.plotly_chart(
        fig_category,
        use_container_width=True
    )

st.markdown("---")

# =====================================================
# BEST SELLING PRODUCTS
# =====================================================

best_products = (
    df.groupby("Product_Name")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig_products = px.bar(
    best_products,
    x="Revenue",
    y="Product_Name",
    orientation="h",
    title="🏆 Top 10 Best Selling Products",
    color="Revenue",
    color_continuous_scale="Blues"
)

fig_products.update_layout(
    template="plotly_white",
    height=420,
    title_x=0.20
)

# =====================================================
# SALES BY REGION
# =====================================================

region_sales = (
    df.groupby("Region")["Revenue"]
    .sum()
    .reset_index()
)

fig_region = px.bar(
    region_sales,
    x="Region",
    y="Revenue",
    color="Region",
    title="🌍 Sales by Region"
)

fig_region.update_layout(
    template="plotly_white",
    height=420,
    title_x=0.25
)

# =====================================================
# DISPLAY SECOND ROW
# =====================================================

left_chart2, right_chart2 = st.columns(2)

with left_chart2:
    st.plotly_chart(
        fig_products,
        use_container_width=True
    )

with right_chart2:
    st.plotly_chart(
        fig_region,
        use_container_width=True
    )

st.markdown("---")
# =====================================================
# PAYMENT MODE ANALYSIS
# =====================================================

payment_sales = (
    df.groupby("Payment_Mode")["Revenue"]
    .sum()
    .reset_index()
)

fig_payment = px.pie(
    payment_sales,
    names="Payment_Mode",
    values="Revenue",
    title="💳 Sales by Payment Mode",
    hole=0.45,
    color_discrete_sequence=px.colors.qualitative.Pastel
)

fig_payment.update_layout(
    template="plotly_white",
    height=420,
    title_x=0.22
)

# =====================================================
# PROFIT BY CATEGORY
# =====================================================

profit_category = (
    df.groupby("Category")["Profit"]
    .sum()
    .reset_index()
)

fig_profit = px.bar(
    profit_category,
    x="Category",
    y="Profit",
    title="💹 Profit by Category",
    color="Category",
    color_discrete_sequence=px.colors.qualitative.Bold
)

fig_profit.update_layout(
    template="plotly_white",
    height=420,
    title_x=0.25
)

# =====================================================
# DISPLAY THIRD ROW
# =====================================================

left3, right3 = st.columns(2)

with left3:
    st.plotly_chart(fig_payment, use_container_width=True)

with right3:
    st.plotly_chart(fig_profit, use_container_width=True)

st.markdown("---")

# =====================================================
# INVENTORY STATUS
# =====================================================

st.subheader("📦 Inventory Status")

inventory_table = df[
    [
        "Product_Name",
        "Category",
        "Current_Stock",
        "Inventory_Status"
    ]
].sort_values(
    by="Current_Stock",
    ascending=True
)

st.dataframe(
    inventory_table,
    use_container_width=True,
    hide_index=True,
    height=350
)

st.markdown("---")

# =====================================================
# CUSTOMER SATISFACTION
# =====================================================

st.subheader("⭐ Customer Satisfaction Score")

gauge = go.Figure(
    go.Indicator(
        mode="gauge+number",
        value=average_rating,
        title={"text": "Average Customer Rating"},
        gauge={
            "axis": {"range": [0, 5]},
            "bar": {"color": "#1565C0"},
            "steps": [
                {"range": [0, 2], "color": "#ffcccc"},
                {"range": [2, 3.5], "color": "#fff3b0"},
                {"range": [3.5, 5], "color": "#d4edda"}
            ]
        }
    )
)

gauge.update_layout(
    height=350
)

st.plotly_chart(
    gauge,
    use_container_width=True
)

st.markdown("---")
# =====================================================
# BUSINESS INSIGHTS
# =====================================================

st.markdown("## 📈 Business Insights")

left,right = st.columns(2)

with left:

    top_region = (
        df.groupby("Region")["Revenue"]
        .sum()
        .idxmax()
    )

    top_category = (
        df.groupby("Category")["Revenue"]
        .sum()
        .idxmax()
    )

    st.success(f"""

### 🏆 Top Performing Region

**{top_region}**

---

### 🛍️ Best Selling Category

**{top_category}**

---

### 💰 Profit Margin

**{profit_margin}%**

""")

with right:

    low_stock = len(
        df[df["Inventory_Status"]=="Low Stock"]
    )

    out_stock = len(
        df[df["Inventory_Status"]=="Out of Stock"]
    )

    st.warning(f"""

### 📦 Inventory Summary

Low Stock Products : **{low_stock}**

Out Of Stock Products : **{out_stock}**

Average Customer Rating :

**⭐ {average_rating} / 5**

""")

st.markdown("---")

# =====================================================
# DASHBOARD SUMMARY
# =====================================================

st.markdown("""
## 📋 Executive Summary
""")

summary1,summary2,summary3 = st.columns(3)

with summary1:

    st.info("""

### Revenue

✔ Total Revenue

✔ Monthly Revenue Trend

✔ Regional Revenue

✔ Category Revenue

""")

with summary2:

    st.success("""

### Sales

✔ Best Selling Products

✔ Quantity Sold

✔ Orders

✔ Payment Analysis

""")

with summary3:

    st.warning("""

### Customers

✔ Customer Rating

✔ Inventory Status

✔ Profit Analysis

✔ Business Performance

""")

st.markdown("---")

# =====================================================
# DOWNLOAD REPORT
# =====================================================

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(

label="📥 Download Filtered Dataset",

data=csv,

file_name="Retail_Report.csv",

mime="text/csv"

)

st.markdown("---")

# =====================================================
# FOOTER
# =====================================================

st.markdown("""

<style>

.footer{

background:#1565C0;

padding:20px;

border-radius:15px;

text-align:center;

color:white;

font-size:18px;

}

</style>

<div class="footer">

📊 Retail Store Business Intelligence Dashboard

<br><br>

Developed using

<b>Python | Streamlit | Plotly | Pandas</b>

<br><br>

© 2026 Retail Analytics Project

</div>

""",unsafe_allow_html=True)