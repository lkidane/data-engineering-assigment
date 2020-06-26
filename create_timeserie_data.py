#!/usr/bin/env python
# coding: utf-8

# # Patient Record Analysis Project
# ## Import Useful Libraries

#import necesssary libraries
import pyodbc
import warnings
import pandas as pd
from collections import Counter
import datetime
import os

warnings.filterwarnings('ignore')


# ## Make Connection to MySql db
#make the connection
conn = pyodbc.connect(
    'Driver={/opt/microsoft/msodbcsql17/lib64/libmsodbcsql-17.5.so.2.1};'
    'Server=localhost;'
    'Database=master;'
    'uid=sa;pwd=Password123')


# ## Data Cleaning

#Read the necessary tables from the database
df_encounter = pd.read_sql('SELECT * FROM encounter', con=conn)
df_condition = pd.read_sql('SELECT * FROM condition', con=conn)
df_procedure = pd.read_sql('SELECT * FROM [procedure]', con=conn)
df_observation = pd.read_sql('SELECT * FROM observation', con=conn)
df_medicationrequest = pd.read_sql('SELECT * FROM medicationrequest', con=conn)


# Lets look at the size of all tha tables.

#Rename columns and print first 5 rows
ft = ['medreq_medicationCodeableConcept','medreq_dI_aI_coding_display','medreq_dI_dQ_value','medreq_dI_aI_coding_code',
              'medreq_dI_t_repeat_period','medreq_dI_t_repeat_frequency','medreq_dI_asNeededBoolean',
              'encounter_id','medreq_dI_aI_coding_system','medreq_dI_aI_text','patient_id','id','medreq_rR_reference','medreq_dI_sequence','medreq_dI_t_repeat_periodUnit','medreq_authoredOn']
df_medicationrequest.columns = ft


#Chenge the date time column in to date time format
df_medicationrequest['medreq_authoredOn'] = pd.to_datetime(df_medicationrequest['medreq_authoredOn'])
#  creating new features from authoredOn column
df_medicationrequest['medreq_month'] = df_medicationrequest.medreq_authoredOn.dt.month

df_medicationrequest['medreq_year'] = df_medicationrequest.medreq_authoredOn.dt.year

df_medicationrequest['medreq_day'] = df_medicationrequest.medreq_authoredOn.dt.day

df_medicationrequest['medreq_hour'] = df_medicationrequest.medreq_authoredOn.dt.hour

df_medicationrequest['medreq_authoredOn'] = df_medicationrequest['medreq_authoredOn'].dt.date


# ### **Encounter Table**
 # 
# hospitalization_dischargeDisposition_coding_code --> h_dD_coding_code
# 
# reason_coding_system --> reason_coding_system
# 
# reason_coding_code -->  reason_coding_code
# 
# hospitalization_dischargeDisposition_coding_display --> h_dD_coding_display
# 
# period_end --> period_end 
# 
# class --> class
# 
# hospitalization_dischargeDisposition_text --> h_dD_text
# 
# patient_id --> patient_id
# 
# id --> id
# 
# reason_coding_display --> reason_coding_display
# 
# period_start --> period_start
# 
# hospitalization_dischargeDisposition_coding_system -->  h_dD_coding_system
# 
# type --> type 
# 

# In[13]:


# rename columns
ft = ['enc_h_dD_coding_code','enc_reason_coding_system','enc_reason_coding_code','enc_h_dD_coding_display',
              'enc_period_end','enc_class','enc_h_dD_text',
              'patient_id','encounter_id','enc_reason_coding_display','enc_period_start','enc_h_dD_coding_system','enc_type']
df_encounter.columns = ft


# In[14]:


#Chenge the date time column in to date time format
df_encounter['enc_period_end'] = pd.to_datetime(df_encounter['enc_period_end'])
df_encounter['enc_period_start'] = pd.to_datetime(df_encounter['enc_period_start'])

#Change the period_end column 

df_encounter['enc_end_month'] = df_encounter.enc_period_end.dt.month

df_encounter['enc_end_year'] = df_encounter.enc_period_end.dt.year

df_encounter['enc_end_day'] = df_encounter.enc_period_end.dt.day

df_encounter['enc_end_hour'] = df_encounter.enc_period_end.dt.hour

df_encounter['enc_period_end'] = df_encounter['enc_period_end'].dt.date

#Change the period_start column 

df_encounter['enc_start_month'] = df_encounter.enc_period_start.dt.month

df_encounter['enc_start_year'] = df_encounter.enc_period_start.dt.year

df_encounter['enc_start_day'] = df_encounter.enc_period_start.dt.day

df_encounter['enc_start_hour'] = df_encounter.enc_period_start.dt.hour

df_encounter['enc_period_start'] = df_encounter['enc_period_start'].dt.date


# ### **Condition Table**
# 
# The names of the column are short. Thus, we are not going to change the names.

# In[15]:


#check the colum
#As the table doesnt have long column names,there is no need to change them.
df_condition.columns


# In[16]:


# rename columns
ft = ['cond_code', 'encounter_id', 'patient_id', 'id', 'cond_clinicalStatus',
       'cond_onsetDateTime']
df_condition.columns = ft


# In[17]:


#Chenge the date time column in to date time format
df_condition['cond_onsetDateTime'] = pd.to_datetime(df_condition['cond_onsetDateTime'])
#Change the period_start column 

df_condition['cond_month'] = df_condition.cond_onsetDateTime.dt.month

df_condition['cond_year'] = df_condition.cond_onsetDateTime.dt.year

df_condition['cond_day'] = df_condition.cond_onsetDateTime.dt.day

df_condition['cond_hour'] = df_condition.cond_onsetDateTime.dt.hour

df_condition['cond_onsetDateTime'] = df_condition['cond_onsetDateTime'].dt.date


# ### **Procedure Table**

# In[18]:


#Check the column names of the table
df_procedure.columns


# In[19]:


# rename columns
ft = ['proc_code','encounter_id','patient_id','proc_rR_display',
              'id','proc_rR_reference','proc_pP_end',
              'proc_pP_start']
df_procedure.columns = ft

# In[20]:


# rename columns
names = ['observ_vCC_coding_code', 'observ_code',
       'observ_vCC_coding_system',
       'observ_vCC_coding_display', 'observ_component_value', 'observ_valueString',
       'observ_value', 'encounter_id', 'observ_component_code', 'patient_id',
       'observ_vCC_text', 'id', 'observ_unit', 'observ_effectiveDateTime',
       'observ_component_unit']
df_observation.columns = names


# 
# 
# We investigated Observation table for missing values in the columns. Our observation revealed that 99.78%, 99.78%, 99.78%, 87.61%, 99.77% , 12.85%, 87.61%, 99.78%, 12.85% and 87.61% of data observations for ```vCC_coding_code``` ,```vCC_coding_system```, ```vCC_coding_display```,  ```component_value```,  ```valueString```,  ```value```,  ```component_value```, ```component_code```, ```vCC_text```, ```unit``` and ```component_unit``` were missing respectively in the data set.

# In[21]:


#Chenge the date  column to date time
df_observation['observ_effectiveDateTime'] = pd.to_datetime(df_observation['observ_effectiveDateTime'])
#Change the effectiveDateTime column 

df_observation['obsv_month'] = df_observation.observ_effectiveDateTime.dt.month

df_observation['obsv_year'] = df_observation.observ_effectiveDateTime.dt.year

df_observation['obsv_day'] = df_observation.observ_effectiveDateTime.dt.day

df_observation['obsv_hour'] = df_observation.observ_effectiveDateTime.dt.hour

df_observation['observ_effectiveDateTime'] = df_observation['observ_effectiveDateTime'].dt.date


# # 2. Create a timeseries dataset
# ### Merge Tables
# 
# We are going to merge the tables based on 'patient_id' and 'encounter_id' for better analysis.

# In[22]:


on = ['patient_id','encounter_id']
merged_df = df_medicationrequest.merge(df_condition,on=on,how='outer').merge(df_procedure,on=on,how='outer').merge(df_observation,on=on,how='outer').merge(df_encounter,on=on)#
merged_df .shape


# In[23]:


unwanted = merged_df.columns[merged_df.columns.str.startswith('id')]
merged_df.drop(unwanted, axis=1, inplace=True)


# ### Create a Time Series Data
# 
# Now we are going to create a time series data from the merged file we created earlier. We are going to use the column 'enc_period_start' as an index to the table to create a time series data for each patient.

# In[25]:


merged_df.set_index(['enc_period_start'],drop=True, inplace=True)


# In[26]:


merged_df.head()


# In[27]:


merged_df.fillna('N.A.',inplace=True)


# In[32]:


print(merged_df.head())

os.makedirs('/data', exist_ok=True)
merged_df.to_csv('/data/time_series.csv',index = False)

# In[ ]:




