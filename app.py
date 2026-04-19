import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Smart Battery System", layout="wide")

st.title("🔋 Smart Battery Monitoring & Optimization System")
st.write("Submitted by Kishor AK")

# Sidebar
st.sidebar.header("System Inputs")

battery_capacity = st.sidebar.slider("Battery Capacity (kWh)", 50, 500, 200)
soc_percent = st.sidebar.slider("Initial State of Charge (%)", 10, 100, 60)
temperature = st.sidebar.slider("Battery Temperature (°C)", 20, 60, 32)
cycles = st.sidebar.slider("Charge Cycles Completed", 0, 5000, 1200)

hours = np.arange(24)

solar = np.array([0,0,0,0,5,15,30,45,60,75,85,95,100,95,80,60,40,20,10,0,0,0,0,0])
demand = np.array([30,28,26,25,24,30,40,50,55,60,65,70,75,72,68,66,70,80,85,78,65,55,45,35])

soc = soc_percent / 100 * battery_capacity
soc_log = []
grid_use = []
action = []

for i in range(24):
    net = solar[i] - demand[i]

    if net > 0:
        charge = min(net, battery_capacity - soc)
        soc += charge
        grid = 0
        act = "Charging"
    else:
        need = abs(net)
        discharge = min(need, soc)
        soc -= discharge
        grid = need - discharge
        act = "Discharging" if discharge > 0 else "Grid Supply"

    soc_log.append(soc)
    grid_use.append(grid)
    action.append(act)

# Health model
health = max(100 - (cycles / 60), 55)

# Alerts
alerts = []
if temperature > 45:
    alerts.append("⚠ High Temperature Risk")
if min(soc_log) < 20:
    alerts.append("⚠ Deep Discharge Detected")
if health < 70:
    alerts.append("⚠ Battery Health Degrading")

# Metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("SOC", f"{soc_log[-1]:.1f} kWh")
col2.metric("SOH", f"{health:.1f}%")
col3.metric("Grid Use", f"{sum(grid_use):.1f} kWh")
col4.metric("Temperature", f"{temperature} °C")

# Alerts
st.subheader("System Alerts")
if alerts:
    for a in alerts:
        st.warning(a)
else:
    st.success("All systems operating normally")

# Charts
df = pd.DataFrame({
    "Hour": hours,
    "Solar": solar,
    "Demand": demand,
    "Battery_SOC": soc_log
})

col5, col6 = st.columns(2)

with col5:
    fig, ax = plt.subplots()
    ax.plot(df["Hour"], df["Solar"], label="Solar")
    ax.plot(df["Hour"], df["Demand"], label="Demand")
    ax.legend()
    ax.set_title("Solar Generation vs Demand")
    st.pyplot(fig)

with col6:
    fig2, ax2 = plt.subplots()
    ax2.plot(df["Hour"], df["Battery_SOC"])
    ax2.set_title("Battery State of Charge")
    st.pyplot(fig2)

# Recommendation
st.subheader("AI Recommendation")
if health < 70:
    st.info("Schedule battery maintenance / replacement planning.")
elif temperature > 40:
    st.info("Activate cooling system and reduce charging rate.")
else:
    st.info("Battery operating efficiently. Use peak tariff discharge mode.")
