from class_person import Person

class Student(Person):
    def __init__(self, sex, age, no: str):
        super().__init__(sex, age)
        self.no=no

    def get_no(self):
        return self.no
    
    def get_age(self):        
        return super().get_age() - 1

    def __str__(self): #객체를 출력했을때 지정된 형태로 출력
        return f'override Student instance'    



def main():
    person_a=Person("male", 30)
    print(f'person sex :{person_a.get_sex()}')
    print(f'person age :{person_a.get_age()}')

    student_b=Student("female", 16, "0001")
    print(f'student sex :{student_b.get_sex()}')
    print(f'student age :{student_b.get_age()}')
    print(student_b)

    men=[person_a, student_b]
    for human in men:
        print(f'human age :{human.get_age()}')
        if isinstance(human, Student):
            print(f'human no :{human.get_no()}')

if __name__ == "__main__":
    main()