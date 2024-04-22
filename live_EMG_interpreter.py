import torch
import pandas as pd
import numpy as np
from EMGModel import EMGModel
from live_csvcompiler import convert_csv
import warnings
import time
import os
import mouse 

warnings.filterwarnings("ignore", category=DeprecationWarning)
current_file_path = os.path.abspath(os.getcwd())

#model directory
model_file = current_file_path + r'\EMG_trained.pth'
#for live csv compiler
input_file = current_file_path + r'\voltageTest.csv'

model = EMGModel()  # Create an instance of your model
model.load_state_dict(torch.load(model_file))  #CHANGE

contract = False

def live_interpret():
    global contract
    # Read data from preprocessed data
    data = pd.read_csv(input_file,dtype=float,header=None)
    #print(data.head())

    # Convert data to NumPy array
    X_test = data.values
    # Convert NumPy array to PyTorch tensor
    X_test = X_test.reshape(-1, 100, 4)
    X_test = torch.FloatTensor(X_test) #CHANGE TO SPLIT/NOT SPLIT
    X_test = X_test.unsqueeze(1)

    # Perform inference with your model
    # Assuming model is already loaded and ready for inference
    with torch.no_grad():
        predictions = model(X_test)

    # Process predictions as needed
    # For example, print the predictions or perform further analysis
    print(predictions)

    rest_val, contraction_val = predictions[0]

    if rest_val > contraction_val:
        if(contract):
            print("You are now resting.")
        contract = False
    else:
        if(not contract):
            print("You are now contracting.")
            mouse.click(button='right')

        contract = True


if __name__ == "__main__":
    while True:
        live_interpret()
        time.sleep(0.5) 
