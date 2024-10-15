def Multiply(Number):
    result = Number
    def multiplying(y = None):
        nonlocal result
        if y is None:
            return result

        else:
            result *= y
            return multiplying

    return multiplying

print(Multiply(2)(3)(4)())