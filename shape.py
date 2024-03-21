import math
class Point:
  definition: str = "Abstract geometric entity representing a location in space."

  def __init__(self, x: float = 0, y: float = 0):
    self.__x = x
    self.__y = y

  def compute_distance(self, point) -> float:
    return round(
        ((self.__x - point.__x)**2 + (self.__y - point.__y)**2)**(0.5), 2)

  def magnitude(self):
    return round((self.__x**2 + self.__y**2)**(0.5), 2)

  def dot_product(self, point):
    return self.__x * point.__x + self.__y * point.__y

  def sum(self, i_point):
    return Point(self.__x + i_point.__x, self.__y + i_point.__y)

  def real_product(self, i_number: float):
    return Point(self.__x * i_number, self.__y * i_number)

  def get_x(self):
    return self.__x

  def get_y(self):
    return self.__y



class Line:
  definition: str = "It's a join between two points"

  def __init__(self, start_point: Point, end_point: Point):
    self.__start_point = start_point
    self.__end_point = end_point

  def length(self):
    return self.__start_point.compute_distance(self.__end_point)

  def get_starting_point(self):
    return self.__start_point

  def get_ending_point(self):
    return self.__end_point

  def to_vector(self):
    return self.__end_point.sum(self.__start_point.real_product(-1))

  def compute_angle(self, i_line):
    self_vector = self.to_vector()
    i_vector = i_line.to_vector()

    magnitude_product = (self_vector.magnitude() * i_vector.magnitude())
    cos = self_vector.dot_product(i_vector) / magnitude_product

    return math.degrees(math.acos(cos))

  def reverse(self):
    return Line(self.__end_point, self.__start_point)


class Shape:

  def __init__(self, vertices: list):
    self.__vertices = vertices

    self.__edges = []
    for i in range(len(vertices) - 1):
      self.__edges.append(Line(vertices[i], vertices[i + 1]))
    if vertices[0] != vertices[-1]:
      self.__edges.append(Line(vertices[-1], vertices[0]))
      self.__vertices.append(vertices[0])


    self.__is_regular = True
    #compare lenghts
    for i in range(len(self.__edges) - 1):
      if self.__edges[i].length() != self.__edges[i + 1].length():
        self.__is_regular = False
        break

    angles = self.compute_inner_angles()
    for i in range(len(angles) - 1):
      if angles[i] != angles[i + 1]:
        self.__is_regular = False
        break

  def compute_area(self):
    sum = 0
    for i in range(len(self.__vertices) - 1):
      sum += self.__vertices[i].get_x() * self.__vertices[i + 1].get_y()
    sum += self.__vertices[-1].get_x() * self.__vertices[0].get_y()

    other_sum = 0
    for i in range(len(self.__vertices) - 1):
      sum += self.__vertices[i + 1].get_x() * self.__vertices[i].get_y()
    other_sum += (self.__vertices[0].get_x() * self.__vertices[-1].get_y())
    return math.fabs(sum - other_sum) / 2

  def compute_perimeter(self):
    perimeter = 0.0
    for line in self.__edges:
      perimeter += line.length()
    return perimeter

  def compute_inner_angles(self):
    angles = []
    for i in range(0, len(self.__edges) - 1):
      angle =self.__edges[i].reverse().compute_angle(self.__edges[i + 1])
      angles.append(angle)
    angles.append(self.__edges[0].compute_angle(self.__edges[-1].reverse()))
    return angles

  def is_regular(self):
    return self.__is_regular

  def get_vertices(self):
    return self.__vertices

  def get_edges(self):
    return self.__edges

class Rectangle(Shape):

  def __init__(self, i_center: Point, i_width: float, i_height: float):
    vertices = [
        Point(i_center.get_x() - i_width / 2,
              i_center.get_y() - i_height / 2),
        Point(i_center.get_x() + i_width / 2,
              i_center.get_y() - i_height / 2),
        Point(i_center.get_x() + i_width / 2,
              i_center.get_y() + i_height / 2),
        Point(i_center.get_x() - i_width / 2,
              i_center.get_y() + i_height / 2)
    ]
    super().__init__(vertices)

  def compute_area(self):
    side1_length = self.get_edges()[0].length()
    side2_length = self.get_edges()[1].length()
    return side1_length * side2_length

  def compute_perimeter(self):
    perimeter = 0
    for line in self.get_edges():
      perimeter += line.length()
    return perimeter

  def compute_inner_angles(self):
    return [90, 90, 90, 90]

class Square(Rectangle):

  def __init__(self, i_center: Point, i_size: float):
    super().__init__(i_center, i_size, i_size)

  def compute_area(self):
    side_length = self.get_edges()[0].length()
    return side_length * side_length

  def compute_perimeter(self):
    side_length = self.get_edges()[0].length()
    return 4 * side_length

  def compute_inner_angles(self):
    return [90, 90, 90, 90]


class Triangle(Shape):
  def __init__(self, vertices: list):
      super().__init__(vertices)

  def compute_area(self):
      side1_lenght1=self.get_edges()[0].length()
      side2_lenght2=self.get_edges()[1].length()
      side3_lenght3=self.get_edges()[2].length()
      s=(side1_lenght1+side2_lenght2+side3_lenght3)/2
      area=(s*(s-side1_lenght1)*(s-side2_lenght2)*(s-side3_lenght3)**0.5)
      return area

  def compute_perimeter(self):
      perimeter = 0
      for line in self.get_edges():
          perimeter += line.length()
      return perimeter

class Equilateral(Triangle):
  def __init__(self, vertices: list):
    super().__init__(vertices)

  def compute_area(self):
    return super().compute_area()

  def compute_perimeter(self):
    return super().compute_perimeter()
   
class Isosceles(Triangle):
  def __init__(self, vertices: list):
    super().__init__(vertices)

  def compute_area(self):
    return super().compute_area()

  def compute_perimeter(self):
    return super().compute_perimeter()

class Scalene(Triangle):
  def __init__(self, vertices: list):
    super().__init__(vertices)

  def compute_area(self):
    return super().compute_area()

  def compute_perimeter(self):
    return super().compute_perimeter()


class TriRectangle(Triangle):
  def __init__(self, vertices: list):
    super().__init__(vertices)

  def compute_area(self):
    return super().compute_area()

  def compute_perimeter(self):
    return super().compute_perimeter()




if __name__ == "__main__":
  print(
      "Welcome to this code, this could calculate the area, the perimeter  and the \
inner angles of a shape"
  )
  print("You could choose one of this shapes: ")
  print(
      "rectangle, square, triangle, isosceles triangle, \
      equilateral triangle, scalene triangle, TriRectangle, other figure"
  
  )

  shape: str = input("Write the name of the shape that you want to use: ")
  fuction: bool = True   #Ayuda al final a imprimir 
                         #los valores si se escogio una figura

  
  match shape:
    case "rectangle":
      print("You chose a rectangle")
      center = Point(
        float(input("Write the x coordinate of the center: ")),
        float(input("Write the y coordinate of the center: "))
      )

      width = float(input("Write the width of the rectangle: "))
      height = float(input("Write the height of the rectangle: "))
      my_shape = Rectangle(i_center=center, i_width=width, i_height=height)

    case "square":
      print("You chose a square")
      center = Point(
        float(input("Write the x coordinate of the center: ")),
        float(input("Write the y coordinate of the center: "))
      )

      size = float(input("Write the size of the square: "))
      my_shape = Square(i_center=center, i_size=size)

    case "triangle":
      print("You chose a triangle") 
      vertices = []
      for i in range(3):
        x = float(input(f"Write the x coordinate of the vertex {i + 1}: "))
        y = float(input(f"Write the y coordinate of the vertex {i + 1}: "))
        vertices.append(Point(x=x, y=y))
      my_shape = Triangle(vertices=vertices)

    case "isosceles triangle":
      print("You chose a isosceles triangle")
      vertices = []
      for i in range(3):
        x = float(input(f"Write the x coordinate of the vertex {i + 1}: "))
        y = float(input(f"Write the y coordinate of the vertex {i + 1}: "))
        vertices.append(Point(x=x, y=y))
      my_shape = Isosceles(vertices=vertices)

    case "equilateral triangle":
      print("You chose a equilateral triangle")
      vertices = []
      for i in range(3):
        x = float(input(f"Write the x coordinate of the vertex {i + 1}: "))
        y = float(input(f"Write the y coordinate of the vertex {i + 1}: "))
        vertices.append(Point(x=x, y=y))
      my_shape = Equilateral(vertices=vertices)

    case "scalene triangle":
      print("You chose a scalene triangle")
      vertices = []
      for i in range(3):
        x = float(input(f"Write the x coordinate of the vertex {i + 1}: "))
        y = float(input(f"Write the y coordinate of the vertex {i + 1}: "))
        vertices.append(Point(x=x, y=y))
      my_shape = Scalene(vertices=vertices)

    case "TriRectangle":
      print("You chose a TriRectangle")
      vertices = []
      for i in range(3):
        x = float(input(f"Write the x coordinate of the vertex {i + 1}: "))
        y = float(input(f"Write the y coordinate of the vertex {i + 1}: "))
        vertices.append(Point(x=x, y=y))
      my_shape = TriRectangle(vertices=vertices)
    case "other figure":
      print("You chose an other figure")
      vertices = []
      other = True
      i = 1
      while other:
        x = float(input(f"Write the x coordinate of the vertex {i}: "))
        y = float(input(f"Write the y coordinate of the vertex {i}: "))
        vertices.append(Point(x=x, y=y))
        other_verification = input("Would you like to add another vertex? (y/n) ")
        i += 1
        if other_verification == "n":
          other = False
      my_shape = Shape(vertices=vertices)
    case _:
      print("Invalid shape")
      fuction: bool = False

  if fuction:
      print("The perimeter of the shape is", my_shape.compute_perimeter())
      print("The area of the shape is", my_shape.compute_area())
      print("The inner angles of the shape are",
            my_shape.compute_inner_angles())
      print("The shape is regular", my_shape.is_regular())  
  else:
      print("Reset the program ")
  