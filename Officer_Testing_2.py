import requests
import pandas as pd


api_key = "03ed5851-da50-4a59-9c87-d903055fd3e6"


company_numbers = ["14295314", "14295313", "14319761", "14339152", "14311212", "13304203", "14084681", "14253404",
                   "14301335", "14290244", "13890037", "14316433", "14319857", "14319824", "14236305", "14237402",
                   "13562968", "12851410"]


headers = {
    'Authorization': f'Basic {api_key}:'
}


officers_list = []


for company_number in company_numbers:
    url = f"https://api.company-information.service.gov.uk/company/{company_number}/officers"
    response = requests.get(url, headers=headers)

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
    else:
        print(f"Failed to retrieve data for company {company_number}. Status code: {response.status_code}")


df = pd.DataFrame(officers_list)
df.to_excel('company_officers.xlsx', index=False)

print("Data has been exported to 'company_officers.xlsx'.")
