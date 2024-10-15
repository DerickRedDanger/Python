def accumulate(element):
    lis = [element]
    def accumulating(elements = None):
        nonlocal lis
        if elements is None:
            return lis
        
        else:
            lis.append(elements)
            return accumulating
    return accumulating

print(accumulate(1)(2)(3)())
