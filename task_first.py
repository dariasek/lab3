import asyncio
import websockets
import numpy as np

def parsing_numbers(f,orig_1,orig_2,N):                            # parsing  numbers
	f = str(f)                                                
	f = f[f.find("n")+1:].split("\\n")                             # starting from looking for first "n" and spliting "\\n"
	f[-1] = f[-1][:-1]                                             # deleting last symbol " ' "  
	for i in range(orig_1,len(f),orig_1 +1):                       # changing digits on "#"
		f[i] = "#"
		
	f = [x for x in f if x != "#"]                                 # deleting every "#"
	a = []
	for i in range(0,len(f), orig_1):                              # parsing every matrix             
		if i==0:
			a.append(f[0:orig_1])
		else:
			a.append(f[i:i+orig_1])
		#print(a[i])
		#print(" ")
	numb = [0]*N                                                   #creating [numb] with N- length- the list whiich contains every matrix

	for i in range(0,len(a)):                                      # adding and spliting by " " every row in every matrix
		e = []
		for j in a[i]:
			e.append([int(j) for j in j.split(" ")])
			u = np.array(e)
		numb[i] = u                                                # adding etalone matrix to numb
	return numb

def parsing_task(x):                                               # the function which parses task-matrix which has to be recognized
	x = str(x)
	global STEP
	STEP = x[2:x.find("n")-1]                                      # starting from looking for first "n" and spliting "\\n"
	x = x[x.find("n")+1:].split("\\n")
	x = list(x)
	x[-1] = x[-1][:-1]                                             # deleting last symbol " ' "  
	g = []
	for i in x:
		g.append([int(i) for i in i.split(" ")])                   # adding and spliting by " " every row in task-matrix
	return np.array(g)                                             # creating numpy array from g
"""
def bigger_digit(orig_array,dig_1, dig_2):                         # function for first version of first_task that scales etalone-matrix to shape of task-matrix 
	d = np.array([])
	for i in range(0,orig_array.shape[0]):
		for j in range(0,orig_array.shape[1]):
			if j == 0:
				c  = np.full((dig_1, dig_2),  orig_array[i][j])
			else:
				c = np.concatenate((c,  np.full((dig_1, dig_2),  orig_array[i][j]   )) , axis = 1)
		d = np.append(d,c.reshape(1,c.shape[0]*c.shape[1]))
	d = d.reshape(dig_1*orig_1,dig_2*orig_2)
	d = d.astype('int64') 
	return d
"""
def recognition(task,cor, dig_1, dig_2, numbers):  # the main function recognition: task - task-matrix, dig_1, dig_2 - scale,numbers  - [numb]
	prob = []
	for i in numbers:
		d = []
		noise = np.bitwise_xor(i, task)                                      #Xoring matrixes
		
		noise = noise.reshape(1, noise.shape[0]*noise.shape[1])              # changing noise- matrix by reshaping into vector with 1 row
		
		for j in range(0, noise.shape[0]*noise.shape[1]):                    # calculating of probabilities
			if noise[0][j] == 0:
				d.append(1-cor)
			else:
				d.append(cor)
		prob.append(sum(np.log10(d)))                                        # creating [prob]- the list of calculated probabilities of each matrix
	#print(prob)
	return prob.index(max(prob))                                             # returning  index at which our guesed number located

async def get_numbers(width_scale,height_scale):
	uri = "wss://sprs.herokuapp.com/first/hide_the_pain_harold"              # hide_the_pain_harold - session id, what you've typed in Task 1
	async with websockets.connect(uri) as websocket:
		msg = "Let's start"
		await websocket.send(msg)
		tsk = await websocket.recv()                                         # Receiving a string [width] [height] [N] from the server
		global orig_1,orig_2                                                 # orig 1, orig 2 - shapes of etalone-matrixes
		orig_2, orig_1, N = [int(i) for i in tsk.split(" ")]                 # N - number of etalone-matrixes
		settings = "{} {} 1 1 off".format(width_scale,height_scale)
		
		dig_2, dig_1, cor, totalSteps, shuffle = [str(i) for i in settings.split(" ")]             # these parameters were discribed in documentation
		dig_2 = int(dig_2)
		dig_1 = int(dig_1)
		cor = float(cor)
		totalSteps = int(totalSteps)
		
		await websocket.send(settings)
		tsk = await websocket.recv()

		numbers = parsing_numbers(bytes(tsk,"utf-8"), orig_1*dig_1,orig_2*dig_2,N)
		return numbers             

# asyncio.get_event_loop().run_until_complete(hello())