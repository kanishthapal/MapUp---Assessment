#!/usr/bin/env python
# coding: utf-8

# In[10]:


import pandas as pd
import numpy as np


# In[2]:


df = pd.read_csv(r"C:\Users\Pasaog Tsomu\Downloads\dataset-1.csv")
df


# # Question 1

# In[4]:


def generate_car_matrix(df):
    # Create a pivot table using id_1 as index, id_2 as columns, and car as values
    car_matrix = df.pivot_table(index='id_1', columns='id_2', values='car', fill_value=0)

    # Set diagonal values to 0
    for i in car_matrix.index:
        if i in car_matrix.columns:
            car_matrix.loc[i, i] = 0

    return car_matrix


# In[5]:


result_matrix = generate_car_matrix(df)
print(result_matrix)


# # Question 2

# In[8]:


def get_type_count(df):
    conditions = [
        (df['car'] <= 15),
        (df['car'] > 15) & (df['car'] <= 25),
        (df['car'] > 25)
    ]
    choices = ['low', 'medium', 'high']
    df['car_type'] = pd.Series(np.select(conditions, choices, default='unknown'), dtype='category')
    type_count = df['car_type'].value_counts().to_dict()
    type_count = dict(sorted(type_count.items()))

    return type_count


# In[11]:


result = get_type_count(df)
print(result)


# # Question 3

# In[12]:


def get_bus_indexes(df):
    bus_mean = df['bus'].mean()
    bus_indexes = df[df['bus'] > 2 * bus_mean].index.tolist()
    # Sort the indices in ascending order
    bus_indexes.sort()

    return bus_indexes


# In[13]:


result = get_bus_indexes(df)
print(result)


# # Question 4

# In[14]:


def filter_routes(df):
    route_avg_truck = df.groupby('route')['truck'].mean()

    # Filter routes where the average of 'truck' values is greater than 7
    filtered_routes = route_avg_truck[route_avg_truck > 7].index.tolist()

    # Sort the list of filtered routes
    filtered_routes.sort()

    return filtered_routes


# In[15]:


result = filter_routes(df)
print(result)


# # Question 5

# In[16]:


def multiply_matrix(result_matrix):
    modified_matrix = result_matrix.copy(deep=True)
    # Apply the specified logic to modify values
    modified_matrix[modified_matrix > 20] *= 0.75
    modified_matrix[modified_matrix <= 20] *= 1.25
    
    modified_matrix = modified_matrix.round(1)

    return modified_matrix


# In[17]:


modified_result_matrix = multiply_matrix(result_matrix)
print(modified_result_matrix)


# # Question 6

# In[19]:


data = pd.read_csv(r"C:\Users\Pasaog Tsomu\Downloads\dataset-2.csv")
data


# In[28]:


def check_time_completeness(data):
    data['start_timestamp'] = pd.to_datetime(data['startDay'] + ' ' + data['startTime'], errors='coerce')
    data['end_timestamp'] = pd.to_datetime(data['endDay'] + ' ' + data['endTime'], errors='coerce')

    grouped = data.groupby(['id', 'id_2'])

    expected_time_range = pd.date_range(start='12:00:00 AM', end='11:59:59 PM', freq='15T')

    # Check if each pair has incorrect timestamps
    def check_pair(pair_df):
        for day in range(7):
            # Filter data for the current day
            day_data = pair_df[(pair_df['start_timestamp'].dt.dayofweek == day) & 
                                (pair_df['end_timestamp'].dt.dayofweek == day)]

            # Check if the time range for the current day is complete
            if not expected_time_range.isin(day_data['start_timestamp']).all() or                not expected_time_range.isin(day_data['end_timestamp']).all():
                return True  
        return False

    # Apply the check_pair function to each group and return the boolean series
    return grouped.apply(check_pair)


# In[29]:


result_series = check_time_completeness(data)
print(result_series)


# In[ ]:




