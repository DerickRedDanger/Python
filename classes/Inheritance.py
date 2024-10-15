class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        pass

class Dog(Animal):
    def speak(self):
        return "Woof!"

class Cat(Animal):
    def speak(self):
        return "Meow!"

dog = Dog("Buddy")
cat = Cat("Whiskers")

print(dog.name)  # Output: Buddy
print(dog.speak())  # Output: Woof!
print(cat.name)  # Output: Whiskers
print(cat.speak())  # Output: Meow!

# Check if cat is an instance of Cat
print(isinstance(cat, Cat))  # Output: True

# Check if cat is an instance of Animal
print(isinstance(cat, Animal))  # Output: True

# Check if cat is not an instance of Dog
print(isinstance(cat, Dog))  # Output: False

# Check if cat is exactly an instance of Cat
print(type(cat) is Cat)  # Output: True

# Check if cat is exactly an instance of Animal
print(type(cat) is Animal)  # Output: False