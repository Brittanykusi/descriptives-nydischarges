# This descriptive analysis should be detailed enough 
# so a physician or nurse could understand what information
# is contained in the dataset, and what potentially questions 
# might be asked and answered. 

############# IMPORT PACKAGES ###########
import pandas as pd
import numpy as np
import researchpy as rp
from scipy import stats 
from tableone import TableOne, load_dataset
########################################




############# IMPORT DATASET ###########
Hospital_Inpatient_Discharges = pd.read_csv('/Users/brittanykusi-gyabaah/Downloads/Hospital_Inpatient_Discharges__SPARCS_De-Identified___2016.csv')
Hospital_Inpatient_Discharges.columns = Hospital_Inpatient_Discharges.columns.str.replace('[^A-Za-z0-9]+', '_')
Hospital_Inpatient_Discharges.info()
########################################

# Link Facility ID to Facilty's name
Facility = pd.pivot_table(Hospital_Inpatient_Discharges, values=['Facility_Name'], index='Facility_Id', columns=None, aggfunc=np.sum)
print(Facility)

# Link DRG Code to its description
APR_DRG = pd.pivot_table(Hospital_Inpatient_Discharges, values=['APR_DRG_Description'], index='APR_DRG_Code', columns=None, aggfunc=np.sum)
print(APR_DRG)




######## CREATE SMALLER TABLE ###########
HID = Hospital_Inpatient_Discharges[['Facility_Id', 'Age_Group', 'Gender', 
               'Type_of_Admission', 'APR_DRG_Description', 
               'Total_Charges', 'Length_of_Stay']]
HID.dtypes
#remove all commas within each column
HID.replace(',','', regex=True, inplace=True)
HID['Total_Charges'] = HID['Total_Charges'].astype(float)
HID.dtypes
#########################################

# What are the top 50 facilities with the highest amount of discharges in 2016?
HCounts = HID['Facility_Id'].value_counts()
HCounts.head(50)
# Relative frequency of facility discharges
HID.Facility_Id.value_counts(normalize=True)*100




##### Let's focus on Facility 1169 ######
# facility 1169 had the highest frequency 
# discharges within the year 2016.
HID1169 = HID[HID.Facility_Id.isin(["1169"])]
#########################################

# What is the mean of total charges for facility 1,169?
HID1169['Total_Charges'] = HID1169['Total_Charges'].astype(float)
HID1169.dtypes
HID1169.Total_Charges.mean()

# What is the mode for APR_DRG_Descriptions and type of admission? 
APR_mode = HID1169.APR_DRG_Description.value_counts()
APR_mode.head(50)
# the most frequent reason for visits --> Neonate birthwt >2499g, normal newborn or neonate w other problem
Type_of_Admission_mode = HID1169.Type_of_Admission.value_counts()
Type_of_Admission_mode.head(50)
# emergency visits were the highest




################# TABLE0NE TABLE #################
HID1169_clone = HID1169
HID1169_clone.dtypes
list(HID1169_clone)
HID1169_clone.head(5)
HID1169_clone['APR_DRG_Description']
HID1169_clone_columns = ['Facility_Id', 'Age_Group', 'Gender', 
               'Type_of_Admission', 'APR_DRG_Description', 
               'Total_Charges', 'Length_of_Stay']
HID1169_clone_categories=['Gender', 'Type_of_Admission', 'APR_DRG_Description', 'Age_Group', 'Length_of_Stay']
HID1169_clone_groupby = ['Facility_Id']
HID1169_clone['Gender'].value_counts()
HID1169_clone_table1 = TableOne(HID1169_clone, columns=HID1169_clone_columns, 
    categorical=HID1169_clone_categories, groupby=HID1169_clone_groupby, pval=False)
print(HID1169_clone_table1.tabulate(tablefmt = "fancy_grid"))
HID1169_clone_table1.to_csv('/Users/brittanykusi-gyabaah/Documents/GitHub/descriptives-nydischarges/data.csv')
