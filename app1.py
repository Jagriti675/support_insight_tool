import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page Config

st.set_page_config(
    page_title="Cubelelo Support Dashboard",
    page_icon="📊",
    layout="wide"
)

# Load Data 

df = pd.read_csv("data.csv")
df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

df["Status"] = df["Status"].astype(str).str.strip().str.lower()
df["Category"] = df["Category"].astype(str).str.strip()

# Title 

st.title("📊 Support Insights Dashboard")

st.markdown("### Weekly Customer Support Report")

st.divider()



st.sidebar.title("Navigation")

option = st.sidebar.radio(
    "Select Section",
    [
        "Dashboard",
        "Dataset"
    ]
)

if option=="Dataset":
    st.subheader("Dataset")
    st.dataframe(df)

# KPI Cards

total = len(df)

open_count = len(df[df["Status"]=="open"])

pending = len(df[df["Status"]=="pending"])

closed = len(df[df["Status"].isin(["closed","resolved"])])

col1,col2,col3,col4 = st.columns(4)

col1.metric("📄 Total Tickets",total)

col2.metric("🟢 Open",open_count)

col3.metric("🟡 Pending",pending)

col4.metric("✅ Closed",closed)

st.divider()

#  Top Issues 

col1,col2 = st.columns(2)

with col1:

    st.subheader("📈 Top Issue Categories")

    issue=df["Category"].value_counts()

    st.bar_chart(issue)

with col2:

    st.subheader("🥧 Ticket Status Distribution")

    status=df["Status"].value_counts()

    fig,ax=plt.subplots()

    ax.pie(status.values,
           labels=status.index,
           autopct="%1.1f%%")

    st.pyplot(fig)

st.divider()

#  Product Complaints 

st.subheader("📦 Most Complained Products")

product=df["Product"].value_counts()

st.bar_chart(product)

st.divider()

#  Unresolved 

def reason(status):

    if status=="open":
        return "Still waiting for action"

    elif status=="pending":
        return "Waiting for warehouse"

    elif status=="escalated":
        return "Manager approval required"

    else:
        return "Under investigation"

unresolved=df[
    ~df["Status"].isin(["closed","resolved"])
].copy()

unresolved["Reason"]=unresolved["Status"].apply(reason)

st.subheader("🚨 Unresolved Tickets")

st.dataframe(unresolved)

st.divider()

# High Priority 

priority=unresolved[
    unresolved["Category"].isin([
        "Delivery Delay",
        "Damaged Product"
    ])
]

st.subheader("🔥 High Priority Tickets")

st.dataframe(priority)

st.divider()

#  Insights

st.subheader("💡 Key Insights")

top_issue=issue.idxmax()

top_product=product.idxmax()

st.success(f"""
• Most common issue : {top_issue}

• Product with highest complaints : {top_product}

• Total unresolved tickets : {len(unresolved)}

• Support team should prioritize Delivery Delay and Pending tickets.
""")

st.divider()

# Manager Summary 

st.subheader("📝 Manager Summary")

st.info(f"""

Top issue this week: **{top_issue}**

{len(unresolved)} tickets remain unresolved.

Most complaints are related to **{top_product}**.

Immediate attention should be given to pending delivery cases.

Warehouse and support coordination should be improved.

""")