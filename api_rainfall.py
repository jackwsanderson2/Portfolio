import requests
import json
import polars as pl
import time
from time import perf_counter
from datetime import datetime, timezone

# global variables
load_id = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H_%M_%S.%fZ")
url = 'http://environment.data.gov.uk/flood-monitoring/id/stations?parameter=rainfall'

# functions
def api_connection(url):
    """
    Connects to the API and returns the data as a JSON object.
    """
    print("Connecting to API...")

    if response_Status := requests.get(url).status_code != 200:
        print(f"API connection failed with status code: {response_Status}")
        return None
    
    else:
        print("API connection successful.")
        response = requests.get(url)
        data = response.json()
        return data


def save_raw_data(data):
    """
    Saves the raw data to a JSON file and tracks the processing time.
    """

    print("Saving raw data...")

    # local variables
    start = perf_counter()
    filename = f"rainfall_raw_data_{load_id}.json"

    try:
        with open(filename, "w") as f:
            json.dump(data, f)
        print(f"Raw data saved to {filename}")
        print(f"Raw data saved in {perf_counter() - start:.3f} s")

    except Exception as e:
        print(f"Raw data not saved: {e}")
        return

def save_conformed_data(data):
    """
    Saves the conformed data to csv file using polars python library and tracks the processing time.
    """

    print("Saving conformed data...")

    # local variables
    start = perf_counter()
    df = pl.DataFrame(data["items"])
    filename = f"rainfall_conformed_data_{load_id}.csv"

    try:
        df_flat = (df.explode("measures").with_columns(pl.col("measures").struct.rename_fields([
            "measure_id",
            "parameter",
            "parameterName",
            "period",
            "qualifier",
            "unitName"
            ]))).unnest("measures")
        
        df_flat.write_csv(filename)
        print(f"Conformed data saved to {filename}")
        print(f"Conformed data saved in {perf_counter() - start:.3f} s")

    except Exception as e:
        print(f"Conformed data not saved.: {e}")
        return
        

def save_reporting_view(data):
    """
    Connects to the API, retrieves the data, and creates a reporting view using Polars.
    """
    print("Creating reporting view...")

    # local variables
    start = perf_counter()
    df = pl.DataFrame(data["items"])
    lf = pl.LazyFrame(df)
    filename = f"rainfall_reporting_view_{load_id}.csv"

    try:
        lf_flat = lf.group_by("measures").agg([
                    pl.col("measures").struct.rename_fields([
                        "measure_id",
                        "parameter",
                        "parameterName",
                        "period",
                        "qualifier",
                        "unitName"
                    ]).unnest().alias("measures")
                ]).collect()
        
        pl.DataFrame(lf_flat).write_csv(filename)

        print(f"Reporting view saved to {filename}")
        print(f"Reporting view saved in {perf_counter() - start:.3f} s")

        print("UNOPTIMIZED")
        print(lf_flat.explain(optimized=False))
        print("\nOPTIMIZED")
        print(lf_flat.explain(optimized=True))

    except Exception as e:
        print(f"Reporting view not saved: {e}")
        return


# main
if __name__ == "__main__":
    data = api_connection(url)
    save_raw_data(data)
    save_conformed_data(data)
    save_reporting_view(data)
