# Experimental Utilities Toolkit

![Python](https://img.shields.io/badge/python-3.x-blue)

A collection of **Python utilities used in experimental physics workflows**, including:

- Time-series **data export from InfluxDB**
- **Vacuum system calculations**
- **Beamline / skimmer geometry tools**

These scripts were developed to support **laboratory data analysis and vacuum system design**.

---

# Repository Overview

| Script | Purpose | Interface |
|------|------|------|
| **`influxdb2_dumper.py`** | Export time-series data from InfluxDB to CSV reports | CLI |
| `skimmers.py` | Solve skimmer geometry parameters | GUI |
| `expected_delta_p.py` | Compute expected pressure rise Δp | GUI |
| `nozzle_diameter.py` | Solve for nozzle diameter | GUI |

---

# Main Utility: InfluxDB Data Exporter

## `influxdb2_dumper.py`

This is the **primary script of the repository**.

It exports **time-series data from an InfluxDB 2.x instance** into structured **CSV reports** suitable for:

- Python analysis
- MATLAB processing
- Excel inspection
- long-term archiving

Each measurement type is exported into a **separate CSV file**.

---

## Exported Data

| Measurement | Description | Output File |
|-------------|-------------|-------------|
| Vacuum gauges | Selected vacuum gauge devices | `report_csv/vacuum.csv` |
| Temperature sensors | Coldhead temperature sensors | `report_csv/temperature.csv` |
| Pressure | Scalar pressure readings | `report_csv/pressure.csv` |
| Density | Density values + species labels | `report_csv/density.csv` |

---

## Time Selection

The query time window can be controlled via command-line arguments.

| Argument | Description | Default |
|--------|--------|--------|
| `--timelength` | Time range length (`h`, `d`, `m`) | `1h` |
| `--endtime` | Query end time | `now()` |
| `--start` | Explicit start time (ISO8601) | — |
| `--end` | Explicit end time (ISO8601) | — |

If `--start` and `--end` are provided, they **override** `--timelength` and `--endtime`.

---

## Example Usage

Export the **last two days of data**:

```bash
python influxdb2_dumper.py --timelength 2d
```

Export a **specific time window**:

```bash
python influxdb2_dumper.py \
--start 2025-09-01T00:00:00Z \
--end   2025-09-01T12:00:00Z
```

---

## Workflow

The script performs the following steps:

```
InfluxDB → Query measurements → Align time series → Export CSV reports
```

Output files are written to:

```
report_csv/
```

---

# Scientific Calculators

The following scripts are **small GUI tools** used for vacuum system design and beamline calculations.

---

# Skimmer Geometry Calculator

`skimmers.py`

A **minimal GUI calculator** that determines missing **skimmer geometry parameters** using **symbolic solving with SymPy**.

### Variables

```
s1   s2   dx   d12   l1   l2
```

Internal variable:

```
h
```

All results are reported in **mm**.

### Usage

1. Enter any known variables  
2. Leave unknown fields blank  
3. Press **Calculate** or **Enter**

The solver returns only **physically valid (positive) solutions**.

---

# Expected Pressure Rise Calculator

`expected_delta_p.py`

Computes the **pressure rise Δp** for up to **four inlet pressures simultaneously**.

### Fixed Parameters

```
k
R_s
T_0
T
c
S
d0 (μm)
```

### Variable Inputs

```
p0_1
p0_2
p0_3
p0_4
```

### Output

```
Δp (mbar)
```

### Usage

1. Enter fixed parameters  
2. Enter one or more inlet pressures  
3. Press **Calculate**

---

# Nozzle Diameter Solver

`nozzle_diameter.py`

Computes the **nozzle diameter d₀** for up to **four pumping speeds simultaneously**.

### Fixed Parameters

```
k
R_s
T_0
T
c
Δp (mbar)
p_0 (bar)
```

### Variable Inputs

```
S1
S2
S3
S4
```

### Output

```
d₀ (μm)
```

---

# Units and Notes

| Script | Important Units |
|------|------|
| `skimmers.py` | Results in **mm** |
| `expected_delta_p.py` | `d0` in **μm**, output **Δp in mbar** |
| `nozzle_diameter.py` | `Δp` in **mbar**, `p₀` in **bar**, output **d₀ in μm** |

The scripts

```
expected_delta_p.py
nozzle_diameter.py
```

accept **mathematical expressions** such as:

```
2e-3
pi/4
```

which are evaluated automatically.

---

# Dependencies

Typical dependencies include:

```
python
sympy
tkinter
influxdb-client
```
