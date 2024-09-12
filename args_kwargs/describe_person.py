def describe_person(name, age = None,**kwargs):
    print(f"Name = {name}")
    if age:
        print(f"Age = {age}")
    for key, value in kwargs.items():
        print(f'{key} = {value}')


describe_person('Jhonson', age = '36', height = '1.69 meters' , weight = '98 kg')
print()
describe_person('Jhonson', height = '1.69 meters' , weight = '98 kg')
print()
describe_person('Jhonson', height = '1.69 meters' , weight = '98 kg', age = '36')