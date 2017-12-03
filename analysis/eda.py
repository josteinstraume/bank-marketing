import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
import seaborn as sns
import statistics as st
import csv as csv

# TO DO: Assess the fit- Hosmer and Lemeshow Goodness of fit
# TO DO: ROC Curve

# Load in the data
# Source:
# https://www.datacamp.com/community/tutorials/exploratory-data-analysis-python
filepath = "/Users/Jostein/Grad School/SMU/6372/project3/bank-marketing/data/bank-full.csv"
bank = pd.read_csv(filepath, header='infer', delimiter=';')

# Check if data loaded in properly
print(bank)

# Check how clean the data is
# If there is missing data, we could use fillna(mean) for imputation
pd.isnull(bank).sum()

# Deal with unknown values
# No NA's, but there are unknowns
# Let's plot each variable and see in which the unknowns occur
# Source:
# https://seaborn.pydata.org/generated/seaborn.countplot.html
cat_vars = ['job', 'marital', 'education', 'default', 'housing', 'loan',
            'contact', 'poutcome']
sns.set(style="darkgrid")
for col in cat_vars:
    plt.figure()
    sns.countplot(y=col, data=bank, palette='hls')
    plt.savefig('/Users/Jostein/Grad School/SMU/6372/project3/bank-marketing/plots/'
                + col + '_count_plot')
    if sum(bank[col] == 'unknown') != 0:
        print(col + ' has unknown variables!')

# Return the number of unknowns for variables:
# job, education, contact, and poutcome
unknown_vars = ['job', 'education', 'contact', 'poutcome']
for col in unknown_vars:
    print('The number of unknowns in ' + col + ' variable is: '
          + str(sum(bank[col] == 'unknown')))

pct_unknown_val = round(100 * (sum(bank['poutcome']=='unknown') / bank.shape[0]), 2)
pct_failure_val = round(100 * (sum(bank['poutcome']=='failure') / bank.shape[0]), 2)
pct_success_val = round(100 * (sum(bank['poutcome']=='success') / bank.shape[0]), 2)

print('Unknown accounts for ' + str(pct_unknown_val) + '% of poutcome observations.')
print('Failure accounts for ' + str(pct_failure_val) + '% of poutcome observations.')
print('Success accounts for ' + str(pct_success_val) + '% of poutcome observations.')

# Imputate the unknown values with the mode of their respective variable
bank.replace({'job': {'unknown': 'blue-collar'}}, inplace=True)
bank.replace({'education': {'unknown': 'secondary'}}, inplace=True)
bank.replace({'contact': {'unknown': 'cellular'}}, inplace=True)

imput_vars = ['job', 'education', 'contact']

# Check to see if unknowns were imputed
# Visually confirm unknowns were successfully imputed
for col in imput_vars:
    if sum(bank[col] == 'unknown') == 0:
        print('Unknowns in ' + col + ' variable imputed successfully!')
    plt.figure()
    sns.countplot(y=col, data=bank, palette='hls')
    plt.savefig('/Users/Jostein/Grad School/SMU/6372/project3/bank-marketing/plots/'
                + col + 'imput_count_plot')

# Snapshot of the data
bank.head()

# Summary statistics for variables
bank.describe()

# Check the data types
bank.dtypes

# Create new data set with categorical variables
# encoded as dummy variables
# Sources:
# http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.merge.html#pandas.DataFrame.merge
# http://pandas.pydata.org/pandas-docs/stable/generated/pandas.get_dummies.html
smart_cols = ['age', 'balance', 'day', 'duration',
              'campaign', 'pdays', 'previous']
dum_cols = ['job', 'marital', 'education', 'default','housing', 
            'loan', 'contact', 'month', 'poutcome', 'y']
dum_bank = pd.get_dummies(bank[dum_cols], prefix=dum_cols, drop_first=True)
dum_bank.head()
dum_bank.columns

new_bank = pd.DataFrame(bank[smart_cols]).join(dum_bank)
new_bank.columns
new_bank.head()

# Exploratory Data Analysis
# Source:
# https://seaborn.pydata.org/generated/seaborn.countplot.html

# First let's plot the distribution of people who subscribe 
# for a term deposit vs don't based on their age
plt.figure()
sns.factorplot(y='age', palette="Set3", col="y",
               data=bank, kind="count", size=10, aspect=.7)
plt.savefig('/Users/Jostein/Grad School/SMU/6372/project3/bank-marketing/plots/dist_age_termdeposit')

# Now that dummy variables are coded, we can create a
# heat map of the correlation between variables
# Source:
# http://www.data-mania.com/blog/logistic-regression-example-in-python/
plt.figure()
sns.heatmap(new_bank.corr())
plt.savefig('/Users/Jostein/Grad School/SMU/6372/project3/bank-marketing/plots/corr_heatmap')

