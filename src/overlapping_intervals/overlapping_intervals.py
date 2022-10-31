"""
MIT License

Copyright (c) 2022 David Kudlek

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


"""
Given a list of intervals: 
We want to know if there's one interval which doesn't overlap with another interval

An interval overlaps if end of one and start of the other are the equal (closed interval, including start and end value)
e.g. 
- [0, 3] and [1, 2] overlap
- [0, 3] and [3, 5] overlap
- [0, 3] and [4, 6] don't overlap

Solutions :
(1) Naive Solution: O(N * N)
(2) Dynamic solution: O(N * log(N) + N) ~ O(N*log(N))

Total: Total: O(N log N) + O (N) + O(N log N) =  O(N log N)

Notes:
- tuple compare compares value by value:
(1, 2) < (2, 4), because 1 < 2
(1, 2) < (1, 3), because 1 == 1 and 2 < 3
(1, 2) > (0, 1), because 1 > 0

"""
import time
import random
import argparse
import csv

def overlaps(first_interval, second_interval):
    if second_interval[0] <= first_interval[1] and second_interval[1] >= first_interval[0]:
        return True
    elif first_interval[0] <= second_interval[1] and first_interval[1] >= second_interval[0]:
        return True
    return False

def naive_search(list_of_intervals):
    """
    Naive approach with: O(N * N)
        
    Compare each intervale with all other intervals.
    Early exit when we find one interval that doesn't overlap with an other interval from the
    list.
    
    """
    for idx, interval in enumerate(list_of_intervals):
        has_overlap = False
        for second_idx, second_interval in enumerate(list_of_intervals):
            if idx == second_idx:
                continue
            elif overlaps(interval, second_interval):
                has_overlap = True
                break # Early exit because we found an overlapping interval
        if not has_overlap:
            return (True, interval)
    return (False, None)

def tupelize(elem):
    return (elem[0], elem[1])

def dynamic_search(list_of_intervals):
    """
    Dynamic approach with: O(N*log(N)) + O(N) ~ O(N*log(N))
    (1) Sort the array: O(N log N)
    (2) Touch each element and compare to a memorized interval: O(N)

    Memoization technique: We use one interval to memorize all the intervals we've seen. When a
    interval overlaps with it then we grow this interval. This means for each element, we only
    need to compare against this interval. If it doesn't overlap then we create a new interval.
    If this is the last element or the next element does not overlap then we found an interval
    that doesn't overlap with any other interval.
    Early exit when we find one interval that doesn't overlap with an other interval from the
    list.
    """
    list_of_intervals = sorted(list_of_intervals, key=tupelize)
    found = False
    low = 0
    high = 0
    idx_max = len(list_of_intervals) - 1
    for (idx, interval) in enumerate(list_of_intervals):
        if idx == 0: 
            low = interval[0]
            high = interval[1]
            found = True
            continue
        has_overlap = overlaps((low, high), interval)
        if has_overlap:
            if interval[1] > high:  
                high = interval[1]
            found = False
        else: 
            if idx == 1: 
                """ First is single """
                return (True, (low, high))
            elif idx == idx_max:
                """ Last is single """
                return (True, interval)
            elif found == True: 
                """ Single in the middle """
                return (True, (low, high))
            low = interval[0]
            high = interval[1]
            found = True

    return (False, None)

def sanity_check():
    """ Sanity check """
    print("[RUN    ] Sanity check")
    interval_a = (0, 4)
    interval_b = (3, 5)
    interval_c = (4, 5)
    interval_d = (6, 7)
    interval_f = (3, 6)
    """ Test helper functions """
    print("[RUN    ] Test helper functions")
    assert(overlaps(interval_a, interval_b))
    assert(overlaps(interval_b, interval_c))
    assert(overlaps(interval_a, interval_a))

    assert(not overlaps(interval_a, interval_d))
    assert(not overlaps(interval_b, interval_d))
    assert(not overlaps(interval_c, interval_d))
    print("[SUCCESS] Test helper functions")

def run_small_examples():
    """ Sanity check """
    unmatched_first = [(0,3), (4,6), (5,7), (7,10)]
    unmatched_last = [(4,6), (5,7), (7,10), (25,50)]
    unmatched_middle = [(3,5), (4,6),(7,9) ,(10,30), (10,20)]
    matched = [(1,3), (2,4), (3,5), (4,6)]
    
    print("[RUN    ] Sanity check: naive approach")
    result, interval = naive_search(unmatched_first)
    assert(result == True and interval == (0,3))
    result, interval = naive_search(unmatched_last)
    assert(result == True and interval == (25,50))
    result, interval = naive_search(unmatched_middle)
    assert(result == True and interval == (7,9))
    result, interval = naive_search(matched)
    assert(not result)
    print("[SUCCESS] Sanity check: naive approach")

    

    print("[RUN    ] Sanity check: dynamic approach")
    result, interval = dynamic_search(unmatched_first)
    assert(result == True and interval == (0,3))
    result, interval = dynamic_search(unmatched_last)
    assert(result == True and interval == (25,50))
    result, interval = dynamic_search(unmatched_middle)
    assert(result == True and interval == (7,9))
    result, interval = dynamic_search(matched)
    assert(not result)
    print("[SUCCESS] Sanity check: dynamic approach")

def s_to_min(val):
    return int(round(val /60))

def s_to_us(val):
    return int(round(val * 1000000))


def s_to_ms(val):
    return int(round(val * 1000))

def s_to_timeformat(val):
    hours = int(val // 360)
    minutes = int(val // 60)
    seconds = round(val, 6)
    return "{:02d}:{:02d}:{:09.6f}".format(hours, minutes, seconds)

def execute_test(list):
    print("[RUN    ] Execute test: naive approach")
    start = time.time()
    naive_result, interval = naive_search(list)
    end = time.time()
    delta_naive = end - start
    print("[SUCCESS] Execute test: naive approach with '{}'".format(naive_result))
    

    print("[RUN    ] Execute test: dynamic approach")
    start = time.time()
    dynamic_result, interval = dynamic_search(list)
    end = time.time()
    delta_dynamic = end - start
    print("[SUCCESS] Execute test: dynamic approach with '{}'".format(dynamic_result))

    assert(naive_result == dynamic_result)
    """Print results""" 
    print("[EVAL   ] Naive Approach took    {} || {:12}us".format(s_to_timeformat(delta_naive),s_to_us(delta_naive)))
    print("[EVAL   ] Dynamic Approach took  {} || {:12}us".format(s_to_timeformat(delta_dynamic), s_to_us(delta_dynamic)))

def execute_random_tests(n):
    for _ in range(0,n):
        test_data = []
        _ = random.seed()
        max_size = 2 ** 20
        for i in range(0, 1000000):
            rand_one = random.randrange(2**32)
            rand_two = random.randrange(2**32) 
            if rand_one > rand_two:
                delta = abs(rand_one - rand_two) - max_size
                if delta > 0:
                    rand_one = rand_two + max_size         
                test_data.append((rand_two, rand_one))
            else:
                delta = abs(rand_one - rand_two) - max_size
                if delta > 0:
                    rand_two = rand_one + max_size    
                test_data.append((rand_one, rand_two))
        execute_test(test_data)

def read_from_disk(file_name):   
    input_list = []
    with open(file_name, newline='') as csvfile:
        file_reader = csv.reader(csvfile, dialect='excel')
        for (idx, row) in enumerate(file_reader):
            if idx == 0:
                continue
            input_list.append((int(row[0]), int(row[1])))
    return input_list

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find an interval that doesn't overlap with any other interval in a list")
    parser.add_argument('--file-with-overlap', type=str, default="overlap.csv") 
    parser.add_argument('--file-without-overlap', type=str, default="no_overlap.csv") 
    parser.add_argument('--number-of-rand-runs', type=int, default=0) 
  
    args = parser.parse_args()


    sanity_check()
    run_small_examples()
    print("[#######]")
    print("[RUN    ] Test with overlap")
    example_with_overlap = read_from_disk(args.file_with_overlap)
    execute_test(example_with_overlap)
    print("[SUCCESS] Test with overlap")
    print("[#######]")
    print("[RUN    ] Test without overlap")
    example_without_overlap = read_from_disk(args.file_without_overlap)
    print("[SUCCESS] Test without overlap")
    execute_test(example_without_overlap)

    """ Start actual function """

    execute_random_tests(args.number_of_rand_runs)

