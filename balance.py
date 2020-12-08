import sys
import random
from math import floor
import time

# Note: when we say current, we mean the processor whose load balancing activity it is currently
# and we are checking the left neighbor (left processor) and right neighbor (right processor) of this processor.


# generate a uniformly distributed random number between the low and high input values
def generate_random_number(low, high):
    return int(round(random.uniform(low, high)))


# check if both neighbors are balanced.
# balance among neighbours is reached when the neighbors on both sides' load units
# differ by 2 or less with the processor we are checking
def balanced_among_neighbors(left_neighbor, curr, right_neighbor):
    if abs(left_neighbor - curr) > 2 or abs(right_neighbor - curr) > 2:
        return False
    return True


# check if the load units of two neighboring processors are balanced
# balanced is when the load units differ by 2 or less
def balanced_neighbors(neighbor, curr):
    if curr - neighbor > 2:
        return False
    return True


# check for overall system balance
# system is balanced when every processor differs by at most 2 load units with its two neighbors
# if every processor fulfills the above condition, overall system balance is reached
def balanced_system():
    for i in range(len(processor_data)):
        # get the left, current and right processor load values
        if i == 0:
            left_neighbor_load = processor_data[len(processor_data) - 1][0]
            right_neighbor_load = processor_data[i + 1][0]
        elif i == len(processor_data) - 1:
            left_neighbor_load = processor_data[i - 1][0]
            right_neighbor_load = processor_data[0][0]
        else:
            left_neighbor_load = processor_data[i - 1][0]
            right_neighbor_load = processor_data[i + 1][0]
        curr_load = processor_data[i][0]

        # if neighbors are not balanced, we return false to continue balancing
        if abs(curr_load - left_neighbor_load) > 2 or abs(right_neighbor_load - curr_load) > 2:
            return False
    return True


# check whether the termination conditions (overall system balanced or time limit exceeded) are met
def check_termination():
    # check overall system balance
    if balanced_system():
        print("Number of cycles executed: " + str(time_index))
        print("The balanced matrix: " + str(processor_data))
        exit(0)

    # check time limit exceeded
    end_time = time.time()
    if (end_time - start_time) / 60 >= 5:
        print("Time limit exceeded")
        print("Number of cycles executed: " + str(time_index))
        print("The final matrix: " + str(processor_data))
        exit(0)


#  get the balance between the left and the current neighbor
def left_balance(left, current):
    avg = floor((left + current) / 2)
    num_to_give = current - avg
    left = left + num_to_give
    current = current - num_to_give
    return left, current


#  get the balance between the right and the current neighbor
def right_balance(right, current):
    avg = floor((right + current) / 2)
    num_to_give = current - avg
    right = right + num_to_give
    current = current - num_to_give
    return right, current


# get the indices of the neighbours to get the load values
def get_neighbor_indices(proc_index):
    if proc_index == 0:
        left_idx = len(processor_data) - 1
        right_idx = proc_index + 1
    elif proc_index == len(processor_data) - 1:
        left_idx = proc_index - 1
        right_idx = 0
    else:
        left_idx = proc_index - 1
        right_idx = proc_index + 1
    return left_idx, right_idx


# get number of processors from the input argument
number_of_processors = int(sys.argv[1])

# initialise the processor matrix
processor_data = [[0 for i in range(2)]] * number_of_processors

# generate initial random load and time interval values respectively in the processor matrix
for i in range(0, number_of_processors):
    processor_data[i] = [generate_random_number(10, 1000), generate_random_number(100, 1000)]

print("The initial matrix: " + str(processor_data))

# start timing so we can break out of the run if system is taking a long time to converge
start_time = time.time()

time_index = 100

# loop representing the run to balance the system
while True:
    # loop through every processor and check if time interval of processor matches the current time interval
    for proc_idx in range(len(processor_data)):
        if processor_data[proc_idx][1] == time_index:
            # set the next time interval value of the processor (current time value + random number)
            processor_data[proc_idx][1] += generate_random_number(100, 1000)

            # get the indices of the neighbours to get the load values
            left_index, right_index = get_neighbor_indices(proc_idx)

            # get load values from processor array
            left_load = processor_data[left_index][0]
            current_load = processor_data[proc_idx][0]
            right_load = processor_data[right_index][0]

            # if the neighbors are not balanced, then we need to do the balancing
            if not balanced_among_neighbors(left_load, current_load, right_load):
                if left_load < current_load <= right_load:
                    # balance the left and current
                    left_load, current_load = left_balance(left_load, current_load)
                elif left_load >= current_load > right_load:
                    # balance the right and current
                    right_load, current_load = right_balance(right_load, current_load)
                elif left_load < current_load and current_load > right_load:
                    # if current is greater than left and right, we need to try and give to both left and right
                    if left_load > right_load:
                        # give to right
                        right_load, current_load = right_balance(right_load, current_load)
                        if not balanced_neighbors(left_load, current_load):
                            # if left and current are not balanced, then give from current to left
                            left_load, current_load = left_balance(left_load, current_load)
                    elif right_load > left_load:
                        # give to left
                        left_load, current_load = left_balance(left_load, current_load)
                        if not balanced_neighbors(right_load, current_load):
                            # if right and current are not balanced, then give from current to right
                            right_load, current_load = right_balance(right_load, current_load)

                # reset the loads after the balancing
                processor_data[left_index][0] = left_load
                processor_data[proc_idx][0] = current_load
                processor_data[right_index][0] = right_load

        # check if our run needs to terminate
        check_termination()

    # increment the time interval
    time_index += 1
