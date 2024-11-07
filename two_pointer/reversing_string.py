# Write a function to reverse a string.
# Use the two-pointer technique.

def reverse_string(s:str) -> str:
    if not s:
        return s
    
    s = list(s)
    left = 0
    right = len(s) -1


    while left < right:
        s[left], s[right] = s[right], s[left]
        left += 1
        right -= 1
    return ''.join(s)

exercise=["hello", "world", "duck", "programming", "computer science","dictionary",
        "The quick brown fox jumps over the lazy dog",
        "CS50 is an introduction to the intellectual enterprises of computer science",
        "",
        "A journey of a thousand miles begins with a single step",
        "In the end, we will remember not the words of our enemies, but the silence of our friends"
]

answer = [reverse_string(s) for s in exercise]

print(answer)
