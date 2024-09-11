import requests
import pandas as pd

api_key = "15f9405a-7801-4f90-8c11-bc6180dd18ff"

company_numbers = [
    "14295314", "14295313", "14319761", "14339152", "14311212",
    "13304203", "14084681", "14253404", "14301335", "14290244",
    "13890037", "14316433", "14319857", "14319824", "14236305",
    "14237402", "13562968", "12851410"
]

headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json'
}

officers_list = []

for company_number in company_numbers:
    url = f"https://api.company-information.service.gov.uk/company/{company_number}/officers"
    params = {
        'items_per_page': 100,  # adjust as needed
        'register_type': 'directors',  # adjust if needed
        'register_view': 'false',  # adjust if needed
        'order_by': 'appointed_on'  # adjust if needed
    }

    while url:
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            officer_data = response.json()
            for officer in officer_data.get('items', []):
                officer_info = {
                    "Company Number": company_number,
                    "Name": officer.get('name', 'N/A'),
                    "Role": officer.get('officer_role', 'N/A'),
                    "Date of Birth": f"{officer.get('date_of_birth', {}).get('month', 'N/A')} {officer.get('date_of_birth', {}).get('year', 'N/A')}",
                    "Nationality": officer.get('nationality', 'N/A'),
                    "Country of Residence": officer.get('country_of_residence', 'N/A'),
                    "Occupation": officer.get('occupation', 'N/A'),
                    "Appointed On": officer.get('appointed_on', 'N/A'),
                    "Address": f"{officer.get('address', {}).get('address_line_1', 'N/A')}, {officer.get('address', {}).get('postal_code', 'N/A')}"
                }
                officers_list.append(officer_info)

            # Check for pagination
            url = officer_data.get('links', {}).get('next')  # URL for the next page, if available
        else:
            print(f"Failed to retrieve data for company {company_number}. Status code: {response.status_code}")
            print(response.text)  # Print the response text for debugging
            url = None  # Stop pagination if there's an error

df = pd.DataFrame(officers_list)
df.to_excel('company_officers.xlsx', index=False)

print("Data has been exported to 'company_officers.xlsx'.")
