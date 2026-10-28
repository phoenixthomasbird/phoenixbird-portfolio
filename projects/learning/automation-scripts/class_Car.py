
class Car:
    #class attribute shared by all instances
    max_speed = 120

#constructor method
    def __init__(self, make, model, color, speed=0):
     self.make = make
     self.model = model
     self.color = color
     self.speed = speed #initial speed set to 0

#method for acccelrating the car
    def accelerate(self, acceleration):
        if self.speed + acceleration <+ Car.max_speed:
            self.speed += acceleration
        else:
            self.speed = Car.max_speed

#method to get the current speed of the car
    def get_speed(self):
        return self.speed

#create objects (instances) of the Car class
car_1 = Car("Toyota", "Camry", "Blue")
car_2 = Car("Honda", "Civic", "Red")

car_1.accelerate(30)
car_2.accelerate(20)


print(f"{car_1.make} {car_1.model} is currently at {car_1.get_speed()} km/h.")
print(f"{car_2.make} {car_2.model} is currently at {car_2.get_speed()} km/h.")