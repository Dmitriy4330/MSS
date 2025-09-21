import math


class Shape:

    def area(self):
        """Вычисляет площадь фигуры. Должен быть переопределен в дочернем классе."""
        raise NotImplementedError("Метод area() должен быть переопределен")

    def perimeter(self):
        """Вычисляет периметр фигуры. Должен быть переопределен в дочернем классе."""
        raise NotImplementedError("Метод perimeter() должен быть переопределен")

    def area_is_greater_than(self, other_shape):
       
        return self.area() > other_shape.area()

    def perimeter_is_greater_than(self, other_shape):
        
        return self.perimeter() > other_shape.perimeter()


class Square(Shape):
    def __init__(self, side):
        self.side = side

    def area(self):
        return self.side ** 2

    def perimeter(self):
        return 4 * self.side


class Rectangle(Shape):
    def __init__(self, length, width):
        self.length = length
        self.width = width

    def area(self):
        return self.length * self.width

    def perimeter(self):
        return 2 * (self.length + self.width)


class Triangle(Shape):
    def __init__(self, side_a, side_b, side_c):
        self.side_a = side_a
        self.side_b = side_b
        self.side_c = side_c

    def area(self):
        # Формула Герона
        s = self.perimeter() / 2
        return math.sqrt(s * (s - self.side_a) * (s - self.side_b) * (s - self.side_c))

    def perimeter(self):
        return self.side_a + self.side_b + self.side_c


class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return math.pi * (self.radius ** 2)

    def perimeter(self):
        return 2 * math.pi * self.radius
