import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="RetailPulse | Retail Intelligence", page_icon="📊", layout="wide")
DATA = Path(__file__).parent / "data" / "processed"

@st.cache_data
def load_csv(name):
    path = DATA / name
    if not path.exists():
        st.error(f"Missing data file: {path}")
        st.stop()
    return pd.read_csv(path)

rfm = load_csv("customer_rfm_segments.csv")
daily = load_csv("daily_total_demand.csv")
monthly = load_csv("monthly_sales_summary.csv")
inventory = load_csv("inventory_reorder_recommendations.csv")
churn = load_csv("churn_proxy_features.csv")

st.title("📊 RetailPulse")
st.caption("AI-powered customer analytics & demand forecasting · Analytics prototype")
page = st.sidebar.radio("Navigate", ["Executive Overview","Sales Trends","Customer Analytics","Demand Forecast","Inventory"])
st.sidebar.caption("Metrics use supplied CSV artifacts. Churn labels are proxies; forecasts are baseline estimates.")

if page == "Executive Overview":
    a,b,c,d=st.columns(4)
    a.metric("Customers",f"{rfm['Customer ID'].nunique():,}")
    b.metric("Products",f"{inventory['StockCode'].nunique():,}")
    c.metric("Revenue",f"{monthly['revenue'].sum():,.0f}")
    d.metric("Invoices",f"{monthly['invoices'].sum():,.0f}")
    st.plotly_chart(px.line(monthly,x="InvoiceMonth",y="revenue",markers=True,title="Monthly revenue"),use_container_width=True)
    seg=rfm["Segment"].value_counts().rename_axis("Segment").reset_index(name="Customers")
    st.plotly_chart(px.bar(seg,x="Segment",y="Customers",title="RFM segment distribution"),use_container_width=True)
elif page == "Sales Trends":
    metric=st.selectbox("Measure",["revenue","units","invoices","customers"])
    st.plotly_chart(px.line(monthly,x="InvoiceMonth",y=metric,markers=True),use_container_width=True)
    st.dataframe(monthly,use_container_width=True)
    st.plotly_chart(px.line(daily,x="InvoiceDate",y="daily_units",title="Daily unit demand"),use_container_width=True)
elif page == "Customer Analytics":
    options=sorted(rfm["Segment"].dropna().unique())
    selected=st.multiselect("RFM segments",options,default=options)
    f=rfm[rfm["Segment"].isin(selected)]
    x,y=st.columns(2)
    x.plotly_chart(px.histogram(f,x="Segment",title="Segment sizes"),use_container_width=True)
    y.plotly_chart(px.scatter(f,x="Frequency",y="Monetary",color="Segment",hover_data=["Customer ID"]),use_container_width=True)
    st.warning("ChurnProxy is a heuristic proxy label—not validated ground-truth churn or a deployed prediction model.")
    st.dataframe(churn.head(1000),use_container_width=True)
elif page == "Demand Forecast":
    horizon=st.slider("Forecast horizon (days)",7,90,30)
    d=daily.copy()
    d["InvoiceDate"]=pd.to_datetime(d["InvoiceDate"],errors="coerce")
    d=d.dropna(subset=["InvoiceDate"]).sort_values("InvoiceDate")
    if len(d)>=7:
        avg=float(d["daily_units"].tail(7).mean())
        dates=pd.date_range(d["InvoiceDate"].max()+pd.Timedelta(days=1),periods=horizon,freq="D")
        fc=pd.DataFrame({"InvoiceDate":dates,"daily_units":avg,"series":"Baseline forecast"})
        hist=d.tail(120).assign(series="Observed")
        st.metric("Trailing 7-day average",f"{avg:,.1f} units/day")
        st.plotly_chart(px.line(pd.concat([hist,fc],ignore_index=True),x="InvoiceDate",y="daily_units",color="series"),use_container_width=True)
        st.info("Transparent moving-average baseline only. Backtest before operational use; this is not Prophet/LSTM/hybrid.")
    else: st.error("Insufficient dated demand observations.")
elif page == "Inventory":
    sort=st.selectbox("Sort recommendations by",["suggested_order_qty","reorder_point","total_revenue"])
    n=st.slider("Rows to display",100,2000,500,step=100)
    st.dataframe(inventory.sort_values(sort,ascending=False).head(n),use_container_width=True)
    st.plotly_chart(px.scatter(inventory,x="mean_daily_demand",y="reorder_point",size="suggested_order_qty",hover_data=["StockCode"]),use_container_width=True)
    st.warning("Recommendations rely on assumptions. Verify lead time, service level, stock on hand, and supplier constraints.")
