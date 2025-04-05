class Person:
    count=0

    def __init__(self, sex: str, age: int):
        self.sex=sex
        self.age=age
        Person.count+=1
        Person.person_func()

    def get_sex(self):
        return self.sex
    
    def get_age(self):
        return self.age
    
    @classmethod #decorator
    def person_func(cls):
        print(f'instance count :{Person.count}')

def main():
    person_a=Person("male", 30)
    print(f'person sex :{person_a.get_sex()}')
    print(f'person age :{person_a.get_age()}')

if __name__ == "__main__":
    main()