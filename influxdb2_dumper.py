import argparse
import os
import csv
from datetime import datetime, timedelta
from influxdb_client import InfluxDBClient

# -------------------------------
# HARD-CODED InfluxDB 2.x settings
# -------------------------------
ORG = "myorg"
BUCKET = "mybucket"
TOKEN = "mytoken"
HOST = "myhost"
PORT = 0000

URL = f"http://{HOST}:{PORT}"

# -------------------------------
# Argument parsing
# -------------------------------
parser = argparse.ArgumentParser()
parser.add_argument("-tl", "--timelength", help="Length of time for dump (ignored if --start is set)", default="1h", nargs='?')
parser.add_argument("-et", "--endtime", help="End time for dump (ignored if --end is set)", default='now()', nargs='?')
parser.add_argument("--start", help="Start time for dump (overrides timelength if set)", default=None, nargs='?')
parser.add_argument("--end", help="End time for dump (overrides -et if set)", default=None, nargs='?')
args = parser.parse_args()

# -------------------------------
# Determine time range
# -------------------------------
end_time = args.end if args.end else args.endtime
start_time = args.start

# If user gave timelength & endtime instead of start
if not start_time:
    if end_time == 'now()':
        end_dt = datetime.utcnow()
    else:
        end_dt = datetime.fromisoformat(end_time.replace("Z", ""))
    length_num = int(args.timelength[:-1])
    length_unit = args.timelength[-1]
    if length_unit == "h":
        delta = timedelta(hours=length_num)
    elif length_unit == "d":
        delta = timedelta(days=length_num)
    elif length_unit == "m":
        delta = timedelta(minutes=length_num)
    else:
        raise ValueError("Unsupported time unit. Use h, d, or m.")
    start_dt = end_dt - delta
    start_time = start_dt.isoformat() + "Z"
    end_time = end_dt.isoformat() + "Z"

print(f"Querying from {start_time} to {end_time}")

# -------------------------------
# Devices of interest
# -------------------------------
VACUUM_DEVICES = ["GJ_E1","GJ_E2","GJ_E3","GJ_E4","GJ_S1","GJ_S2","GJ_S3","GJ_S4"]
TEMP_DEVICES = ["GJ_ColdheadT1", "GJ_ColdheadT2"]

# -------------------------------
# Read/export logic
# -------------------------------
with InfluxDBClient(url=URL, token=TOKEN, org=ORG) as client:
    query_api = client.query_api()

    # ----- Vacuum -----
    print("Exporting measurement: vacuum")
    flux_query = f'''
    from(bucket: "{BUCKET}")
      |> range(start: {start_time}, stop: {end_time})
      |> filter(fn: (r) => r._measurement == "vacuum")
    '''
    tables = query_api.query(flux_query)
    data = {}
    for table in tables:
        for record in table.records:
            dev_name = record.values.get("dev")
            if dev_name not in VACUUM_DEVICES:
                continue
            ts = record.get_time().isoformat()
            val = record.get_value()
            if ts not in data:
                data[ts] = {}
            data[ts][dev_name] = val
    filename = "report_csv/vacuum.csv"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["time"] + VACUUM_DEVICES)
        writer.writeheader()
        for ts in sorted(data.keys()):
            row = {"time": ts}
            for d in VACUUM_DEVICES:
                row[d] = data[ts].get(d, "")
            writer.writerow(row)

    # ----- Temperature -----
    print("Exporting measurement: temperature")
    flux_query = f'''
    from(bucket: "{BUCKET}")
      |> range(start: {start_time}, stop: {end_time})
      |> filter(fn: (r) => r._measurement == "temperature")
    '''
    tables = query_api.query(flux_query)
    data = {}
    for table in tables:
        for record in table.records:
            dev_name = record.values.get("dev")
            if dev_name not in TEMP_DEVICES:
                continue
            ts = record.get_time().isoformat()
            val = record.get_value()
            if ts not in data:
                data[ts] = {}
            data[ts][dev_name] = val
    filename = "report_csv/temperature.csv"
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["time"] + TEMP_DEVICES)
        writer.writeheader()
        for ts in sorted(data.keys()):
            row = {"time": ts}
            for d in TEMP_DEVICES:
                row[d] = data[ts].get(d, "")
            writer.writerow(row)

    # ----- Pressure -----
    print("Exporting measurement: pressure")
    flux_query = f'''
    from(bucket: "{BUCKET}")
      |> range(start: {start_time}, stop: {end_time})
      |> filter(fn: (r) => r._measurement == "pressure")
    '''
    tables = query_api.query(flux_query)
    filename = "report_csv/pressure.csv"
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["time","value"])
        writer.writeheader()
        for table in tables:
            for record in table.records:
                ts = record.get_time().isoformat()
                val = record.get_value()
                writer.writerow({"time": ts, "value": val})

     # ----- Density -----
    print("Exporting measurement: density")
    flux_query = f'''
    from(bucket: "{BUCKET}")
      |> range(start: {start_time}, stop: {end_time})
      |> filter(fn: (r) => r._measurement == "density")
    '''
    tables = query_api.query(flux_query)

    data = {}
    for table in tables:
        for record in table.records:
            ts = record.get_time().isoformat()
            field = record.get_field()
            val = record.get_value()
            if ts not in data:
                data[ts] = {}
            if field == "species":
                data[ts]["species"] = val
            else:
                # assume this is the numeric density
                data[ts]["value"] = val

    filename = "report_csv/density.csv"
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["time","value","species"])
        writer.writeheader()
        for ts in sorted(data.keys()):
            row = {"time": ts,
                   "value": data[ts].get("value",""),
                   "species": data[ts].get("species","")}
            writer.writerow(row)

print("Export complete.")