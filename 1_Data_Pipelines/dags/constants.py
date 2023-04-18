
# File path declaration

input_path = "input/"
output_path = "output/"
success_dir = "successful"
failed_dir = "unsuccessful"

input_file_names = ["applications_dataset_{}.csv".format(x) for x in [1, 2]]

# validate mobile number range
min_range = 9999999
max_range = 100000000

# Ignore Salutations and Degree
name_prefix_list = ["Dr", "Miss", "Mr.", "Mrs.", "Ms."]
name_suffix_list = ["MD", "I", "II", "III", "DDS"]

# Age Calculation date
min_age_date = "2022-01-01"
age_criteria = 18

# - Email validator
valid_email_list = ["com", "net"]

# variable list

# Successful application
final_col_list = ['membership_id', 'first_name', 'last_name', 'date_of_birth', 'email', 'mobile_no', 'above_18']
