#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  8 13:00:31 2023

@author: nikhil88
"""

import os
import datetime
import pandas as pd

pdf_folder = os.getcwd()
pdf_files = [file for file in os.listdir(pdf_folder) if file.endswith('.pdf')]

data = []

for file in pdf_files:
    patient_name, date_str, diagnosis = file.split('_', 2)
    
    try:
        date_obj = datetime.datetime.strptime(date_str, '%d%m%Y')
        date_formatted = date_obj.strftime('%d-%m-%Y')
    except ValueError:
        date_formatted = "unknown"
    
    data.append([patient_name, date_formatted, diagnosis])

df = pd.DataFrame(data, columns=['patient_name', 'date', 'diagnosis'])

total_ecg_pdfs = len(pdf_files)
unique_patient_count = len(df['patient_name'].unique())
valid_dates_df = df[df['date'] != 'unknown']
valid_dates_df['date'] = pd.to_datetime(valid_dates_df['date'], format='%d-%m-%Y')

earliest_date = valid_dates_df['date'].min().strftime('%d-%m-%Y')
latest_date = valid_dates_df['date'].max().strftime('%d-%m-%Y')

print(f"Total ECG PDFs: {total_ecg_pdfs}")
print(f"Unique Patients: {unique_patient_count}")
print(f"Earliest Date: {earliest_date}")
print(f"Latest Date: {latest_date}")

patient_counts = df.groupby('patient_name')['date'].count()
lower_quartile = patient_counts.quantile(0.25)
median_ecgs = patient_counts.median()
upper_quartile = patient_counts.quantile(0.75)

print(f"Median ECGs per Patient: {median_ecgs}")
print(f"Lower Quartile: {lower_quartile}")
print(f"Upper Quartile: {upper_quartile}")

daily_counts = df[df['date'] != 'unknown'].groupby('date')['patient_name'].count()
daily_median = daily_counts.median()
daily_lower_quartile = daily_counts.quantile(0.25)
daily_upper_quartile = daily_counts.quantile(0.75)

print(f"Median ECGs per Day: {daily_median}")
print(f"Lower Quartile: {daily_lower_quartile}")
print(f"Upper Quartile: {daily_upper_quartile}")

import fitz
import re

pdf_folder = os.getcwd()
pdf_files = [file for file in os.listdir(pdf_folder) if file.endswith('.pdf')]

rows = []

for pdf_file in pdf_files:
    pdf_path = os.path.join(pdf_folder, pdf_file)
    
    with fitz.open(pdf_path) as pdf_doc:
        for page_num, page in enumerate(pdf_doc):
            page_text = page.get_text()

            # Extract the name from the page text
            name_pattern = r"^(.*)\n"
            name_match = re.search(name_pattern, page_text)
            name = name_match.group(1)

            # Extract the date from the page text
            date_pattern = r"Recorded on (\d{2} \w{3} \d{4})"
            date_match = re.search(date_pattern, page_text)
            if date_match:
                date_str = date_match.group(1)
                date_parts = date_str.split()
                day = date_parts[0]
                month = date_parts[1]
                year = date_parts[2]
                month_num = {
                    "Jan": "01",
                    "Feb": "02",
                    "Mar": "03",
                    "Apr": "04",
                    "May": "05",
                    "Jun": "06",
                    "Jul": "07",
                    "Aug": "08",
                    "Sep": "09",
                    "Oct": "10",
                    "Nov": "11",
                    "Dec": "12"
                }[month]
                date = day + month_num + year
            else:
                date = "unknown"

            # Extract the rhythm from the page text
            lines = page_text.split("\n")
            rhythm = lines[3]

            # Extract symptoms
            symptoms_pattern = r"Reported Symptoms"
            symptoms_match = re.search(symptoms_pattern, page_text)
            has_symptoms = int(bool(symptoms_match))

            # Extract symptom types
            if has_symptoms:
                symptom_phrases = [
                    "coughing",
                    "rapid, pounding, or fluttering heartbeat",
                    "shortness of breath",
                    "skipped heartbeat",
                    "wheezing"
                ]
                
                symptom_types = []
                for phrase in symptom_phrases:
                    if phrase.lower() in page_text.lower():
                        symptom_types.append(phrase)
                
                symptom_types = ', '.join(symptom_types)
            else:
                symptom_types = ""


            rows.append([name, date, rhythm, has_symptoms, symptom_types])

df = pd.DataFrame(rows, columns=["Name", "Date", "Rhythm", "Symptoms", "Symptom Type"])
print("Number of patients with symptoms:", sum(df['Symptoms']))

rhythm_counts = df['Rhythm'].value_counts()

symptom_type_counts = df['Symptom Type'].value_counts()
print("Symptom Type Counts:")
print(symptom_type_counts)



rhythm_types = [
    'Atrial Fibrillation',
    'Sinus Rhythm',
    'High Heart Rate',
    'Heart Rate Over',
    'Poor Recording',
    'Inconclusive',
    'Heart Rate Under'
]

rhythm_counts = {rhythm_type: 0 for rhythm_type in rhythm_types}

for rhythm_type in rhythm_types:
    rhythm_counts[rhythm_type] = df['Rhythm'].apply(lambda x: rhythm_type in x).sum()

for rhythm_type, count in rhythm_counts.items():
    print(f"{rhythm_type}: {count}")

rhythm_types = [
    'Atrial Fibrillation',
    'Sinus Rhythm',
    'High Heart Rate',
    'Heart Rate Over',
    'Poor Recording',
    'Inconclusive',
    'Heart Rate Under'
]

import matplotlib.pyplot as plt

# Calculate the sum of unknown rhythm types
unknown_sum = sum([rhythm_counts['High Heart Rate'], rhythm_counts['Heart Rate Over'], rhythm_counts['Poor Recording'], rhythm_counts['Inconclusive'], rhythm_counts['Heart Rate Under']])

# Prepare the data for the stacked bar chart
rhythm_types_chart = ['Atrial Fibrillation', 'Sinus Rhythm', 'Unknown']
counts = [rhythm_counts['Atrial Fibrillation'], rhythm_counts['Sinus Rhythm'], unknown_sum]
segments = [count / 3 for count in counts]

fig, ax = plt.subplots()

# Set the bar thickness
bar_thickness = 0.5

# Create the horizontal stacked bar chart with custom colors and thickness
ax.barh(rhythm_types_chart, segments, height=bar_thickness, label='Atrial Fibrillation', color='blue')
ax.barh(rhythm_types_chart, segments, left=segments, height=bar_thickness, label='Sinus Rhythm', color='orange')
ax.barh(rhythm_types_chart, segments, left=[2 * seg for seg in segments], height=bar_thickness, label='Unknown', color='lightgreen')

ax.set_xlabel('Count')
ax.set_ylabel('Apple Watch label')
#ax.set_title('Horizontal Stacked Bar Chart')
ax.legend(title='Expert label')

plt.show()

rows = []

for rhythm_type in rhythm_types:
    total_count = df['Rhythm'].apply(lambda x: rhythm_type in x).sum()
    with_symptoms = df.loc[(df['Rhythm'].apply(lambda x: rhythm_type in x)) & (df['Symptoms'] == 1)].shape[0]
    without_symptoms = df.loc[(df['Rhythm'].apply(lambda x: rhythm_type in x)) & (df['Symptoms'] == 0)].shape[0]
    
    rows.append([rhythm_type, total_count, with_symptoms, without_symptoms])

summary_df = pd.DataFrame(rows, columns=['Rhythm', 'Total Count', 'Symptoms', 'No Symptoms'])

print(summary_df)

