import datetime
import io
import time

import pandas as pd
import requests
import logging
logger = logging.getLogger(__name__)

"""
Documentation of geolux is only available via email, qoted here

This is the format for the CSV API:
http://www.hydro-view.com/api/v1/data/get?id0=HASHID&start=1657002493&end=1657175293
(with HASHID the hash of a variable time series of a given sensor)

The start and end are UNIX timecode; in the above example I have selected the start
2 days ago, and end timestamp was some 30 minuted ago.
id0 is not the site id, but the measurement ID. The API does not return an error, but
just an empty document will be returned if id0 is incorrect.

You can request more than one data column, by adding more id parameters:
id0, id1, id2 etc, like in this example:
http://www.hydro-view.com/api/v1/data/get?id0=HASHID0&id1=HASHID1&
start=1657002493&end=1657175293

When using more columns, always check the header row because the API can rearrange the
columns order. But in the header (first) row, you will see the measurement ID for the
associated column. When more columns are requested, there can also be empty elements
with no data, just link in the example which I ave you. When parsing the data,
you must take this into account. This happens when for example one instrument connected
to the datalogger was not able to send the data at a given timestamp, but the data for
the other requested column, did deliver the data for that timestamp.
"""


GEOLUX_TS_IDS = {
    "iot_waterquantity_geolux_smartdatalogger_0001": {
        "surface_velocity": "H7hRBnw9uVvvJCTYgXsFm4uTQgc4rhwQatPso8GAGzAs-"
        "4QuZcvBqiJaXvj1aFq98YDcknYocmU7iBqhrPYgEtRAC",
        "average_surface_velocity": "H7hRBnw9uVvvJCTYgXsFm4uTQgc4rhwQatPso8GAGzAs-"
        "CGNbNF6qjZVadzbo6rNWzSCQaZ82rf5R5FMT5jVgYuQk",
        "tilt_angle": "H7hRBnw9uVvvJCTYgXsFm4uTQgc4rhwQatPso8GAGzAs-"
        "5R3umPJrKtkXrxJYdaTXagsnLmDPA1CrJSDTbdCjk534",
        "flow_direction": "H7hRBnw9uVvvJCTYgXsFm4uTQgc4rhwQatPso8GAGzAs-"
        "39qHVRoS4zazVAs8n3gFT5rmGCojcaC1CMtnKuXRHh7H",
        "signal_noise_ratio": "H7hRBnw9uVvvJCTYgXsFm4uTQgc4rhwQatPso8GAGzAs-4"
        "fsGmiTQotHLavJf2mYmihyxVnZRpS3RpqTUwgDQybhz",
        "discharge": "H7hRBnw9uVvvJCTYgXsFm4uTQgc4rhwQatPso8GAGzAs-"
        "AgNJ4a4rybxA5sc8dJMH1eYgRWttRS9ACjfiSzDA2B4x",
        "distance": "H7hRBnw9uVvvJCTYgXsFm4uTQgc4rhwQatPso8GAGzAs-"
        "8pEo9aLTcR9tycG2dwZn7XrXKzyNd76tF7xBwGL39ZaV",
        "water_level": "H7hRBnw9uVvvJCTYgXsFm4uTQgc4rhwQatPso8GAGzAs-"
        "E39kXtrp558aMDq4sovHnpudqgwd1gMsjjHaDZpjxbac",
        "temperature_device": "H7hRBnw9uVvvJCTYgXsFm4uTQgc4rhwQatPso8GAGzAs-"
        "DiUBcdDNi2H4z2f5HK3vxAj6bGbP4rygHfA7Z93VrnXW",
        "relative_humidity_device": "H7hRBnw9uVvvJCTYgXsFm4uTQgc4rhwQatPso8GAGzAs-"
        "FVxC8Qo6z4pvDieKHTtZULoaHweX2Jc96M7vv8vyguU8",
        "battery": "H7hRBnw9uVvvJCTYgXsFm4uTQgc4rhwQatPso8GAGzAs-"
        "GejuCHTA5A1oLXmyyetKi4tu5fPY7FkTwvLuJfWoGLaT",
        "voltage_input": "H7hRBnw9uVvvJCTYgXsFm4uTQgc4rhwQatPso8GAGzAs-"
        "2Pji2SbsiHYRmVcCHEiVDCtvWox8X8wyYUG5P9SVPcQF",
        "battery_charge_current": "H7hRBnw9uVvvJCTYgXsFm4uTQgc4rhwQatPso8GAGzAs-"
        "HbqBb6BEXSMrYtMEtPAtKY3k4ipjxAbZLkdLD2imH1zP",
        "received_signal_strength_indicator_modem": "H7hRBnw9uVvvJCTYgXsFm4uTQgc4r"
        "hwQatPso8GAGzAs-7DapZ6dX8ULNF3h"
        "Z6BknQuWbn6rsPAvGGm757Qkx7Xem",
    },
    "iot_waterquantity_geolux_smartdatalogger_0002": {
        "temperature_device": "CGHszu5D9G3TkXEpr9Gye9wJNGH2tWnT5VmBwCe6ZF47-"
        "8fY1FCS3H7Nu2aYJeTXXCRMMcGMv3p4QRBJfAeiFsbgs",
        "relative_humidity_device": "CGHszu5D9G3TkXEpr9Gye9wJNGH2tWnT5VmBwCe6ZF47-"
        "8dbW7gbrj7BNmpDBJCBxgdYg5BJSq24mRhCd6AVqyqZm",
        "battery": "CGHszu5D9G3TkXEpr9Gye9wJNGH2tWnT5VmBwCe6ZF47-"
        "CcUsoCVzM76M5cFgSiuBu57Z7MmD2VecgV9TJtMEcjNQ",
        "voltage_input": "CGHszu5D9G3TkXEpr9Gye9wJNGH2tWnT5VmBwCe6ZF47-"
        "DijJ6FkGcwGjbSiocBD9UAB24AaV87RCNiq72Dr6zRpB",
        "battery_charge_current": "CGHszu5D9G3TkXEpr9Gye9wJNGH2tWnT5VmBwCe6ZF47-"
        "DGfRV83b11aQhA6WkbpYQe1FZAQxpRH195862XoPULub",
        "received_signal_strength_indicator_modem": "CGHszu5D9G3TkXEpr9Gye9wJNGH2tWnT5"
        "VmBwCe6ZF47-GrLUfqVZL1vzSEBvF8XPt"
        "uPs9y1kfnUK9iGBhxnisJDM",
        "surface_velocity": "CGHszu5D9G3TkXEpr9Gye9wJNGH2tWnT5VmBwCe6ZF47-"
        "CW8MeF1L4bf9mCP8iZNZMLHSBgn4B8Xiw74dheZATG1p",
        "average_surface_velocity": "CGHszu5D9G3TkXEpr9Gye9wJNGH2tWnT5VmBwCe6ZF47-"
        "3BGFA9DqWTvYVpWWG7QRGVCP7GKTrabryJGUccKKi4WU",
        "tilt_angle": "CGHszu5D9G3TkXEpr9Gye9wJNGH2tWnT5VmBwCe6ZF47-"
        "9HnE2ofSF1yqoSUunYKPtPYngyYSV1LsBGoKDfhypmAe",
        "flow_direction": "CGHszu5D9G3TkXEpr9Gye9wJNGH2tWnT5VmBwCe6ZF47-"
        "EyjB8TyocwAEERnn4qbAzzqxACKkz6ve3MoPLz3NcMyG",
        "signal_noise_ratio": "CGHszu5D9G3TkXEpr9Gye9wJNGH2tWnT5VmBwCe6ZF47-"
        "9y6dRKoq1Yt8vAwxC5JdvVjWYoAor32sjpYquqfrboDT",
        "discharge": "CGHszu5D9G3TkXEpr9Gye9wJNGH2tWnT5VmBwCe6ZF47-"
        "8RTdwSRCsESpwW7QQpivKnjycqaxbnjNKk6LDfuSHn4f",
        "distance": "CGHszu5D9G3TkXEpr9Gye9wJNGH2tWnT5VmBwCe6ZF47-"
        "GKd9yxedfQGSFndjfH21xNctQ5wiJYP4vq7PGTWxDMfm",
        "water_level": "CGHszu5D9G3TkXEpr9Gye9wJNGH2tWnT5VmBwCe6ZF47-"
        "8CkY2x6fcTqDkKjHm2wJbRmS1GanUhjN8VFRKgDDvtsm",
    },
    "iot_waterquantity_geolux_smartdatalogger_0003": {
        "temperature_device": "GVdFqmbGV9RtxGzbhFuJUwZXdux42zUe2PZTjf6FoUtv-"
        "9Foekt2RUJ8JpBTFh6xaRbzPAzsD9CPWN6zGKF4WPth2",
        "relative_humidity_device": "GVdFqmbGV9RtxGzbhFuJUwZXdux42zUe2PZTjf6FoUtv-"
        "BcnZwmhZ9PgR14bEEJMTRdSUN6gPuv3ZFAWgjXEme1Ca",
        "battery": "GVdFqmbGV9RtxGzbhFuJUwZXdux42zUe2PZTjf6FoUtv-"
        "CLQL1X1mTCbbJyucaprzoXhkbXyxm9bpkFQqxQxMUWD7",
        "voltage_input": "GVdFqmbGV9RtxGzbhFuJUwZXdux42zUe2PZTjf6FoUtv-"
        "DabgBCGPk5X61z9V1J4BwYoHMFySt78gSnzh5VFcyb6e",
        "battery_charge_current": "GVdFqmbGV9RtxGzbhFuJUwZXdux42zUe2PZTjf6FoUtv-"
        "61hiKV8VTqKejtzw5WG3jZgQHzavrZaZUpUeUd5jJ2ZX",
        "received_signal_strength_indicator_modem": "GVdFqmbGV9RtxGzbhFuJUwZXdux42zUe2"
        "PZTjf6FoUtv-4qQa4sgfubamTqGpnRawsK"
        "MY53FvquACTse73Qed9H5G",
        "surface_velocity": "GVdFqmbGV9RtxGzbhFuJUwZXdux42zUe2PZTjf6FoUtv-"
        "8XPzREpaiMHCfuABLS6WXbFDXBFonUgMjPuxGEygf9xm",
        "average_surface_velocity": "GVdFqmbGV9RtxGzbhFuJUwZXdux42zUe2PZTjf6FoUtv-"
        "47N48GWKKpga75qPsr3A4Db7SkBrmXBAMAD5oRZagvWZ",
        "tilt_angle": "GVdFqmbGV9RtxGzbhFuJUwZXdux42zUe2PZTjf6FoUtv-"
        "4EyEdqFvHpafdi7UaRwuY2YYYp163v11reGNWPhrdXoq",
        "flow_direction": "GVdFqmbGV9RtxGzbhFuJUwZXdux42zUe2PZTjf6FoUtv-"
        "91iisVM8vKYGgfxg5C2kBAYrdYKpXadmWw1FStJuEf6t",
        "signal_noise_ratio": "GVdFqmbGV9RtxGzbhFuJUwZXdux42zUe2PZTjf6FoUtv-"
        "5oLdWwPrPXBDun9mgrKoc3vcGCZLtnD3fYN2TodQmpAG",
        "discharge": "GVdFqmbGV9RtxGzbhFuJUwZXdux42zUe2PZTjf6FoUtv-"
        "4Rcf8VZLyF8eDBkT8WG9YNYDszewyy35AryXryFrMNyr",
        "distance": "GVdFqmbGV9RtxGzbhFuJUwZXdux42zUe2PZTjf6FoUtv-"
        "9AunnjoJCaK2mL5NgYd172iwQ787hgS1j97GEykBAMmw",
        "water_level": "GVdFqmbGV9RtxGzbhFuJUwZXdux42zUe2PZTjf6FoUtv-"
        "5vdE64wRZAKgMpQweYeLgV91c9Ja9n4dprMwoZvB1gQb",
    },
    "iot_waterquantity_geolux_smartdatalogger_0004": {
        "temperature_device": "5LvL1NL8zKc4QHX3p6crutSBGWG19CgUTCnbzJqruANF-"
        "ENAJWkU85WvKpxEAsiePTQA558pEmdJ4YCPzj3vCcYQo",
        "relative_humidity_device": "5LvL1NL8zKc4QHX3p6crutSBGWG19CgUTCnbzJqruANF-"
        "Fgmro5BxW82w85wNavhoq4Xy2BgDKNLxUHEm9Ufkv5PT",
        "battery": "5LvL1NL8zKc4QHX3p6crutSBGWG19CgUTCnbzJqruANF-"
        "AnPLDxnwVf77QJExHEwZnFvA2FS94ShbF4W2R7N2WT1w",
        "voltage_input": "5LvL1NL8zKc4QHX3p6crutSBGWG19CgUTCnbzJqruANF-"
        "7shf4KEr3ZZ33h9z9hA5DGKqedd8CgfdxKPaJoHofin4",
        "battery_charge_current": "5LvL1NL8zKc4QHX3p6crutSBGWG19CgUTCnbzJqruANF-"
        "HWkEiogDyx26Q8TmWhyiMdU8BKYdU4LPW4daCHzVLgP1",
        "received_signal_strength_indicator_modem": "5LvL1NL8zKc4QHX3p6crutSBGWG19Cg"
        "UTCnbzJqruANF-6wvH8Q5MguC5xuPwT"
        "fUNxzTJ4v769dHTY8yeTJCBSnbB",
        "surface_velocity": "5LvL1NL8zKc4QHX3p6crutSBGWG19CgUTCnbzJqruANF-"
        "AG8AEHg6zuR662CAQ72q66fmrmxuJgkcKC7nA8AGYkAw",
        "average_surface_velocity": "5LvL1NL8zKc4QHX3p6crutSBGWG19CgUTCnbzJqruANF-"
        "CNLJhZk3aHVU8wzKJQA4fZqxqp6aYPsfDocUQeb5FSHD",
        "tilt_angle": "5LvL1NL8zKc4QHX3p6crutSBGWG19CgUTCnbzJqruANF-"
        "BNwntKsEij56hGXLNQytjRUwMgKgqv9SnY3sAB4AVk4G",
        "flow_direction": "5LvL1NL8zKc4QHX3p6crutSBGWG19CgUTCnbzJqruANF-"
        "GYrcHFwrpBs4xVruhha8QMPLVRz4mG4KoGYtxbDPNVKR",
        "signal_noise_ratio": "5LvL1NL8zKc4QHX3p6crutSBGWG19CgUTCnbzJqruANF-"
        "BrC9aKQdFCaSJ2Y2eEvni42h48sx4FDYvy5AToy2vcWG",
        "discharge": "5LvL1NL8zKc4QHX3p6crutSBGWG19CgUTCnbzJqruANF-"
        "2qBxcGuuK6aaipoLyGgtY9rQCh4aJeEWygJFnYJRnAvD",
        "distance": "5LvL1NL8zKc4QHX3p6crutSBGWG19CgUTCnbzJqruANF-"
        "5zbLjeF9khQoL6bNCWjwqfwG65U3iudD48HEE1637fGG",
        "water_level": "5LvL1NL8zKc4QHX3p6crutSBGWG19CgUTCnbzJqruANF-"
        "4U9Kfq1J1XRSGUNGbGZqgRsSgnUtohbfBpm5n4kTD9NL",
    },
}

BASE_URL = "http://www.hydro-view.com/api/v1/data/get?"


def get_geolux_data(
    sensor_id, start_timestamp, end_timestamp, ts_id_mapping=GEOLUX_TS_IDS
):
    """Request Geolux data from API

    Parameters
    ----------
    sensor_id : str
        sensor identifier as defined in the IOT metadata (which is the same identifier
        used in the Hydroview platform).
    start_timestamp : datetime.datetime
        Start timestamp to request data from hydroview API (naive UTC).
    end_timestamp :  datetime.datetime
        End timestamp to request data from hydroview API (naive UTC).
    ts_id_mapping : dict
        For each sensor_id, provide the mapping of variable names to the Hydroview
        platform hash identifiers.
    """
    if sensor_id not in ts_id_mapping.keys():
        raise KeyError(
            f"No Geolux time series hash identifiers available " f"for {sensor_id}"
        )
    ts_ids = ts_id_mapping[sensor_id]

    # convert to unixtime
    d_start_unixtime = int(time.mktime(start_timestamp.timetuple()))
    d_end_unixtime = int(time.mktime(end_timestamp.timetuple()))

    # request data from geolux platform
    ts_ids = ts_id_mapping[sensor_id]    
    data = pd.DataFrame()  
    for j, (key, ts_ids_value) in enumerate(ts_ids.items()):
        try:
            r = requests.get(
                BASE_URL,
                params={f"id{j}": ts_ids_value, "start": d_start_unixtime, "end": d_end_unixtime},
            )
            data = data.append(pd.read_csv(io.StringIO(r.content.decode("utf-8"))),
                               ignore_index=True)
        except:   
            logger.error(f"Geolux API request error - {sensor_id}\t{r.status}\t{key}\t{ts_ids_value}") 

    # convert to timestamps
    data["time"] = pd.to_datetime(data["timestamp"], unit="s")
    data = data.drop(columns=["timestamp"])

    # use Fluves variable names as column names
    data = data.rename(columns={v: k for k, v in ts_ids.items()})

    # convert to long format
    data = pd.melt(data, id_vars="time", var_name="variable_name", value_name="value")
    data = data.dropna()
    df_data = data.sort_values(by="time")
    df_data["sensor_name"] = sensor_id
    return df_data