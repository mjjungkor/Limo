class Person:
    def __init__(self, sex: str, age: int):
        self.sex=sex
        self.age=age

    def get_sex(self):
        return self.sex
    
    def get_age(self):
        return self.age

def main():
    person_a=Person("male", 30)
    print(f'person sex :{person_a.get_sex()}')
    print(f'person age :{person_a.get_age()}')

if __name__ == "__main__":
    main()