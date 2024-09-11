# import requests
# import pandas as pd
#
# company_numbers = 14295314
#
# #["14295314", "14295313", "14319761", "14339152", "14311212", "13304203", "14084681", "14253404","14301335", "14290244", "13890037", "14316433", "14319857", "14319824", "14236305", "14237402","13562968", "12851410"]
# api_key = "03ed5851-da50-4a59-9c87-d903055fd3e6"
#
# url = f"https://api.company-information.service.gov.uk/company/{company_numbers}/officers"
#
# response = requests.get(url,auth=(api_key,''))
#
#
# data = response.json()
#
# officer_list = data.get('items',[])
#
# df = pd.DataFrame(officer_list)
#
# df.to_excel("officers_info.xlsx",index=False)
# print("Done")

import requests
import pandas as pd
import time

# List of company numbers
company_numbers = [
    "14295314", "14295313", "14319761", "14339152", "14311212",
    "13304203", "14084681", "14253404", "14301335", "14290244",
    "13890037", "14316433", "14319857", "14319824", "14236305",
    "14237402", "13562968", "12851410"

]

api_key = "03ed5851-da50-4a59-9c87-d903055fd3e6"
base_url = "https://api.company-information.service.gov.uk/company/"

all_officers = []

for company_number in company_numbers:
    url = f"{base_url}{company_number}/officers"
    response = requests.get(url, auth=(api_key, ''))

    if response.status_code == 200:
        data = response.json()
        officer_list = data.get('items', [])

        for officer in officer_list:
            officer['company_number'] = company_number
            all_officers.append(officer)
    else:
        print(f"Failed to retrieve data for company {company_number}: {response.status_code}")

    time.sleep(1)


df = pd.DataFrame(all_officers)
df.to_excel("officers_info_One.xlsx", index=False)
print("Data export completed!")
