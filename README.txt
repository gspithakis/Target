## 1) Skimmer Calculator (`skimmers.py`)

A minimal GUI that calculates **skimmer geometry parameters** from whatever inputs you have, and fills in the missing ones. It uses **Sympy** to solve a small system and shows only physically valid (positive) results, formatted with subscripts.

**Variables**
- `s1`, `s2`, `dx`, `d12`, `l1`, `l2` (internally also `h`)
- Results are displayed in **mm**.

**Usage**
- Enter any subset of the variables; leave blanks for unknowns.
- Click **Calculate** (or press **Enter**) to fill in missing values.
- Click **Clear** to reset inputs.

---

## 2) Expected Δp Calculator (`expected_delta_p.py`)

Computes the **pressure rise Δp** for up to four different inlet pressures `p₀` simultaneously. Results are reported in **mbar**.

**Inputs**
- Fixed parameters: `k`, `R_s`, `T_0`, `T`, `c`, `S`, `d0` (enter **d0 in μm**).
- Multiple inlet pressures: `p0_1`, `p0_2`, `p0_3`, `p0_4`.

**Usage**
- Fill in the fixed parameters once, then any subset of the `p0_*` inputs.
- Click **Calculate** (or press **Enter**) to see Δp for each provided `p₀`.
- Click **Clear** to reset.

---

## 3) Nozzle Diameter Calculator (`nozzle_diameter.py`)

Solves for the **nozzle diameter `d₀`** (in **μm**) for up to four different pumping speeds `S` in parallel.

**Inputs**
- Fixed parameters: `k`, `R_s`, `T_0`, `T`, `c`, `Δp` (mbar), `p_0` (bar).
- Multiple speeds: `S1`, `S2`, `S3`, `S4`.

**Usage**
- Fill in the fixed parameters once, then any subset of `S1…S4`.
- Click **Calculate** (or press **Enter**) to see `d₀` for each provided `S`.
- Click **Clear** to reset.

---

## Notes

- **Units matter:**  
  - `skimmers.py` displays results in mm.  
  - `expected_delta_p.py` expects `d0` in μm; outputs Δp in mbar.  
  - `nozzle_diameter.py` expects `Δp` in mbar and `p₀` in bar; outputs `d₀` in μm.
  - `expected_delta_p.py` and `nozzle_diameter.py` accept expressions (e.g., `2e-3`, `pi/4`).

