# Open the file containing company numbers
with open('Companies_Reg_Num.txt', 'r') as file:
    # Read the contents of the file
    content = file.read()

# Remove extra spaces and new lines, split the numbers by commas
company_numbers = content.replace("'", "").replace("\n", "").split(',')

# Reformat the numbers inside double quotes and separated by commas
formatted_numbers = ', '.join(f'"{number.strip()}"' for number in company_numbers)

# Output the result
print(formatted_numbers)

# Optionally, you can save the formatted string back to a file
with open('formatted_company_numbers.txt', 'w') as output_file:
    output_file.write(formatted_numbers)
