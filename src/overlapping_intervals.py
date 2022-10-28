"""
Given a list of intervals: 
We want to know if there's one interval which doesn't overlap with another interval

An interval overlaps if end of one and start of the other are the equal (closed interval, including start and end value)
e.g. 
- [0, 3] and [1, 2] overlap
- [0, 3] and [3, 5] overlap
- [0, 3] and [4, 6] don't overlap

Trival: 
- For each interval, check overlap with all other intervals O(N*N)

Better Solution: 
- Sort intervals (with respect to start AND end value!): O(N log N)
- Loop through the intervals: O(N)
- For each (N) element, do a binary search find at least on overlapping interval or none: O(N log N)

Total: Total: O(N log N) + O (N) + O(N log N) =  O(N log N)

Notes:
- tuple compare compares value by value:
(1, 2) < (2, 4), because 1 < 2
(1, 2) < (1, 3), because 1 == 1 and 2 < 3
(1, 2) > (0, 1), because 1 > 0

"""
import time
import random
import sys
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt

def overlaps(first_interval, second_interval):
    if second_interval[0] <= first_interval[1] and second_interval[1] >= first_interval[0]:
        return True
    elif first_interval[0] <= second_interval[1] and first_interval[1] >= second_interval[0]:
        return True
    return False

def has_non_overlapping(list_of_intervals):
    for idx, interval in enumerate(list_of_intervals):
        has_overlap = False
        for second_idx, second_interval in enumerate(list_of_intervals):
            if idx == second_idx:
                continue
            elif overlaps(interval, second_interval):
                has_overlap = True
                break
        if not has_overlap:
            return (True, interval)
    return (False, None)

def tupelize(elem):
    return (elem[0], elem[1])

def binsearch_match(interval, list_of_intervals):
    low = 0
    high = len(list_of_intervals) - 1
    while low <= high:
        mid = (low+high)//2
        midval = list_of_intervals[mid]
        if low == high:  
            break
        if midval < interval:
            if interval != midval and overlaps(interval, midval):
                return True
            low = mid+1
        elif midval >= interval:
            if interval != midval and overlaps(interval, midval):
                """
                Skip the interval that we currently look at
                If it's equal we can look into the right branch
                """
                return True
            high = mid
        else:
            break
    return False 

def has_non_overlapping_with_sort(list_of_intervals):
    for interval in list_of_intervals:
        """
        Binary Search for each interval in our list
        """
        has_overlap = binsearch_match(interval, list_of_intervals)
        if not has_overlap:
            return (True, interval)
    return (False, None)

def has_non_overlapping_dynamic(list_of_intervals):
    found = False
    low = None 
    high = None
    if len(list_of_intervals) > 1:
            low = list_of_intervals[0][0]
            high = list_of_intervals[0][1]
    for idx in range(1, len(list_of_intervals)):
        interval = list_of_intervals[idx]
        has_overlap = overlaps((low, high), interval)
        if has_overlap: 
            high = interval[1]
            found = False
        else: 
            if idx == 1: 
                """ First is single """
                print("first")
                return (True, (low, high))
            elif idx == len(list_of_intervals) - 1:
                """ Last is single """
                print("last")
                return (True, (interval[0], interval[1]))
            elif found == True: 
                """ Single in the middle """
                print("middle")
                return (True, (list_of_intervals[idx-1][0], list_of_intervals[idx-1][1]))
            low = interval[0]
            high = interval[1]
            found = True

    return (False, None)


if __name__ == "__main__":
    interval_a = (0, 4)
    interval_b = (3, 5)
    interval_c = (4, 5)
    interval_d = (6, 7)
    interval_f = (3, 6)

    """ Test helper functions """
    assert(overlaps(interval_a, interval_b))
    assert(overlaps(interval_b, interval_c))
    assert(overlaps(interval_a, interval_a))

    assert(not overlaps(interval_a, interval_d))
    assert(not overlaps(interval_b, interval_d))
    assert(not overlaps(interval_c, interval_d))
    print("Test: overlaps success")


 
    """ Sanity check """
    print("sanity check")
    unmatched_first = [(0,3), (4,6), (5,7), (7,10)]
    unmatched_last = [(4,6), (5,7), (7,10), (25,50)]
    unmatched_middle = [(3,5), (4,6),(7,9) ,(10,30), (10,20)]
    matched = [(1,3), (2,4), (3,5), (4,6)]
    result, interval = has_non_overlapping(unmatched_first)
    assert(result == True and interval == (0,3))
    result, interval = has_non_overlapping(unmatched_last)
    assert(result == True and interval == (25,50))
    result, interval = has_non_overlapping(unmatched_middle)
    assert(result == True and interval == (7,9))
    result, interval = has_non_overlapping(matched)
    assert(not result)

    unmatched_first_sorted = sorted(unmatched_first, key=tupelize)
    unmatched_last_sorted = sorted(unmatched_last, key=tupelize)
    unmatched_middle_sorted = sorted(unmatched_middle, key=tupelize)
    matched_sorted = sorted(matched, key=tupelize)

    result, interval = has_non_overlapping_with_sort(unmatched_first_sorted)
    assert(result == True and interval == (0,3))
    result, interval = has_non_overlapping_with_sort(unmatched_last_sorted)
    assert(result == True and interval == (25,50))
    result, interval = has_non_overlapping_with_sort(unmatched_middle_sorted)
    assert(result == True and interval == (7,9))
    result, interval = has_non_overlapping(matched)
    assert(not result)
    

    result, interval = has_non_overlapping_dynamic(unmatched_first_sorted)
    assert(result == True and interval == (0,3))
    result, interval = has_non_overlapping_dynamic(unmatched_last_sorted)
    assert(result == True and interval == (25,50))
    result, interval = has_non_overlapping_dynamic(unmatched_middle_sorted)
    assert(result == True and interval == (7,9))
    result, interval = has_non_overlapping_dynamic(matched)
    assert(not result)

    """ Generate sets """
    print("Create data set")
    test_data = []
    gen = random.seed()
    for i in tqdm(range(0, 10000000)):
        rand_one = random.randrange(sys.maxsize)
        rand_two = random.randrange(sys.maxsize) 
        if rand_one > rand_two:
            test_data.append((rand_two, rand_one))
        else:
            test_data.append((rand_one, rand_two))

    """ Start actual function """
    print("Test naive approach")
    start = time.time()
    no_overlap_naive, interval = has_non_overlapping(test_data)
    print(no_overlap_naive, interval)
    end = time.time()
    delta_naive = end - start
    
    """ Sort """
    print("Sort")
    start = time.time()
    list_of_intervals = sorted(test_data, key=tupelize)   
    end = time.time()
    delta_sort = end - start

    """ Test optimised functions """
    print("Test optimized")

    start = time.time()
    no_overlap_optimized, interval = has_non_overlapping_with_sort(list_of_intervals)
    print(no_overlap_optimized, interval)
    end = time.time()
    delta_optimized = end - start

    """ Has overlapping dynamic """
    start = time.time()
    no_overlap_dynamic, interval =has_non_overlapping_dynamic(list_of_intervals)
    print(no_overlap_dynamic, interval)
    end = time.time()
    delta_dynamic = end - start

    """Print results""" 
    print("Test: has_non_overlapping success. Time: {} s".format(delta_naive))
    print("Test: has_non_overlapping_with_sort success. Time: {} + {} = {} ".format(delta_sort, delta_optimized, delta_sort + delta_optimized))
    print("Test: has_non_overlapping_with_sort success. Time: {} + {} = {}".format(delta_sort, delta_dynamic, delta_sort + delta_dynamic))


    assert(no_overlap_naive == no_overlap_optimized)
    assert(no_overlap_naive == no_overlap_dynamic)

    """
    fig, ax = plt.subplots(figsize=(6, 6))
    if no_overlap:
        x = []
        y = []
        x_special = []
        y_special = []
        for idx, el in enumerate(tqdm(sorted_list)):
            if el != interval: 
                y.append(idx)
                y.append(idx)
                y.append(None)
                x.append(el[0])
                x.append(el[1])
                x.append(None)
            else:  
                y_special.append(idx)
                y_special.append(idx)
                x_special.append(el[0])
                x_special.append(el[1])
        ax.plot(x, y, 'r', label='miss')
        ax.plot(x_special, y_special, 'b', label='hit')
    else:
        x = []
        y = []
        for idx, el in enumerate(tqdm(sorted_list)):
            y.append(idx)
            y.append(idx)
            y.append(None)
            x.append(el[0])
            x.append(el[1])
            x.append(None)
        ax.plot(x, y, 'r', label='miss')
    plt.show()
    """