import sys
import random
from math import floor
import time


def generateRandomNumber(low, high):
    return int(round(random.uniform(low, high)))


def balancedNeighbors(leftNeighbor, cur, rightNeighbor):
    if abs(leftNeighbor - cur) > 2 or abs(rightNeighbor - cur) > 2:
        return False
    return True


def balancedOnOneSide(neighbor, curr):
    if curr-neighbor > 2:
        return False
    return True


def balanced():
    for i in range(len(proc_array)):
        if i == 0:
            leftneighbor = proc_array[len(proc_array) - 1][0]
            rightneighbor = proc_array[i + 1][0]
        elif i == len(proc_array) - 1:
            leftneighbor = proc_array[i - 1][0]
            rightneighbor = proc_array[0][0]
        else:
            leftneighbor = proc_array[i - 1][0]
            rightneighbor = proc_array[i + 1][0]
        curr = proc_array[i][0]
        if abs(curr - leftneighbor) > 2 or abs(rightneighbor - curr) > 2:
            return False
    return True


k = int(sys.argv[1])

proc_array = [[0 for i in range(2)]] * k

for i in range(0, k):
    proc_array[i] = [generateRandomNumber(10, 1000), generateRandomNumber(100, 1000)]

print(proc_array)
start = time.time()
index = 100
while True:
    for proc_id in range(len(proc_array)):
        if proc_array[proc_id][1] == index:
            proc_array[proc_id][1] += generateRandomNumber(100, 1000)
            if proc_id == 0:
                left_index = len(proc_array) - 1
                right_index = proc_id + 1
            elif proc_id == len(proc_array) - 1:
                left_index = proc_id - 1
                right_index = 0
            else:
                left_index = proc_id - 1
                right_index = proc_id + 1

            left = proc_array[left_index][0]
            current = proc_array[proc_id][0]
            right = proc_array[right_index][0]

            if not balancedNeighbors(left, current, right):
                if left < current < right:
                    avg = floor((left + current) / 2)
                    numToGive = current - avg
                    left = left + numToGive
                    current = current - numToGive
                elif left > current > right:
                    avg = floor((right + current) / 2)
                    numToGive = current - avg
                    right = right + numToGive
                    current = current - numToGive
                elif left < current > right:
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

                proc_array[left_index][0] = left
                proc_array[proc_id][0] = current
                proc_array[right_index][0] = right

        end = time.time()
        if balanced() or ((end - start) / 60 >= 2):
            print("The number of cycles executed: " + str(index))
            print("The matrix after initializing : " + str(proc_array))
            exit(0)
    index += 1
