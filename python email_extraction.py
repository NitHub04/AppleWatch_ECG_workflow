from exchangelib import Account, Credentials, DELEGATE
import os

# Set up Exchange credentials
username = "[email]"
password = "[password]"
shared_mailbox = "[if applicable]"
credentials = Credentials(username=username, password=password)

# Set up Exchange account
account = Account(
    primary_smtp_address=shared_mailbox,
    credentials=credentials,
    autodiscover=True,
    access_type=DELEGATE,
)

# Set up a search folder for emails with attachments
search_folder = account.inbox
search_folder_items = search_folder.filter(has_attachments=True)

# Create a directory to store the attachments
save_folder = os.path.join(os.getcwd(), "All_Attachments")
if not os.path.exists(save_folder):
    os.makedirs(save_folder)

search_folder_items = list(search_folder.filter(has_attachments=True))

# Loop through the emails and download attachments
for i, mail_item in enumerate(search_folder_items):
    attachments = mail_item.attachments
    for attachment in attachments:
        try:
            # Get the binary content of the attachment
            content = attachment.content
            # Get the file name of the attachment
            filename = attachment.name
            # Save the attachment to a file
            with open(os.path.join(save_folder, filename), "wb") as f:
                f.write(content)
        except AttributeError:
            # Skip the current attachment if it's not a file attachment
            continue
    print(f"Downloaded attachments from email {i + 1} of {len(search_folder_items)}")

# Close the connection to the Exchange server
account.protocol.close()


import fitz
import re
import os
from datetime import datetime
import pandas as pd
import random

"""
 individual pdf file name_date_rhythm
 
"""
"""
# Set up the file paths
pdf_path = os.path.join(os.getcwd(), "[filename.pdf")

# Open the PDF file and loop through the pages
with fitz.open(pdf_path) as pdf_doc:
    for page_num, page in enumerate(pdf_doc):
        # Get the page text
        page_text = page.get_text()

        # Extract the name from the page text
        name_pattern = r"^(.*)\n"
        name_match = re.search(name_pattern, page_text)
        name = name_match.group(1)

        # Extract the date from the page text
        date_pattern = r"Recorded on (\d{2} \w{3} \d{4})"
        date_match = re.search(date_pattern, page_text)
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

        # Extract the rhythm from the page text
        lines = page_text.split("\n")
        rhythm = lines[3]
#        rhythm_pattern = r"^Sinus Rhythm.*|^(?!Sinus Rhythm)[A-Z][a-z]+\s[A-Z][a-z]+.*|Inconclusive|Low Heart Rate|High Heart Rate"
#        rhythm_match = re.search(rhythm_pattern, page_text, re.MULTILINE)
#        rhythm = rhythm_match.group(0)

        print(name)
        print(date)
        print(rhythm)
        
"""
"""
Looped pdf to named pdf

"""

# Set up the file paths
pdf_dir = os.getcwd()

#count how many files
pdf_count = len([f for f in os.listdir(pdf_dir) if f.endswith('.pdf')])
print(f'There are {pdf_count} PDF files in the directory.')

# Loop through each PDF file in the directory
for pdf_file in os.listdir(pdf_dir):
    if pdf_file.endswith(".pdf"):
        # Open the PDF file and loop through the pages
        pdf_path = os.path.join(pdf_dir, pdf_file)
        with fitz.open(pdf_path) as pdf_doc:
            for page_num, page in enumerate(pdf_doc):
                # Get the page text
                page_text = page.get_text()

                # Extract the name from the page text
                name_pattern = r"^(.*)\n"
                name_match = re.search(name_pattern, page_text)
                if name_match:
                    name = name_match.group(1)
                else:
                    name = "unknown"

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
                rhythm = lines[3] if len(lines) >= 4 else "unknown"

                # Rename the PDF file
                new_name = f"{name}_{date}_{rhythm}.pdf"
                new_path = os.path.join(pdf_dir, new_name)
                os.rename(pdf_path, new_path)
                break  # Only process the first page
                

