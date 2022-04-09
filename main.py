# An attempt to rewrite the codebase as a script

import numpy as np
import pandas as pd
import dask.dataframe as dd
import matplotlib.pyplot as plt
import json

chunksize = 10 ** 4
filepath = "data/2022_place_canvas_history.csv"

ddf = dd.read_csv(filepath, blocksize="400MB")

part = ddf.partitions[-7]
part["timestamp"] = dd.to_datetime(part["timestamp"])
# part.sort_values(by=["timestamp"], ascending=True)

print("Formatted CSV.")

timestamp_idx = 1
user_id_idx = 2

threshold = 0.2 # in seconds

count_dict = {}
variance_dict = {}
time_since_dict = {}
last_pixel_time_dict = {}
thing1 = []
thing2 = []

# I don't know what they were doing here nor do I wanna think about it.

print("Processing data for bot detection...")

for row in part.itertuples():
    user_id = row[user_id_idx]
    if user_id in last_pixel_time_dict.keys():
        if user_id in time_since_dict.keys():
            time_since_last_pixel = row[timestamp_idx] - last_pixel_time_dict[row[user_id_idx]]
            variance = abs((time_since_dict[user_id] - time_since_last_pixel).total_seconds())
            # thing1.append(variance)
            if variance < threshold:
                if user_id not in count_dict.keys():
                    count_dict[user_id] = 0
                count_dict[user_id] += 1
            else:
                time_since_dict[user_id] = time_since_last_pixel
        else:
            time_since_dict[user_id] = row[timestamp_idx] - last_pixel_time_dict[user_id]
    last_pixel_time_dict[user_id] = row[timestamp_idx]

count_dict = {}
variance_dict = {}
time_since_dict = {}
last_pixel_time_dict = {}
thing1 = []
thing2 = []

for partit in ddf.partitions:
    partit["timestamp"] = dd.to_datetime(partit["timestamp"])
    for row in partit.itertuples():
        user_id = row[user_id_idx]
        if user_id in last_pixel_time_dict.keys():
            if user_id in time_since_dict.keys():
                time_since_last_pixel = row[timestamp_idx] - last_pixel_time_dict[row[user_id_idx]]
                variance = abs((time_since_dict[user_id] - time_since_last_pixel).total_seconds())
                if variance < threshold:
                    if user_id not in count_dict.keys():
                        count_dict[user_id] = 0
                    count_dict[user_id] += 1
                else:
                    time_since_dict[user_id] = time_since_last_pixel
            else:
                time_since_dict[user_id] = row[timestamp_idx] - last_pixel_time_dict[user_id]
        last_pixel_time_dict[user_id] = row[timestamp_idx]

print("Generating result files...")

with open('counts.txt', 'w') as convert_file:
    convert_file.write(json.dumps(count_dict))
count_series = pd.Series(count_dict)


# Finalize output
with open('counts_greater_than_2.txt', 'w') as convert_file:
    convert_file.write(json.dumps(count_series[count_series > 2].to_dict()))
with open('user_ids_greater_than_2.txt', 'w') as outfile:
    json.dump(list(count_series[count_series > 2].to_dict().keys()), outfile)