# Shapes

### For computing the inner angles, perimeter and area, we decided to use the dot product, this simplify many things, and help us a lot. You could decide if you wanna know the area, perimeter and the inner angles of the square or rectangle, the triangle and many kind of triangles. Also this code could calculate (approximately), the inner angles of a shape that have more than 4 vertex

```python
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
  
```


# Restaurant
### I privatize the attributes of any class, less in Payment_method, and i agragate last one. You can decide the payment method and enter the ammount of money or your credit card depending the method that you choose
```python
class MenuItem:
    def __init__(self, name: str, price: int):
        self.__name = name
        self.__price = price  


    def get_name(self):
        return self.__name
    
    def set_name(self, new_name):
        if new_name:
            self.__name = new_name


    def get_price(self):
        return self.__price
    
    def set_price(self, new_price):
        if new_price:
            self.__price = new_price


class Beverage(MenuItem):
    def __init__(self, name: str, price: int, alcohol: bool):
        super().__init__(name, price)
        self.__alcohol = alcohol
    
    def get_alcohol(self):
        return self.__alcohol
    
    def set_alcohol(self, new_alcohol):
        if new_alcohol:
            self.__alcohol = new_alcohol


class Appetizer(MenuItem):
    def __init__(self, name: str, price: int,origin: str):
        super().__init__(name, price)
        self.__origin = origin
        
    def get_origin(self):
        return self.__origin
    
    def set_origin(self, new_origin):
        if new_origin:
            self.__origin = new_origin

    

class MainCourse(MenuItem):
    def __init__(self, name: str, price: int, vegan: bool):
        super().__init__(name, price)
        self.__vegan = vegan
    
    def get_vegan(self):
        return self.__vegan
    
    def set_vegan(self, new_vegan):
        if new_vegan:
            self.__vegan = new_vegan



class Dessert(MenuItem):
    def __init__(self, name: str, price: int, kind: str):
        super().__init__(name, price)
        self.__kind = kind
        
    def get_kind(self):
        return self.__kind
    
    def set_kind(self, new_kind):
        if new_kind:
            self.__kind = new_kind



class Order:
    def __init__(self, Menu_items:list):
        self.Menu_items = Menu_items


    def add_items(self, new_food:list):
        self.new_food = new_food
        for i in self.new_food:
            self.Menu_items.append(i)


    def calculate_total_bill(self):
        total_money = []
        for i in self.Menu_items:
            total_money.append(i.get_price())
        return sum(total_money)


    def calculate_discounts(self):
        total_discount = self.calculate_total_bill()
        total_price = self.calculate_total_bill()
        
        has_appetizer = any(isinstance(item, Appetizer) for item in self.Menu_items)

        has_dessert = any(isinstance(item, Dessert) for item in self.Menu_items)

        has_beverage = any(isinstance(item, Beverage) for item in self.Menu_items)

        if has_appetizer:
            total_discount = (total_discount - total_price*0.025)
        
        if has_dessert:
            total_discount = (total_discount - total_price*0.05)

        if has_beverage:
            total_discount = (total_discount - total_price*0.035)
        
        return(int(total_discount))

class Payment_method:
  def __init__(self):
    pass

  def pagar(self, money):
    raise NotImplementedError()

class Credit_card(Payment_method):
  def __init__(self, number, cvv):
    super().__init__()
    self.number = number
    self.cvv = cvv

  def pagar(self, money):

    print(f"Paying {money} with credit card {self.number[-4:]}")

class Cash(Payment_method):
  def __init__(self, money_payed):
    super().__init__()
    self.money_payed = money_payed

  def pagar(self, money):

    if self.money_payed >= money:
      print(f"Sucessfully payment. Exchange: {self.money_payed - money}")
    else:
      print(f"Sorry, you will have to wash the dishes. Missing {money - self.money_payed} for completing the payment .")


if __name__ == "__main__":
    

    lemonade = Beverage(name="Lemonade", price=2000, alcohol=False)
    beer = Beverage(name="Beer", price=3000, alcohol=False)
    water = Beverage(name="Water", price=1000, alcohol=False)


    empanada = Appetizer(name="Lemonade", price=1500, origin="Colombia")
    arepa = Appetizer(name="Lemonade", price=2200, origin="Venezuela")
    


    chinese_rise = MainCourse(name="Chinese rise", price=20000, vegan=False)
    hamburger = MainCourse(name="Hamburger", price=25000, vegan=False)
    vegan_hamburger = MainCourse(name="Vegan_hambuerger", price=30000, vegan=True)



    ice_cream = Dessert(name="orange ice cream", price=3000, kind="Ice Cream")
    candys = Dessert(name="sweet mind", price=500, kind="Candy")
    cake = Dessert(name="Banana Cake", price=4500, kind="Cake")

    print("Menu")
    print("lemonade, water, beer, empanada, arepa, chinese rise, hamburger, vegan hamburger, Banana Cake, sweet mind, orange ice cream")

    print("So, you want a cake, a empanada, a water and a hamburger")

    First_order: Order = Order([cake, empanada, water, hamburger])

    start = True
    new_food = []
    while start or mores_food:
        start = False
        more_food: str = input("Would you like more food, yes or no?\n" )
        if more_food == "yes":
            mores_food = True
            food = input("Which one?: ")
            match food:
                case "lemonade": 
                    wished_food = lemonade
                case "beer":
                    wished_food = beer
                case "water":
                    wished_food= water
                case "arepa": 
                    wished_food = arepa
                case "empanada":
                    wished_food = empanada
                case "chinise rise":
                    wished_food= chinese_rise
                case "hamburger": 
                    wished_food = hamburger
                case "vegan hamburger":
                    wished_food = vegan_hamburger
                case "orange ice cream":
                    wished_food= ice_cream
                case "Banana Cake":
                    wished_food = cake
                case "sweet mind":
                    wished_food= candys
            new_food.append(wished_food)
        else:
            mores_food = False
        

    First_order.add_items(new_food=new_food)
        
    print("Your bill without discount is: ",First_order.calculate_total_bill())
    print("your bill with discounts is: ", First_order.calculate_discounts())


        
    print("This will be the two methods on payment: ")
    payment = input("Enter credit card or efective:\n")
    match payment:
        case "credit card":
            fuc: bool = True
            credit_card: str = input("Enter your credit card number:\n")
            cvv: str = input("Enter the password:\n")
            if len(credit_card) != 13:
                print("This is not the number of a credit card")
                fuc: bool = False
            if len(cvv) != 3:
                print("This is not the cvv")
                fuc: bool = False
            if fuc:
                cvv: int = int(cvv)
                pay1 = Credit_card(number=credit_card, cvv=cvv)
                pay1.pagar(First_order.calculate_discounts())
                
        case "efective":
            money_have: int = int(input("How much money do you have?:\n"))
            pay1 = Cash(money_payed=money_have)
            pay1.pagar(First_order.calculate_discounts())

        case _:
            print("Invalid payment method")
    
```
