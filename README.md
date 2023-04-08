# AppleWatch_ECG_workflow
Python scripts for individuals or institutions receiving ECGs from Apple Watch (and hopefully Kardia soon!) can be systemically handled and managed

This repository contains two Python scripts that help healthcare institutions, individuals, or device clinics process and analyse Apple Watch ECGs. 
The first script extracts ECGs from your email inbox and saves them as code-named PDF files, while the second script analyses the extracted ECGs and outputs useful statistics and visualizations.

Prerequisites
Before you can use these scripts, you need to have Python installed on your computer. We recommend using Python 3.7 or later.

You will also need to install the following Python libraries:
numpy
pandas
matplotlib
scipy
PyMuPDF (also known as fitz)
imapclient
email (part of Python standard library)
You can install these libraries using pip:

Copy code
pip install numpy pandas matplotlib scipy PyMuPDF imapclient

Usage
1. Set up an online Python environment (optional)
If you don't have a local Python installation, you can use an online Python environment like Google Colab or Repl.it. Simply sign up for a free account and create a new Python project.

2. Clone the repository
Clone this GitHub repository to your local machine or online Python environment using the following command:

bash
Copy code
git clone https://github.com/NitHub04/AppleWatch_ECG_workflow.git
Alternatively, you can download the repository as a ZIP file and extract it to your desired location.

Copy code
python email_extraction.py
The script will save the extracted ECG PDFs to the same directory as the script.

5. Run the ECG analysis script
Run the ecg_analysis.py script to analyze the extracted ECGs:

Copy code
python ecg_analysis.py
The script will output various statistics and visualizations based on the analyzed ECGs.

Contributing
If you have any suggestions or improvements, feel free to open an issue or create a pull request.

License
This project is licensed under the MIT License. See the LICENSE file for details.
