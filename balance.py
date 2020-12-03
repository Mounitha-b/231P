import sys
import random
import time
import datetime
from math import floor


def generateRandomNumber(start, stop):
    return int(round(random.uniform(start, stop)))


def balancedNeighbors(i, j, k):
    if abs(i - j) > 2 or abs(k - j) > 2:
        return False
    return True


def balancedOnOneSide(neighbor, current):
    if abs(neighbor - current) > 2:
        return False
    return True



k = int(sys.argv[1])

proc_array = [[0 for i in range(2)]] * k

print("The matrix after initializing : " + str(proc_array))

for i in range(0, k):
    proc_array[i] = [generateRandomNumber(10, 1000), generateRandomNumber(100, 1000)]

print(proc_array)



for i in range(100, 1000000):
    for proc_id in range(len(proc_array)):
        # implement circular
        if proc_array[proc_id][1] == i:
            left = proc_array[proc_id - 1][0]
            current = proc_array[proc_id][0]
            right = proc_array[proc_id + 1][0]
            if not balancedNeighbors(left, current, right):
                if left < current < right:
                    avg = floor((left + current) / 2)
                    numToGive = current - avg
                    left = left + numToGive
                    current = current - numToGive
                if left > current > right:
                    avg = floor((right + current) / 2)
                    numToGive = current - avg
                    right = right + numToGive
                    current = current - numToGive
                if left < current > right:
                    if left > right:  # 200 500 2
                        avg = floor((right + current) / 2)
                        numToGive = current - avg
                        right = right + numToGive
                        current = current - numToGive
                        if not balancedOnOneSide(left, current):
                            avg = floor((left + current) / 2)
                            numToGive = current - avg
                            left = left + numToGive
                            current = current - numToGive
                    elif right > left:
                        avg = floor((left + current) / 2)
                        numToGive = current - avg
                        left = left + numToGive
                        current = current - numToGive
                        if not balancedOnOneSide(right, current):
                            avg = floor((right + current) / 2)
                            numToGive = current - avg
                            right = right + numToGive
                            current = current - numToGive

                proc_array[proc_id - 1][0] = left
                proc_array[proc_id][0] = current
                proc_array[proc_id + 1][0] = right
