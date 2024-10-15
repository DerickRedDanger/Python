def Concatenation(String):
    lis = [String]
    def concatenating(Strings = None):
        nonlocal lis
        if Strings is None:
            return ''.join(lis)
        
        else:
            lis.append(Strings)
            return concatenating
    return concatenating

print(Concatenation("Hello")(" ")("World")("!")())
