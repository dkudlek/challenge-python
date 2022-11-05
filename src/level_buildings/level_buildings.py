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
Given a list of building hights.
Select the building hight that minimizes the number of removed levels.
For each building smaller than the selected building, we remove all levels.
For each building higher than the selected building, we remove all levels above the selected building height. 

Input: [1, 2, 3, 4, 5]
         _
       _|x|                        S - Selected building height
     _|x|x|            _ _ _       x - Demolish levels  
   _|o|o|o|     ->    |o|o|o|      o - keep levels 
 _|x|o|o|o|           |o|o|o|      
|x|x|o|o|o|        _ _|o|o|o|         
 0 1 2 3 4
     S

Return minimal number of demolished levels

Trival: 
- For each building height, test result: O(N * (N-1))

Better solution: 
- Sort the building heights: O(N log N)
- Memoization: Integrate building height over the list: O(N) 
- For each possible building height, we can check the number of levels by taking the 
    - left value: number of levels up to the selected building which we need to remove
    - last value: Total number of levels of all builds where substract the left value and the height of the selected buildings times the number of building after the selected building
- Walk over all levels and pick the best: O(N)

Total: O(N log N) + O(N) + O(N) = O(N log N)

Notes:
- input: [1, 2, 3, 4, 5]
- integrated: [1, 3, 6, 10, 15]
- Select idx: 2, height: 3
- val[idx-1] = 3 Levels need to be removed
- val[end] = 15 - val[idx] - (len(integrated) - 1 - idx ) * input[idx]
           = 15 - 6 - (5 - 1 - 2) * 3 = 9 - (2 * 3) = 3 

"""
import time
import random
from enum import Enum 

class Methode(Enum):
    NAIVE=1
    DYNAMIC=2


def naive_approach(list_of_building_heights):
    """
    Naive approach: O(N * N)
    """
    min_demolished_levels = None
    for selected_height in list_of_building_heights:
        demolished_levels = 0
        for height in list_of_building_heights:
            if height >= selected_height: 
                demolished_levels += (height - selected_height)
            else: 
                demolished_levels += height
        if min_demolished_levels is None or demolished_levels < min_demolished_levels:
            min_demolished_levels = demolished_levels
    return min_demolished_levels

def dynamic_approach(list_of_building_heights):
    """
    Dynamic approach with: O(N*log(N)) + O(N) + O(N) ~ O(N*log(N))
    (1) Sort: O(N*log(N))
    (2) Integrate: O(N)
    (3) Find min: O(N)

    """
    # Sort
    sorted_building_heights = sorted(list_of_building_heights)
    # Memoization
    integrate_building_heights = []
    accu = 0
    for el in sorted_building_heights:
        accu = accu + el 
        integrate_building_heights.append(accu)

    min_demolished_levels = None
    for idx, height in enumerate(sorted_building_heights):
        left_levels = 0
        if idx > 0:
            left_levels = integrate_building_heights[idx-1]
        last_idx = len(integrate_building_heights) - 1
        right_levels = integrate_building_heights[last_idx] - integrate_building_heights[idx] - ((last_idx - idx) * height)
        demolished_levels = left_levels + right_levels
        if min_demolished_levels is None or demolished_levels < min_demolished_levels:
            min_demolished_levels = demolished_levels
    return min_demolished_levels

def level_buildings(list_of_building_heights, methode):
    if not list_of_building_heights:
        print("[WARN   ] List is empty!")
        return None 
    elif not all(el >= 0 for el in list_of_building_heights):
        print("[ERROR  ] Negative building heights! Invalid!")
        return None
    elif len(list_of_building_heights) == 1:
        print("[INFO   ] Only one element!")
        return 0
    elif methode == Methode.NAIVE:
        return naive_approach(list_of_building_heights)
    elif methode == Methode.DYNAMIC:
        return dynamic_approach(list_of_building_heights)


def sanity_check():
    print("[RUN    ] Sanity check")
    """
             _
           _|x|                       
         _|x|x|           
       _|o|o|o|      
     _|x|o|o|o|     
    |x|x|o|o|o|              
     0 1 2 3 4
         S
    """
    building_heights = [1, 2, 3, 4, 5]
    min_levels = 6
    assert(min_levels == level_buildings(building_heights, Methode.NAIVE))
    assert(min_levels == level_buildings(building_heights, Methode.DYNAMIC))
    """
             _
            |x|
            |x|
            |x| 
           _|x|                       
          |o|o|
          |o|o|
          |o|o|           
          |o|o|      
     _ _ _|o|o|     
    |x|x|x|o|o|              
     0 1 2 3 4
           S
    """
    print("[SUCCESS] Sanity check: Default test")
    building_heights = [1, 1, 1, 6, 10]
    min_levels = 7
    assert(min_levels == level_buildings(building_heights, Methode.NAIVE))
    assert(min_levels == level_buildings(building_heights, Methode.DYNAMIC))
    """
     _ _ _ _ _ 
    |o|o|o|o|o|
    |o|o|o|o|o|
    |o|o|o|o|o| 
    |o|o|o|o|o|                       
    |o|o|o|o|o|
    |o|o|o|o|o|
    |o|o|o|o|o|           
    |o|o|o|o|o|      
    |o|o|o|o|o|     
    |o|o|o|o|o|              
     0 1 2 3 4
     S    
    """
    print("[SUCCESS] Sanity check: non linear building heights successfull")
    building_heights = [10, 10, 10, 10, 10]
    min_levels = 0
    assert(min_levels == level_buildings(building_heights, Methode.NAIVE))
    assert(min_levels == level_buildings(building_heights, Methode.DYNAMIC))
    """
             _
            |o|
            |o|
            |o| 
            |o|                       
            |o|
            |o|
            |o|           
            |o|      
            |o|     
     _ _ _ _|o|              
     0 1 2 3 4
             S
    """
    print("[SUCCESS] Sanity check: equal building heights successfull (pick first)")
    
    building_heights = [0, 0, 0, 0, 10]
    min_levels = 0
    assert(min_levels == level_buildings(building_heights, Methode.NAIVE))
    assert(min_levels == level_buildings(building_heights, Methode.DYNAMIC))
    print("[SUCCESS] Sanity check: pick last")
    """
    Negative numbers
    """
    assert(level_buildings([1, -1], Methode.NAIVE) is None)
    assert(level_buildings([1, -1], Methode.DYNAMIC) is None)
    print("[SUCCESS] Sanity check: Negative levels")
    """
    Empty list
    """
    assert(level_buildings([], Methode.NAIVE) is None)
    assert(level_buildings([], Methode.DYNAMIC) is None)
    print("[SUCCESS] Sanity check: Empty list")
    """
    One element
    """
    assert(level_buildings([1], Methode.NAIVE) == 0)
    assert(level_buildings([1], Methode.DYNAMIC) == 0)
    print("[SUCCESS] Sanity check: Single Element")
    
def s_to_us(val):
    return int(round(val * 1000000))

def s_to_timeformat(val):
    hours = int(val // 360)
    minutes = int(val // 60)
    seconds = round(val, 6)
    return "{:02d}:{:02d}:{:09.6f}".format(hours, minutes, seconds)

def execute_test(list):
    print("[RUN    ] Execute test: naive approach")
    start = time.time()
    naive_result = level_buildings(list, Methode.NAIVE)
    end = time.time()
    delta_naive = end - start
    print("[SUCCESS] Execute test: naive approach with '{}'".format(naive_result))
    

    print("[RUN    ] Execute test: dynamic approach")
    start = time.time()
    dynamic_result = level_buildings(list, Methode.DYNAMIC)
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
        for _ in range(0, 10000):
            test_data.append(random.randrange(2**32))
        execute_test(test_data)

if __name__ == "__main__":
    sanity_check()
    execute_random_tests(3)
