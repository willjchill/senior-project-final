import asyncio
import os
import csv
from bleak import BleakScanner, BleakClient
import numpy as np # for FFTs
from live_EMG_interpreter import live_interpret
import keyboard
import pywt
                                                                                                                                                                                                                                      
# Important address from Bluefruit chip
target_mac_address = "F4:7D:A4:2C:1E:EE" 
SERVICE_UUID = "6e400001-b5a3-f393-e0a9-e50e24dcca9e"
TX_CHARACTERISTIC_UUID = "6e400002-b5a3-f393-e0a9-e50e24dcca9e"
RX_CHARACTERISTIC_UUID = "6e400003-b5a3-f393-e0a9-e50e24dcca9e"

# Store samples to store in a file later
voltage_samples = []
sample_time = 1
current_file_path = os.path.abspath(os.getcwd())
num_save_rest = 0
num_save_contract = 0
samples_so_far = 0

def write_data():
    # creating training set
    global num_save_contract
    global num_save_rest
    global samples_so_far
    # label = "rest"                                                                                                                                                                                                                                                                                                                                                                                                                 
    # label_folder = r'\rest_filtered_v3'
    # if keyboard.is_pressed('space'):                                                                                                                                                                                                                      
    #     label = "contraction"
    #     label_folder = r'\contraction_filtered_v3'
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
    #print("Writing samples to file at ..") # debug message
    #print(current_file_path + r'\voltageTest.csv')
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
    # DSP (initially tested on MATLAB)        
    processed_signal = voltage_samples[0:1000]                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
    processed_signal = processed_signal - np.mean(processed_signal)
    wavelet = 'db1'  
    level = 3       
    processed_signal = pywt.mra(processed_signal, wavelet, level)
    processed_signal = np.array(processed_signal)

    # regular use
    np.savetxt(current_file_path + r'\voltageTest.csv', [row[-100:] for row in processed_signal], delimiter=',')
    live_interpret()

    # creating training set
    # if(samples_so_far > 100):
    #     if(label == "rest"):
    #         num_save_rest = num_save_rest + 1
    #         np.savetxt(current_file_path + label_folder + '\\emg_' + label + str(num_save_rest) + '.csv', [row[-100:] for row in processed_signal], delimiter=',')
    #     else:
    #         num_save_contract = num_save_contract + 1
    #         np.savetxt(current_file_path + label_folder + '\\emg_' + label + str(num_save_contract) + '.csv', [row[-100:] for row in processed_signal], delimiter=',')
    #     samples_so_far = 0
                                                                                                                 
#scans for the device
async def scan_for_device():
    print("Scanning for nearby BLE devices...")
    devices = await BleakScanner.discover()
    for device in devices:
        if device.address == target_mac_address:
            print("Found target device:", device.name)
            return device
    print("Target device not found.")
    return None

#connects to device
async def connect_to_device(device):
    if device is None:
        return None
    print("Connecting to target device...")
    client = BleakClient(device)
    try:
        await client.connect()
        print("Connected to target device successfully!")
        return client
    except Exception as e:
        print("Failed to connect to target device:", e)
        return None

#read sensor value when updated in callback
def notification_callback(sender, data):
    global voltage_samples
    global samples_so_far
    if(len(data) % 3 == 0): # check for faulty data
        for i in range(0, len(data), 3):
            #print(f"Received notification: {data[i:i+3]}")
            sample = int(data[i:i+3].decode('utf-8'), 16)   # convert to integer
            # print(f"Received notification: {sample}")
            if(sample <= 1023):  # append sample if it is reasonable
                if(len(voltage_samples) <= sample_time*1000): # "loading" not done yet
                    voltage_samples.append(sample)
                else: # loading complete
                    voltage_samples = voltage_samples[1:] # shift all values to the left
                    voltage_samples.append(sample) # add new sample to end
                    if(samples_so_far > 100):
                        write_data()  
                        samples_so_far = 0 
                    else:
                        samples_so_far = samples_so_far + 1

async def main():
    target_device = await scan_for_device()
    if target_device:
        client = await connect_to_device(target_device)
        #THIS IS THE CODE THAT WILL RUN ONCE CONNECTED!
        if client:
            # # DEBUGGING
            for service_obj in client.services:
                print("-----")
                print("SERVICE: ")
                print(service_obj)

            for char_obj in client.services.characteristics.values():
                    print("-----")
                    print("DESCRIPTION: " + char_obj.description)
                    print("UUID: " + char_obj.uuid)
                    print(char_obj.properties)
            await client.start_notify(RX_CHARACTERISTIC_UUID, notification_callback)
            print("Loading...")
            await asyncio.sleep(sample_time+1) # let the main thread take some time to "Load"
            print("Done Loading.")
            print("You are now resting.")
            while True:
                # put main thread to sleep for as long as possible
                await asyncio.sleep(sample_time*100000)
                # if(len(voltage_samples) >= sample_time*1000):
                #     write_data()     
        else:
            print("Failed to connect to target device.")
    else:
        print("Exiting.")

if __name__ == "__main__":
    asyncio.run(main())
