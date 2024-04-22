import os
import csv

max_length = 400

current_file_path = os.path.abspath(os.getcwd())

# Directory containing the input CSV files
input_directory = current_file_path + r'\database_filtered' 
#input_directory = 'C:\\Users\\Jakeeer\\git\\senior_project\\machine learning p2\\test_database' #to compile to the test csv 
# Define the output CSV filename
output_filename = current_file_path + r'\emg_compiled.csv'
#output_filename = "C:\\Users\\Jakeeer\\git\\senior_project\\machine learning p2\\emg_compiled_test.csv" #compiled test csv

# Function to read data from multiple CSV files
def read_data_from_csv(files):
    data = []
    for file in files:
        label = os.path.basename(file).split('_')[1]  # Extract label from filename
        label = label.split('.')[0]  # Remove file extension
        label = ''.join([i for i in label if not i.isdigit()])  # Remove numbers
        with open(file, 'r') as f:
            reader = csv.reader(f)

            # Transpose the reader to iterate through columns
            columns = zip(*reader)
            
            values = []
            for column in columns:
                values += column

            # Append values along with the extracted label
            data.append({"signal": values, "label": label})
    return data

# Function to write data to CSV file
def write_to_csv(filename, data):
    # Determine the maximum length of signals
    #max_length = max(len(d["signal"]) for d in data)
    
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        
        # Write header
        header = [f"Point {i+1}" for i in range(max_length)]
        header.append("Label")
        writer.writerow(header)
        
        # Write data rows
        for d in data:
            # Truncate or pad the signal to match the maximum length
            truncated_signal = d["signal"][:max_length] + [0] * (max_length - len(d["signal"]))
            writer.writerow(truncated_signal + [d["label"]])

# List all CSV files in the directory
csv_files = [os.path.join(input_directory, f) for f in os.listdir(input_directory) if f.endswith('.csv')]

# Read data from CSV files
data = read_data_from_csv(csv_files)

# Write data to CSV file
write_to_csv(output_filename, data)

print(f"Data has been compiled and written to {output_filename}")
