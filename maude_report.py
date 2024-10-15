import requests
import pandas as pd
import os
import json

# Take user input
def user_input():
    product_code_input = input("Enter the Product Code: ")
    start_date_input = input("Start Date [YYYY-MM-DD]: ")
    end_date_input = input("End Date [YYYY-MM-DD]: ")
    return product_code_input, start_date_input, end_date_input

# Construct the API query
def query_constructor(start_date, end_date, product_code):
    base_endpoint = "https://api.fda.gov/device/event.json?search="
    separator = "+AND+"
    limit = "&limit=500"
    
    date_received = f"date_received:[{start_date}+TO+{end_date}]"
    p_code = f"device.device_report_product_code.exact:{product_code}"
    
    query = f"{base_endpoint}{date_received}{separator}{p_code}{limit}"
    return query

# Fetch data from openFDA
def fetch_API(query):
    response = requests.get(query)
    if response.status_code == 200:
        data = response.json().get('results', [])
        if data:
            return data
        else:
            raise ValueError("No results found.")
    else:
        raise Exception(f"Failed to retrieve data: {response.status_code} {response.text}")

# Normalize the fetched data
def normalize_data(data):
    combined_data = pd.json_normalize(data)

    combined_data['Brand_Name'] = combined_data['device'].apply(
        lambda x: x[0]['brand_name'] if isinstance(x, list) and x else None
    )
    combined_data['Event_Type'] = combined_data['event_type'].apply(
        lambda x: x if pd.notnull(x) else None
    )
    combined_data['Product_Problems'] = combined_data['product_problems'].apply(
        lambda x: '; '.join(x) if isinstance(x, list) and x else None
    )

    return combined_data

# Create event report
def create_event_report(combined_data):
    event_report = (combined_data
        .groupby(['Brand_Name', 'Event_Type'])
        .size()
        .reset_index(name='Event_Count')
        .sort_values(by=['Brand_Name', 'Event_Count'], ascending=[True, False])
    )
    return event_report

# Create problem report
def create_problem_report(combined_data):
    problem_report = (combined_data
        .groupby(['Brand_Name', 'Product_Problems'])
        .size()
        .reset_index(name='Problem_Count')
        .sort_values(by=['Brand_Name', 'Problem_Count'], ascending=[True, False])
    )
    return problem_report

# Save report to CSV
def save_report_to_csv(report, filename):
    os.makedirs('reports', exist_ok=True)
    try:
        report.to_csv(f"reports/{filename}", index=False)
        print(f"Report generated: {filename}")
    except Exception as e:
        print(f"Error writing {filename}: {str(e)}")

# Save JSON response to file
def save_json(data):
    os.makedirs('reports', exist_ok=True)
    try:
        with open("reports/fda_data.json", "w") as json_file:
            json.dump(data, json_file, indent=4)
        print("JSON data saved as fda_data.json")
    except Exception as e:
        print(f"Error saving JSON data: {str(e)}")

# Save normalized data to JSON file
def save_normalized_json(data):
    os.makedirs('reports', exist_ok=True)
    try:
        normalized_json_file_path = "reports/normalized_data.json"
        data.to_json(normalized_json_file_path, orient='records', lines=True)
        print(f"Normalized data saved as normalized_data.json")
    except Exception as e:
        print(f"Error saving normalized data: {str(e)}")

def main():
    try:
        product_code, start_date, end_date = user_input()
        query = query_constructor(start_date, end_date, product_code)
        data = fetch_API(query)
        save_json(data)  # Save the raw JSON data
        
        combined_data = normalize_data(data)  # Normalize the data
        event_report = create_event_report(combined_data)  # Create event report
        problem_report = create_problem_report(combined_data)  # Create problem report

        save_report_to_csv(event_report, "event_type_report.csv")  # Save event report
        save_report_to_csv(problem_report, "product_problems_report.csv")  # Save problem report
        
        save_normalized_json(combined_data)  # Save normalized data
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
