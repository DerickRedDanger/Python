from typing import List, Set

# Using a set for quick look up and to store elements that appeared ad odd number of times
# While removing those that appear an even number of times


def lonelyinteger_set(lis: List[int]) -> Set[int]:
    # Write your code here
    
    # using a set because of their constant lookup time
    explored = set()

    for i in lis:
        # If an element appeared for the first time, add it to the set
        if i not in explored:
            explored.add(i)
        # If it appeared again, remove it
        elif i in explored:
            explored.remove(i)
            
    # returns the remaining element in the set
    return list(explored)

    
# Using XOR to reach the same effect, 
# but it only works when only 1 int appears a odd number of times
# otherwise it will only show the last int that appeared an odd number of times

def lonelyinteger_XOR(lis: List[int]) -> int:
    # Write your code here
    
    # Using XOR to find a single element that appeared an odd number of times
    
    # initializing result
    result = 0

    for i in lis:
        # When we XOR an number with 0, if it appeared an odd number of times,
        # the result will be the number itself, else, it will be 0
        result = result ^ i

        # For debugging and understanding purposes
        """
        print(f" i = {i}")
        print(f"Result = {result}")
        """
    return result



for i in range(2):

    if i % 2 == 0:
        print("List with one number appearing an odd number of times")
        lis = [1, 2, 3, 4, 3, 2, 1]
    
    else:
        print("List with 3 numbers appearing an odd number of times")
        lis = [1, 2, 3, 4, 5, 6, 7, 8, 6, 5, 3, 2, 1]

    print("Using sets")
    print (f"Result = {lonelyinteger_set(lis)}")

    print("Using Xor")
    print(f"Result = {lonelyinteger_XOR(lis)}")
    print("The reason why it's returning 11, is because 4 XOR 7 XOR 8 == 11")
    print("4 XOR 7 is 0100 XOR 0111 in binary, which equals 0011 or 3 in decimal.")
    print("Then, 3 XOR 8 is 0011 XOR 1000 in binary, which equals 1011 or 11 in decimal.")