# Finding the longest substring without repeating characters

def Longest_sub(s:str) -> tuple:
    dic = dict()
    largest = (0,'')

    # Initializing the window
    left, right = 0, 0

    while right < len(s):

        # If this character is in the dictionary and it's past appearance is inside the window
        if s[right] in dic and dic[s[right]] >= left:

                # Check largest and update if nescessary
                if right - left > largest[0]:
                    largest = (right - left, s[left:right])

                # Move left to the index after the reapeated char
                left = dic[s[right]] +1
        
        # add/update the char and it's position to the dictionary
        dic[s[right]] = right

        # Move right 
        right +=1
    
    # Check outside the while
    if right - left > largest[0]:
        largest = (right - left, s[left:right])

    return largest

exercise = [
    "abcabcbb",
    "bbbbb",
    "pwwkew",
    "dvdf",
    "anviajvnvn"
    ]

answer = [Longest_sub(string) for string in exercise]
print(answer)
