# MAUDE Report

## Introduction

This program utilizes data from the Manufacturer and User Facility Device Experience (MAUDE) Database through the openFDA API to generate insightful reports.

⚠ WARNING: This is a work in progress and is not yet complete.

## Current Shortcoming

Currently, the program accepts only Product Codes and Start/End Dates for custom search queries. Efforts are underway to enhance its customization options.

## How to Run

1. **Ensure you have Python installed**

    Check your Python version:

    ```bash
    python --version
    ```

    If Python is not installed, download it from: [Python Downloads](https://www.python.org/downloads/)

2. **Create a Virtual Environment and install required libraries**

    ```bash
    python -m venv .venv && .venv\Scripts\activate && pip install -r requirements.txt 
    ```

3. **Run the Script**

    ```bash
    python maude_report.py
    ```

## Note

This is an active project and may not work as intended. Any collaboration to improve it is welcomed and appreciated.

## ToDo

[X] Create a process to search openFDA from the program

[] Make the query constructor more diverse, similar to MAUDE Database search

[] Create easier executable

[] To be determined
