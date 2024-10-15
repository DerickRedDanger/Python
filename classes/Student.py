class Student:
    def __init__(self,name,grade):
        self.name = name
        self.grade = grade

    def display_info(self):
        print(self.name)
        print(self.grade)

Harry = Student('Harry','First Year')
Harry.display_info()