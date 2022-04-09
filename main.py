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
        variance = []
        for time in difference_in_time:
            variance.append(time / average)
        user_placement_variance[user_id] = sum(variance) / len(variance)


# I don't know what they were doing here nor do I wanna think about it.

print("Processing data for bot detection...")
