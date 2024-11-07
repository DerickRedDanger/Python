# 3. Given a string, write a function to return the character count for each character in a dictionary format.
# Example: char_count("hello") should return {'h': 1, 'e': 1, 'l': 2, 'o': 1}

from collections import defaultdict

def char_count(s: str) -> dict[str,int]:
    char_dic = defaultdict(int)
    for char in s:
        char_dic[char] += 1
    return char_dic


exercise=["hello", "world", "duck", "programming", "computer science","dictionary",
        "The quick brown fox jumps over the lazy dog",
        "CS50 is an introduction to the intellectual enterprises of computer science",
        "A journey of a thousand miles begins with a single step",
        "In the end, we will remember not the words of our enemies, but the silence of our friends"
]

answer = [char_count(string) for string in exercise]

for string in answer:
    print(f"{dict(string)}\n")

