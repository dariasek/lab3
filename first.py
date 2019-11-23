import asyncio
import websockets

import numpy as np

def preprocess_input(input_string,w,h,n):
    index = 0
    list_digit_arrays = list()
    for digit in range(n):
        digit_array = list()
        for h_i in range(h):
            index+=2
            row = input_string[index:index+2*w-1]
            row = row.split(" ")
            row = [int(j) for j in row]
            digit_array.append(row.copy())
            index+= 2*w-2
        digit_array = np.array(digit_array)
        list_digit_arrays.append(digit_array.copy())
        index+=2
    return list_digit_arrays


async def get_numbers   (w,h,p=0.2,n_steps=1,mode='off'):
    uri = "wss://sprs.herokuapp.com/first/rot"  
    async with websockets.connect(uri) as websocket:
        # Connecting to server
        msg = "Let's start"
        await websocket.send(msg)
        # Receiving a string [width] [height] [N] from the server        
        parameters = await websocket.recv()
        #print("{}".format(parameters))
        width, height, N = [int(i) for i in parameters.split(" ")]
        # Processing manual input 
        #settings = input("input the settings: format -  [width] [height] [noise] [totalSteps] ")
        settings = str(w) + ' ' + str(h) + ' ' +str(p) + ' ' + str(n_steps) + ' ' + mode
        scale_width, scale_height, probability, number_steps,  _ = [str(i) for i in settings.split(" ")]
        width *= int(scale_width)
        height *= int(scale_height)
        number_steps = int(number_steps)
        probability = float(probability)
        # Sending input to the server
        await websocket.send(settings)
        # Getting labels( true digit matrices)
        labels_str = await websocket.recv()
        # Converting labels from str to list of numpy arrays
        labels_list = preprocess_input(labels_str,width,height,N)
        return labels_list         

