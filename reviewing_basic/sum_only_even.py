import random


# Creating the list to try the program
List_sizes = [5,10,15,30,40,50,100,120,150,1000]
Random_lists = [[random.randint(1,100) for _ in range (size)] for size in List_sizes]

# function to sum all even numbers in a list.
def sum_even_numbers(nums: list) -> int:
    return sum(num for num in nums if num % 2 == 0)

# Calculate sums of even numbers on each list
List_sums = [sum_even_numbers(List) for List in Random_lists]

# print the lists and their sums
for sums, Lists in zip(List_sums, Random_lists):
    print(f'List = {Lists}')
    print(f"Sum of list's even numbers: {sums}")
    print('')

print(f'List with the sums {List_sums}')


