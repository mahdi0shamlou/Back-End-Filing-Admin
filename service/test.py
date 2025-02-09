from datetime import datetime

# Input date string
date_string = "2024-04-20 07:06:44"

# Parse the string into a datetime object
date_object = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")

# Convert the datetime object to a timestamp
timestamp = date_object.timestamp()

# Print the results
print("Datetime:", date_object)
print("Timestamp:", timestamp)