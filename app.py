import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(page_title="RetailPulse | Intelligence Suite", page_icon="◈", layout="wide", initial_sidebar_state="expanded")
DATA=Path(__file__).parent/"data"/"processed"

# ── Design system ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Manrope:wght@400;500;600;700;800&display=swap');
:root{--ink:#e9eef8;--muted:#91a0b8;--panel:#101a2b;--line:#24344c;--cyan:#52e0d0;--blue:#7799ff}
html,body,[class*="css"]{font-family:'Manrope',sans-serif}
.stApp{background:radial-gradient(ellipse at 8% 0%,#17243b 0%,#080e19 48%,#080e19 100%);color:var(--ink)}
section[data-testid="stSidebar"]{background:#0b1321;border-right:1px solid #203049}
section[data-testid="stSidebar"] .block-container{padding-top:1.5rem}
h1,h2,h3{font-weight:800;letter-spacing:-.04em;color:#f1f5ff}
h1{font-size:2.2rem!important} h2{font-size:1.35rem!important}
p, label, .stCaption{color:var(--muted)}
div[data-testid="stMetric"]{background:linear-gradient(135deg,#121e31,#0e1726);border:1px solid #263750;padding:17px 19px;border-radius:15px}
div[data-testid="stMetric"] label{color:#9aabc4!important;font-size:.78rem!important}
div[data-testid="stMetric"] [data-testid="stMetricValue"]{color:#eff5ff;font-weight:800}
.stButton>button{border-radius:10px;border:1px solid #314764;background:#142239;color:#eaf1ff}
.stButton>button:hover{border-color:#52e0d0;color:#52e0d0}
div[data-testid="stDataFrame"]{border:1px solid #25364d;border-radius:12px}
hr{border-color:#23344a}
div[data-testid="stSelectbox"],div[data-testid="stMultiSelect"],div[data-testid="stSlider"]{color:#eaf1ff}
.brand{font-size:1.5rem;font-weight:800;letter-spacing:-.06em;color:#f5f8ff}
.brand span{color:#52e0d0}
.eyebrow{font-family:'DM Mono';font-size:.68rem;letter-spacing:.16em;color:#52e0d0;text-transform:uppercase}
.hero{padding:1.2rem 0 .8rem}
.sub{color:#91a0b8;font-size:.9rem}
.pill{display:inline-block;padding:5px 10px;border:1px solid #2a435b;border-radius:30px;color:#52e0d0;font: .68rem 'DM Mono';margin-right:6px}
</style>
""",unsafe_allow_html=True)

@st.cache_data
def load(name):
    p=DATA/name
    if not p.exists(): st.error(f"Data artifact missing: {p}"); st.stop()
    return pd.read_csv(p)

rfm=load("customer_rfm_segments.csv")
daily=load("daily_total_demand.csv")
monthly=load("monthly_sales_summary.csv")
inventory=load("inventory_reorder_recommendations.csv")
churn=load("churn_proxy_features.csv")
daily["InvoiceDate"]=pd.to_datetime(daily["InvoiceDate"],errors="coerce")
monthly["month"]=pd.to_datetime(monthly["month"],errors="coerce")
rfm["LastPurchase"]=pd.to_datetime(rfm["LastPurchase"],errors="coerce")

PAGES=[
("01","Command Center","Executive snapshot and business pulse"),
("02","Revenue Studio","Revenue, volume and invoice trends"),
("03","Product Intelligence","SKU leaders and product concentration"),
("04","Customer Segments","RFM segments and customer value"),
("05","Geo & Market View","Country-level view (data availability check)"),
("06","Seasonality Lab","Monthly patterns and seasonal signals"),
("07","Basket Behavior","Customer purchasing behavior"),
("08","Revenue Quality","Value distribution and concentration"),
("09","Inventory Control","Reorder risk and stock planning"),
("10","Order Operations","Invoice and transaction metrics"),
("11","Forecast Lab","Demand baseline, horizon and scenario"),
("12","Analytics Workbench","Interactive filters and data explorer"),
]
with st.sidebar:
    st.markdown('<div class="brand">RETAIL<span>PULSE</span></div>',unsafe_allow_html=True)
    st.markdown('<div class="eyebrow">INTELLIGENCE SUITE · V 2.0</div>',unsafe_allow_html=True)
    st.divider()
    choice=st.radio("NAVIGATION", [f"{n}  {name}" for n,name,_ in PAGES],label_visibility="collapsed")
    page=PAGES[[f"{n}  {name}" for n,name,_ in PAGES].index(choice)][1]
    st.divider()
    st.markdown("**DATA STATUS**")
    st.caption("● Processed artifacts loaded")
    st.caption(f"Customers · {rfm['Customer ID'].nunique():,}")
    st.caption(f"SKUs · {inventory['StockCode'].nunique():,}")
    st.caption("Prototype analytics · local runtime")
    st.markdown('<span class="pill">STREAMLIT</span><span class="pill">PLOTLY</span>',unsafe_allow_html=True)
    st.markdown('<div style="margin-top:1.1rem;padding:12px 0;border-top:1px solid #203049;color:#91a0b8;font-size:.76rem">DESIGNED & BUILT BY<br><strong style="color:#e9eef8;letter-spacing:.04em">GOVIND SUTHAR</strong></div>',unsafe_allow_html=True)

def header(title,subtitle,tag="RETAIL ANALYTICS"):
    st.markdown(f'<div class="hero"><div class="eyebrow">{tag}</div><h1>{title}</h1><div class="sub">{subtitle}</div></div>',unsafe_allow_html=True)
def metrics(items):
    cols=st.columns(len(items))
    for c,(label,val,delta) in zip(cols,items):
        c.metric(label,val,delta)
def chart(fig,height=370):
    fig.update_layout(template="plotly_dark",paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font=dict(family="Manrope",color="#aebbd0"),margin=dict(l=15,r=15,t=45,b=15),height=height,legend=dict(bgcolor="rgba(0,0,0,0)"))
    fig.update_xaxes(showgrid=False,zeroline=False)
    fig.update_yaxes(gridcolor="#223249",zeroline=False)
    st.plotly_chart(fig,use_container_width=True)
def table(df, height=360):
    st.dataframe(df,use_container_width=True,height=height,hide_index=True)
def money(x): return f"{x:,.0f}"
def monthly_filtered():
    m=monthly.copy()
    if m["month"].notna().any():
        start,end=st.date_input("Period",value=(m["month"].min().date(),m["month"].max().date()),key="period")
        m=m[(m["month"].dt.date>=start)&(m["month"].dt.date<=end)]
    return m

# ── 12 multi-function dashboards ─────────────────────────────────────────────
if page=="Command Center":
    header("Command Center","A premium overview of retail performance, customer value and operational signals.","01 / EXECUTIVE")
    metrics([("NET REVENUE",f"{money(monthly.revenue.sum())}","Across available months"),("CUSTOMER BASE",f"{rfm['Customer ID'].nunique():,}","RFM profiles"),("INVOICE COUNT",f"{monthly.invoices.sum():,.0f}","Aggregated invoices"),("SKU CATALOG",f"{inventory.StockCode.nunique():,}","Products in inventory model")])
    a,b=st.columns([1.55,1])
    with a: chart(px.area(monthly,x="month",y="revenue",title="Revenue trajectory",markers=True))
    with b:
        seg=rfm.Segment.value_counts().reset_index();seg.columns=["Segment","Customers"]
        chart(px.pie(seg,names="Segment",values="Customers",hole=.62,title="Customer portfolio mix"))
    st.subheader("Signal board")
    risk=inventory.sort_values("suggested_order_qty",ascending=False).head(8)
    st.caption("High suggested replenishment quantities — review supplier and lead-time assumptions.")
    table(risk[["StockCode","mean_daily_demand","reorder_point","suggested_order_qty","total_revenue"]])

elif page=="Revenue Studio":
    header("Revenue Studio","Explore revenue velocity, sales volume and invoice activity.","02 / SALES")
    m=monthly_filtered()
    metric=st.selectbox("Primary metric",["revenue","units","invoices","customers"])
    metrics([("TOTAL",f"{m[metric].sum():,.0f}","Selected period"),("MONTHLY AVG",f"{m[metric].mean():,.0f}" if len(m) else "0","Mean per month"),("PEAK MONTH",str(m.loc[m[metric].idxmax(),"InvoiceMonth"]) if len(m) else "—","Top period"),("PERIODS",f"{len(m)}","Months included")])
    chart(px.line(m,x="month",y=metric,markers=True,title=f"{metric.title()} by month"))
    x,y=st.columns(2)
    with x: chart(px.bar(m,x="InvoiceMonth",y="revenue",title="Monthly revenue bars"))
    with y: chart(px.line(daily.tail(180),x="InvoiceDate",y="daily_units",title="Daily unit activity · recent 180 records"))
    table(m.sort_values(metric,ascending=False))

elif page=="Product Intelligence":
    header("Product Intelligence","SKU performance, demand ranking and product concentration.","03 / PRODUCT")
    col=st.selectbox("Rank by",["total_revenue","total_units","mean_daily_demand","suggested_order_qty"])
    n=st.slider("Top products",5,50,20)
    top=inventory.nlargest(n,col)
    metrics([("SKU COUNT",f"{inventory.StockCode.nunique():,}","Catalog"),("TOP SKU",str(top.iloc[0].StockCode),"By selected metric"),("TOP VALUE",f"{top.iloc[0][col]:,.1f}",col),("TOP-N SHARE",f"{top[col].sum()/inventory[col].sum()*100:.1f}%" if inventory[col].sum() else "—","Catalog total")])
    chart(px.bar(top,x="StockCode",y=col,title=f"Top {n} SKUs by {col}"))
    chart(px.scatter(inventory,x="total_units",y="total_revenue",size="suggested_order_qty",hover_data=["StockCode"],title="SKU revenue vs volume"))
    table(top)

elif page=="Customer Segments":
    header("Customer Segments","RFM-powered customer value and segment composition.","04 / CUSTOMER")
    segments=sorted(rfm.Segment.dropna().unique())
    selected=st.multiselect("Segment filter",segments,default=segments)
    f=rfm[rfm.Segment.isin(selected)]
    metrics([("CUSTOMERS",f"{len(f):,}","Filtered"),("AVG MONETARY",f"{f.Monetary.mean():,.0f}","Customer value"),("AVG FREQUENCY",f"{f.Frequency.mean():.2f}","Purchases/profile"),("AVG RECENCY",f"{f.Recency.mean():.1f} days","Days since purchase")])
    a,b=st.columns(2)
    with a: chart(px.bar(f.Segment.value_counts().reset_index(),x="Segment",y="count",title="Segment population"))
    with b: chart(px.scatter(f,x="Frequency",y="Monetary",color="Segment",hover_data=["Customer ID"],title="Frequency vs monetary"))
    chart(px.box(f,x="Segment",y="Recency",color="Segment",title="Recency distribution by segment"))
    table(f.sort_values("Monetary",ascending=False).head(500))

elif page=="Geo & Market View":
    header("Geo & Market View","Market exploration using the aggregated artifacts currently available.","05 / MARKET")
    st.info("The supplied processed summaries do not include a country-level revenue table. This page provides available market/customer slices and clearly flags the geographic data gap.")
    metrics([("MONTHS",f"{len(monthly)}","Monthly summary"),("CUSTOMERS",f"{len(rfm):,}","RFM records"),("REVENUE",f"{monthly.revenue.sum():,.0f}","Total aggregated")])
    chart(px.bar(monthly,x="InvoiceMonth",y="customers",title="Monthly active customer counts"))
    st.subheader("Market dataset readiness")
    table(pd.DataFrame({"Required field":["Country","Revenue by country","Invoice-level geography"],"Status":["Not present in processed artifacts","Not calculated","Raw source required"],"Next step":["Include country from transaction-level data","Group revenue by country","Load cleaned transaction data"]}))

elif page=="Seasonality Lab":
    header("Seasonality Lab","Investigate monthly movement and recurring patterns.","06 / SEASONALITY")
    m=monthly.copy();m["calendar_month"]=m.month.dt.month;m["year"]=m.month.dt.year
    metrics([("MONTHS",f"{len(m)}","Observations"),("AVG MONTHLY REVENUE",f"{m.revenue.mean():,.0f}","Mean"),("REVENUE STD",f"{m.revenue.std():,.0f}","Volatility"),("HIGHEST MONTH",str(m.loc[m.revenue.idxmax(),"InvoiceMonth"]) if len(m) else "—","Revenue peak")])
    chart(px.line(m,x="month",y="revenue",color="year",markers=True,title="Revenue trend by year"))
    season=m.groupby("calendar_month",as_index=False).agg(avg_revenue=("revenue","mean"),avg_units=("units","mean"))
    chart(px.bar(season,x="calendar_month",y="avg_revenue",title="Average revenue by calendar month"))
    chart(px.line(season,x="calendar_month",y="avg_units",markers=True,title="Average units by calendar month"))
    table(season)

elif page=="Basket Behavior":
    header("Basket Behavior","Customer purchase frequency, basket size proxies and product breadth.","07 / BEHAVIOR")
    metrics([("AVG PURCHASES",f"{rfm.Frequency.mean():.2f}","Per customer"),("AVG ORDER VALUE",f"{rfm.AverageOrderValue.mean():,.0f}","RFM-derived"),("AVG UNIQUE PRODUCTS",f"{churn.UniqueProducts.mean():.1f}","Churn feature proxy"),("AVG BASKET UNITS",f"{churn.MeanBasketUnits.mean():,.1f}","Feature estimate")])
    a,b=st.columns(2)
    with a: chart(px.histogram(rfm,x="Frequency",nbins=40,title="Purchase frequency distribution"))
    with b: chart(px.histogram(churn,x="UniqueProducts",nbins=40,title="Unique product breadth"))
    chart(px.scatter(churn,x="Frequency",y="MeanBasketUnits",color="ChurnProxy",hover_data=["Customer ID"],title="Frequency vs basket units proxy"))
    table(churn.sort_values("Monetary",ascending=False).head(400))

elif page=="Revenue Quality":
    header("Revenue Quality","Customer value distribution, concentration and revenue indicators.","08 / QUALITY")
    f=rfm.sort_values("Monetary",ascending=False).copy()
    f["cumulative_revenue_share"]=f.Monetary.cumsum()/f.Monetary.sum()
    f["customer_share"]=np.arange(1,len(f)+1)/max(len(f),1)
    metrics([("CUSTOMER VALUE SUM",f"{f.Monetary.sum():,.0f}","RFM monetary sum"),("MEDIAN VALUE",f"{f.Monetary.median():,.0f}","Customer median"),("TOP 10% SHARE",f"{f.head(max(1,int(len(f)*.1))).Monetary.sum()/f.Monetary.sum()*100:.1f}%","Revenue concentration"),("VALUE CV",f"{f.Monetary.std()/f.Monetary.mean():.2f}" if f.Monetary.mean() else "—","Dispersion ratio")])
    chart(px.line(f,x="customer_share",y="cumulative_revenue_share",title="Customer revenue concentration curve"))
    chart(px.histogram(f,x="Monetary",nbins=50,title="Monetary value distribution"))
    chart(px.box(f,y="AverageOrderValue",title="Average order value spread"))
    table(f.head(500))

elif page=="Inventory Control":
    header("Inventory Control","Replenishment signals and demand-risk exploration.","09 / INVENTORY")
    sort=st.selectbox("Sort inventory by",["suggested_order_qty","reorder_point","mean_daily_demand","total_revenue"])
    n=st.slider("Records",100,2000,500,100)
    metrics([("SKU COUNT",f"{len(inventory):,}","Items"),("ORDER QTY SUM",f"{inventory.suggested_order_qty.sum():,.0f}","Suggested units"),("HIGH REORDER POINT",f"{inventory.reorder_point.max():,.1f}","Maximum"),("MEAN DAILY DEMAND",f"{inventory.mean_daily_demand.mean():,.2f}","Across SKUs")])
    a,b=st.columns(2)
    with a: chart(px.scatter(inventory,x="mean_daily_demand",y="reorder_point",size="suggested_order_qty",hover_data=["StockCode"],title="Demand vs reorder threshold"))
    with b: chart(px.histogram(inventory,x="suggested_order_qty",nbins=45,title="Suggested order distribution"))
    table(inventory.sort_values(sort,ascending=False).head(n))
    st.warning("Planning estimates are assumption-based. Validate on-hand stock, lead time, service level, MOQ and supplier constraints.")

elif page=="Order Operations":
    header("Order Operations","Monthly invoice activity, customer activity and operational throughput.","10 / OPERATIONS")
    m=monthly_filtered()
    metrics([("INVOICES",f"{m.invoices.sum():,.0f}","Selected period"),("AVG INVOICES/MONTH",f"{m.invoices.mean():,.0f}" if len(m) else "—","Throughput"),("CUSTOMER-MONTHS",f"{m.customers.sum():,.0f}","Aggregated"),("UNITS",f"{m.units.sum():,.0f}","Selected period")])
    chart(px.bar(m,x="InvoiceMonth",y="invoices",title="Invoice volume by month"))
    a,b=st.columns(2)
    with a: chart(px.scatter(m,x="invoices",y="revenue",size="units",hover_data=["InvoiceMonth"],title="Invoice count vs revenue"))
    with b: chart(px.line(m,x="month",y="customers",markers=True,title="Monthly customers"))
    table(m)

elif page=="Forecast Lab":
    header("Forecast Lab","Adjust a transparent demand baseline and explore scenarios.","11 / FORECAST")
    horizon=st.slider("Forecast horizon (days)",7,120,30)
    window=st.slider("Moving average window (days)",3,30,7)
    multiplier=st.slider("Scenario multiplier",0.50,1.50,1.00,0.05)
    d=daily.dropna(subset=["InvoiceDate"]).sort_values("InvoiceDate")
    avg=float(d.daily_units.tail(window).mean()) if len(d)>=window else float(d.daily_units.mean())
    dates=pd.date_range(d.InvoiceDate.max()+pd.Timedelta(days=1),periods=horizon,freq="D")
    fc=pd.DataFrame({"InvoiceDate":dates,"Forecast units":avg*multiplier})
    metrics([("BASELINE / DAY",f"{avg:,.1f}","Trailing window"),("SCENARIO / DAY",f"{avg*multiplier:,.1f}",f"{multiplier:.2f}× baseline"),("HORIZON TOTAL",f"{fc['Forecast units'].sum():,.0f}","Projected units"),("WINDOW",f"{window} days","Smoothing window")])
    hist=d.tail(120).rename(columns={"daily_units":"Observed units"})
    fig=go.Figure();fig.add_trace(go.Scatter(x=hist.InvoiceDate,y=hist["Observed units"],name="Observed",mode="lines"));fig.add_trace(go.Scatter(x=fc.InvoiceDate,y=fc["Forecast units"],name="Scenario baseline",mode="lines",line=dict(dash="dash")))
    chart(fig)
    chart(px.histogram(d.tail(180),x="daily_units",nbins=40,title="Recent daily demand distribution"))
    table(fc)
    st.warning("This is a moving-average baseline, not a validated ML forecast. Backtest and consider holidays, promotions, returns and stock constraints.")

else:
    header("Analytics Workbench","Choose a dataset, search records and inspect numeric summaries.","12 / WORKBENCH")
    dataset=st.selectbox("Dataset",["Monthly sales","Daily demand","RFM customers","Inventory recommendations","Churn proxy features"])
    mapping={"Monthly sales":monthly,"Daily demand":daily,"RFM customers":rfm,"Inventory recommendations":inventory,"Churn proxy features":churn}
    df=mapping[dataset].copy()
    query=st.text_input("Search all visible fields",placeholder="Type a customer ID, SKU, segment, date…")
    if query:
        mask=df.astype(str).apply(lambda s:s.str.contains(query,case=False,na=False)).any(axis=1);df=df[mask]
    numeric=df.select_dtypes(include=np.number).columns.tolist()
    selected_num=st.multiselect("Numeric columns for summary",numeric,default=numeric[:min(4,len(numeric))])
    metrics([("ROWS",f"{len(df):,}","Filtered records"),("COLUMNS",f"{df.shape[1]}","Fields"),("NUMERIC FIELDS",f"{len(numeric)}","Available"),("MISSING CELLS",f"{int(df.isna().sum().sum()):,}","Current view")])
    table(df,500)
    if selected_num: st.subheader("Descriptive statistics");table(df[selected_num].describe().T.reset_index().rename(columns={"index":"Feature"}))
    st.download_button("Download filtered CSV",df.to_csv(index=False).encode("utf-8"),file_name="retailpulse_filtered_export.csv",mime="text/csv")

st.divider()
st.markdown('<div style="text-align:center;padding:16px 0 6px;color:#91a0b8;font-size:.78rem;letter-spacing:.04em">RETAILPULSE · RETAIL INTELLIGENCE INTERFACE<br><span style="color:#52e0d0">DESIGNED & BUILT BY GOVIND SUTHAR</span><br><span style="font-size:.68rem">ANALYTICAL PROTOTYPE · VALIDATE DERIVED PROXIES AND ASSUMPTIONS BEFORE BUSINESS DECISIONS</span></div>',unsafe_allow_html=True)
