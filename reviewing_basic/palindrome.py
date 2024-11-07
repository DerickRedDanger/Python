# Write a function to check if a given string is a palindrome.
def is_palindrome(s: str) -> bool:
    s1 = s.lower().replace(' ','').replace('.','')
    return s1 == s1[::-1]
        
# examples with answers
Exercise = [
        ("racecar",True),
        ("level", True),
        ("hello", False),
        ("world", False),
        ("A man a plan a canal Panama", True),
        ("Was it a car or a cat I saw", True),
        ("No lemon no melon", True),
        ("Able was I ere I saw Elba", True),
        ("Madam In Eden Im Adam", True),
        ("This is not a palindrome", False)
]

print(f"the output is in the format:")
print("( (String), (Output from the function), (If output was correct, and the correct answer if it wasn't) )\n")

# trying the function against the exercise and checking the answers
report = [
    (string, output,'Correct answer') if (output:= is_palindrome(string)) == answer
    else (string, output,'wrong answer', f'function returned "{output}", expected answer was "{answer}"')
    for string, answer in Exercise
]

# The report Above does the same as 
# for string, answer in Exercise:
#     output = is_palindrome(string)
#     if outpt == answer:
#         report.append((string, output,'Correct answer'))
#     else:
#         report.append((string, output,'wrong answer', f'function returned "{output}", expected answer was "{answer}"'))

for rep in report:
    print(rep)