class Person:
    """Базовый класс Человек."""

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def print_info(self):
        print(f"ФИО: {self.name}, Возраст: {self.age}")


class Student(Person):
    def __init__(self, name, age, group_number, average_grade):
        super().__init__(name, age)
        self.group_number = group_number
        self.average_grade = average_grade

    def calculate_scholarship(self):
 
        if self.average_grade == 5:
            return 6000
        elif self.average_grade < 5 and self.average_grade >= 4:  # Предположим, что "меньше 5" - это все еще хорошая оценка
            return 4000
        else:
            return 0

    def print_scholarship(self):

        scholarship = self.calculate_scholarship()
        print(f"Стипендия студента {self.name}: {scholarship}р")

    def scholarship_is_greater_than(self, other_student):
      
        return self.calculate_scholarship() > other_student.calculate_scholarship()


class Aspirant(Student):
    def __init__(self, name, age, group_number, average_grade, research_topic):
        super().__init__(name, age, group_number, average_grade)
        self.research_topic = research_topic

    def calculate_scholarship(self):

        if self.average_grade == 5:
            return 8000
        elif self.average_grade < 5 and self.average_grade >= 4:
            return 6000
        else:
            return 0

    def print_info(self):

        super().print_info()
        print(f"Тема научной работы: {self.research_topic}")

    def print_scholarship(self):

        scholarship = self.calculate_scholarship()
        print(f"Стипендия аспиранта {self.name}: {scholarship}р")


