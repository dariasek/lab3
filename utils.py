import numpy as np

matrix_0 = np.array([[1, 1, 1],
       				[1, 0, 1],
       				[1, 0, 1],
       				[1, 0, 1],
       				[1, 1, 1]])

matrix_1 = np.array([[0, 1, 0],
       				[0, 1, 0],
       				[0, 1, 0],
       				[0, 1, 0],
       				[0, 1, 0]])

matrix_2 = np.array([[1, 1, 1],
       				[0, 0, 1],
       				[1, 1, 1],
       				[1, 0, 0],
       				[1, 1, 1]])

matrix_3 = np.array([[1, 1, 1],
				     [0, 0, 1],
				     [1, 1, 1],
				     [0, 0, 1],
			         [1, 1, 1]])


matrix_4 = np.array([[1, 0, 1],
			       [1, 0, 1],
			       [1, 1, 1],
			       [0, 0, 1],
			       [0, 0, 1]])

matrix_5 = np.array([[1, 1, 1],
			       [1, 0, 0],
			       [1, 1, 1],
			       [0, 0, 1],
			       [1, 1, 1]])

matrix_6 = np.array([[1, 1, 1],
			       [1, 0, 0],
			       [1, 1, 1],
			       [1, 0, 1],
			       [1, 1, 1]])

matrix_7 = np.array([[1, 1, 1],
			       [0, 0, 1],
			       [0, 1, 0],
			       [1, 0, 0],
			       [1, 0, 0]])


matrix_8 = np.array([[1, 1, 1],
			       [1, 0, 1],
			       [1, 1, 1],
			       [1, 0, 1],
			       [1, 1, 1]])


matrix_9 = np.array([[1, 1, 1],
			       [1, 0, 1],
			       [1, 1, 1],
			       [0, 0, 1],
			       [0, 0, 1]])

int_to_image_list = [matrix_0,matrix_1,matrix_2,matrix_3,matrix_4,matrix_5,matrix_6,matrix_7,matrix_8,matrix_9]

def get_true_images(width_scale,height_scale):
	int_to_image_list_ = list()
	for i in range(len(int_to_image_list)):
	    int_to_image_list_.append(np.repeat(
	        np.repeat(int_to_image_list[i],width_scale,axis=0),height_scale,axis=1))
	return int_to_image_list_


def generate_noised_images_list(width,height,ethalon_matrices_list,p):
    """Add a noise to the ethalon images.
    Args:
        width - (int)
        height - (int)
        p - (float) probability of a noise
        ethalon_matrices_list - a list of a ethalon matrices
    Returns:
        noised_images - a list of a noised matrices, length tha same as in the 'ethalon_matrices_list'
    """
    noised_images = list()
    for matrix in ethalon_matrices_list:
        noise = np.random.choice(a=[0, 1], size=(width,height), p=[p, 1-p])
        noised_image = matrix^noise
        noised_images.append(noised_image)
    return noised_images


def calculate_prob(x_noised,true_matrices_list,histogram,target_index,p):
    """Due to the seminar notation, this fuction try to calculate p(x_noised,true_matrices_list[target_index])
    Args:
        x_noised - ndarray 100*120
        true_matrices_list - the list of 10 ndarray 100*120
        histogram - the list of 10 probabilities for each digit
        target_index - int in {0,..,9}
        p - float in [0,1]
    
    """
    xor_target = x_noised^true_matrices_list[target_index]
    result_sum = 0
    for index_matrix,true_matrix in enumerate(true_matrices_list):
        xor_matrix = x_noised^true_matrix
        # the equation from the seminar
        power_ = (xor_matrix - xor_target).sum()
        result_sum += histogram[index_matrix]*((1-p)/p)**power_
    return histogram[target_index]/result_sum


def calc_prob_list(noised_image,int_to_image_list,histogram,p):
    """Calculate a list of possibilities that digit_index corresponds to [0,..,9] 
    """
    possible_sum = list()
    for i in range(10):
        prob = calculate_prob(noised_image,int_to_image_list,histogram,i,p)
        possible_sum.append(prob)
    return possible_sum

def calc_partial_sum(previous_probs_list,current_probs_list,t):
    """This function is convolution when dimension = 2.
    Args:
        previous_probs_list - a list of length = 9*t +1,where at position i, the probability, that the
            first (t-1) digits' sum = i
        current_probs_list -  a list of length = 10, ,where at position i, the probability, that the
            t-th digit equals to i
        t - (int), denotes current position , we calculate sums for
    """
    predictions = list(np.zeros((9*(t+1) +1)))
    for current_value,current_prob in enumerate(current_probs_list):
        for prev_value,prev_prob in enumerate(previous_probs_list):
            predictions[current_value + prev_value] += current_prob*prev_prob
    return predictions


def sum_digits(number):
    """Calcuate the sum of digits in 'number'
    """
    digits_sum = 0
    while number:
        digits_sum += number % 10
        number //= 10
    return digits_sum

def generate_histogram(n):
    """generate histogram of length n"""
    generated_seq = np.random.rand(n)
    return (generated_seq/np.sum(generated_seq))
   