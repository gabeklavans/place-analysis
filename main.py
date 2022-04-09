# An attempt to rewrite the codebase as a script

import numpy as np
import pandas as pd
import dask.dataframe as dd
import matplotlib.pyplot as plt
import json

chunksize = 10 ** 4
filepath = "data/2022_place_canvas_history.csv"

ddf = dd.read_csv(filepath, blocksize="10MB")

part = ddf.partitions[-7]
part["timestamp"] = dd.to_datetime(part["timestamp"])
# part.sort_values(by=["timestamp"], ascending=True)

print("Formatted CSV.")

timestamp_idx = 1
user_id_idx = 2


# Danny's rewrite attempt

## Re-arrange the data set to organize it by key: user value: time place
## TO DO: Maybe use dataframe to organize this data set instead due to it's large size?
user_pixels_placed = {}

for row in part.itertuples():
    user_id = row[user_id_idx]
    if user_pixels_placed[user_id] == None:
        user_pixels_placed[user_id] = []
    user_pixels_placed[user_id].append(user_pixels_placed)

## Process this data
user_placement_variance = []

for user_id in user_pixels_placed.keys():
    placement_time_list = user_pixels_placed[user_id]
    if len(placement_time_list)>1:
        # Find differences between pixel placements
        difference_in_time = []
        for i in range(1, len(placement_time_list)):
            difference_in_time.append(placement_time_list[i - 1], placement_time_list[i])
        # Compare differences between the pixels placed by dividing idk if this is a good way or hella inefficient probably is
        average = sum(difference_in_time) / len(difference_in_time)


threshold = 0.2 # in seconds

count_dict = {}
variance_dict = {}
time_since_dict = {}
last_pixel_time_dict = {}
thing1 = []
thing2 = []

# I don't know what they were doing here nor do I wanna think about it.

print("Processing data for bot detection...")



"""
for row in part.itertuples():
    user_id = row[user_id_idx]
    if user_id in last_pixel_time_dict.keys():
        if user_id in time_since_dict.keys():
            # Get time difference between last pixel placement and newly found pixel
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
    # Store current pixel placement
    last_pixel_time_dict[user_id] = row[timestamp_idx]
"""
print("Done!")

# Scans whole data set, disabled for testing purposes

"""

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

"""

print("Generating result files...")

with open('counts.txt', 'w') as convert_file:
    convert_file.write(json.dumps(count_dict))
count_series = pd.Series(count_dict)


# Finalize output
with open('counts_greater_than_2.txt', 'w') as convert_file:
    convert_file.write(json.dumps(count_series[count_series > 2].to_dict()))
with open('user_ids_greater_than_2.txt', 'w') as outfile:
    json.dump(list(count_series[count_series > 2].to_dict().keys()), outfile)