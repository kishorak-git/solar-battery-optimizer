# Solar Battery Optimizer

A Streamlit simulation that applies a simple hourly solar, battery, and grid-balancing model to fixed example profiles.

## How it works

The app evaluates 24 hourly periods using a fixed array of simulated solar generation values and a fixed array of simulated demand values.

For each hour:

1. It subtracts demand from solar generation.
2. If generation exceeds demand, it charges the battery with the remaining energy, up to the battery capacity.
3. If demand exceeds generation, it discharges the battery to meet as much demand as possible.
4. It records any unmet demand as grid use.
5. It records the battery state of charge and action for that hour.

The app also calculates an illustrative SOH estimate from completed charge cycles using:

```text
SOH = max(100 - (cycles / 60), 55)
```

Temperature and battery charge thresholds are used to display warnings and one of three text recommendations.

## Inputs

The sidebar accepts:

- Battery capacity in kWh: 50–500 kWh, default 200 kWh
- Initial state of charge in percent: 10–100%, default 60%
- Battery temperature in °C: 20–60°C, default 32°C
- Completed charge cycles: 0–5000, default 1200

Solar generation and demand are fixed inside `app.py`; they are not loaded from a file or sensor feed.

## Outputs

The dashboard displays:

- Final simulated battery state of charge
- Illustrative state-of-health percentage
- Total recorded grid use across the 24-hour model
- Temperature
- Temperature, deep-discharge, and health alerts
- A Solar vs Demand chart
- A Battery State of Charge chart
- A maintenance, cooling, or operating recommendation

## Run locally

Python 3 with `pip` is required.

```powershell
git clone https://github.com/kishorak-git/solar-battery-optimizer.git
cd solar-battery-optimizer
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Open the local URL printed by Streamlit, normally `http://localhost:8501`.

## Example output

With the default inputs (200 kWh capacity, 60% initial SOC, 32°C, and 1200 completed cycles), the fixed profiles produce:

```text
Final SOC: 0.0 kWh
SOH: 80.0%
Grid use: 362.0 kWh
Minimum recorded SOC: 0.0 kWh
```

Hourly actions are 7 charging hours, 9 discharging hours, and 8 grid-supply hours.

## Limitations

- This is a simulation using hard-coded solar and demand arrays, not measured or real-time data.
- It has not been validated against real batteries, real solar installations, or real operating data.
- The charge, discharge, SOH, temperature, tariff, and recommendation logic is illustrative and should not be treated as engineering sizing, safety, or financial advice.
- No real deployment, hardware integration, energy savings, accuracy, or cost savings are claimed.
- The app does not read IoT sensors, write to a database, or control charging hardware.
