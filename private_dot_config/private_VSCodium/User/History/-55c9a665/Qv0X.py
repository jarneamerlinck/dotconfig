import datetime
import logging
import os
import time

import click
import pandas as pd

from pyiotdataflow.airtable import (
    add_metadata,
    sensor,
    sensor_placement_deployment_metadata,
)
from pyiotdataflow.connection import dbase_engine
from pyiotdataflow.geoluxserver import get_geolux_data
from pyiotdataflow.load import exclude_duplicate, merge_ids
from pyiotdataflow.metadata import update_metadata

logger = logging.getLogger(__name__)

API_KEY = os.environ.get("AIRTABLE_API_KEY")
BASE_ID = "appnRGoJcIqoyua6I"  # airtable unique base identifier


@click.command()
@click.option("--delta_hours", type=int, default=2)
def upload_geolux(delta_hours):
    """Download data via geolux api and upload to dbase.

    Parameters
    ----------
    delta_hours : int
        Hours back from now to request data from
    """

    # 1a check the airtable API for the smartdatalogger devices to get ID
    sensors = sensor(API_KEY, BASE_ID)
    sensor_ids = sensors[sensors["device_type"] == "smartdatalogger"][
        "sensor_id"
    ].values
    # 1b prepare the time sequence to resuest data
    d_start = datetime.datetime.now() - datetime.timedelta(hours=delta_hours)
    d_end = datetime.datetime.now()

    # 2. for each of the devices call `get_geolux_data`
    res = []
    for sensor_id in sensor_ids:
        try:
            df = get_geolux_data(sensor_id, d_start, d_end)
            res.append(df)
        except Exception as exc:
            logger.error(f"Geolux data request error - {exc}")
    df_data = pd.concat(res)
    df_data = df_data.sort_values(by="time")

    # 3. Add metadata,... analogue to mqtt/ftp and push to dbase.
    # Load metadata database
    click.echo("Check existing sensor metadata...")
    try:
        deployment_sensor_location_metadata = sensor_placement_deployment_metadata(
            API_KEY, BASE_ID
        )
    except Exception as exc:
        logger.error(f"Airtable metadata handling error - {exc}")
        raise

    # combine data and metadata
    df_data_merged = add_metadata(df_data, deployment_sensor_location_metadata)
    df_data_merged = df_data_merged.rename(columns={"location_id": "site_name"}).drop(
        columns=["sensor_id"]
    )

    # dropna replaces the `exclude_without_metadata`
    df_data_merged = df_data_merged.dropna()
    df_data_merged = df_data_merged.drop_duplicates()

    # make metadata compatible to previous version of the database metadata upload
    metadata_db = deployment_sensor_location_metadata[
        [
            "location_id",
            "easting",
            "northing",
            "sensor_id",
            "variable_name",
            "variable_unit",
            "manufacturer",
        ]
    ].rename(
        columns={
            "location_id": "site_name",
            "sensor_id": "sensor_name",
            "variable_unit": "unit",
            "manufacturer": "comment",
        }
    )

    # create dbase engine
    db = dbase_engine()

    with db.connect() as connection:
        click.echo("Update metadata in database...")
        # Any new sensors defined in metadata, register in dbase
        update_metadata(metadata_db.copy(), connection)

        # Load the appropriate identifiers for each new data point
        click.echo("Assign appropriate identifiers to data...")
        df_data_ids = merge_ids(df_data_merged, connection)

        # Exclude earlier uploaded data points from table
        click.echo("Cut data on last uploaded data point per sensor")
        df_data_ids = exclude_duplicate(df_data_ids, connection)

        # Upload to database
        click.echo(f"Uploading new data with {df_data_ids.shape[0]} records...")
        # Assign explicit UTC so Pandas uses correct Timezone for to_sql
        df_data_ids["time"] = df_data_ids["time"].dt.tz_localize("UTC")
        df = df_data_ids[["time", "value", "site_id", "variable_id", "sensor_id"]]
        #df.to_sql(name="measurement", con=connection, if_exists="append", index=False)
        click.echo("New geolux data uploads")


if __name__ == "__main__":
    upload_geolux()
