class Car:
    def __init__(self,maker,model,year):
        self.maker = maker
        self.model = model
        self.year = year

    def start_engine(self):
        print("Engine Started")

Dummy_car = Car('test', 'prototype', 1111)
print(Dummy_car.maker, Dummy_car.model, Dummy_car.year)
Dummy_car.start_engine()