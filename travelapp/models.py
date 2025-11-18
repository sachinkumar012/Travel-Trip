from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.
class City(models.Model):
    city = models.CharField(max_length=200)
    bestlink = models.CharField(max_length=200)
    weekgetlinks = models.CharField(max_length=200)

    def __str__(self):
        return self.city


class Flights(models.Model):
    id = models.AutoField(primary_key=True)
    source = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)
    flight_num = models.CharField(max_length=10)
    city = models.ForeignKey(City,on_delete=models.CASCADE)
    eprice = models.IntegerField(null=True)
    dept_time = models.TimeField(auto_now=False,auto_now_add=False)
    dest_time = models.TimeField(auto_now=False,auto_now_add=False)
    company = models.CharField(max_length=15,default=" ")
    seats = models.IntegerField()


    def __str__(self):
        return self.flight_num

class Hotels(models.Model):
    id = models.AutoField(primary_key=True)
    city = models.ForeignKey(City,on_delete=models.CASCADE)
    hotel_name = models.CharField(max_length=200)
    hotel_address = models.CharField(max_length=500)
    hotel_price = models.IntegerField(null=True)
    hotel_rating = models.IntegerField(null=True)
    amenities = models.CharField(max_length=500)
    distfromap = models.IntegerField(null=True)
    rooms = models.IntegerField(default=0)
    image1 = models.ImageField(null=True,upload_to='img/')


    def __str__(self):
        return self.hotel_name

class Famous(models.Model):
    city = models.ForeignKey(City,on_delete=models.CASCADE)
    place_name = models.CharField(max_length=200)
    image = models.ImageField(null=True,upload_to='img/')
    desc = models.CharField(max_length=500)

    def __str__(self):
        return self.place_name

class BookFlight(models.Model):
    username_id = models.ForeignKey(User,on_delete=models.CASCADE)
    flight = models.CharField(max_length=10)
    date = models.CharField(max_length=20)
    seat = models.IntegerField(default=1)
    passenger_name = models.CharField(max_length=200, blank=True, null=True)
    passenger_email = models.EmailField(blank=True, null=True)
    passenger_phone = models.CharField(max_length=20, blank=True, null=True)
    passenger_address = models.TextField(blank=True, null=True)
    passenger_id_number = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.date

class BookHotel(models.Model):
    username_id = models.ForeignKey(User,on_delete=models.CASCADE)
    hotel_name = models.CharField(max_length=200)
    date = models.CharField(max_length=20)
    room = models.IntegerField(default=1)
    guest_name = models.CharField(max_length=200, blank=True, null=True)
    guest_email = models.EmailField(blank=True, null=True)
    guest_phone = models.CharField(max_length=20, blank=True, null=True)
    guest_address = models.TextField(blank=True, null=True)
    guest_id_number = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.date

class BookPackage(models.Model):
    username_id = models.ForeignKey(User,on_delete=models.CASCADE)
    seat = models.IntegerField(default=1)
    flight = models.CharField(max_length=10)
    hotel_name = models.CharField(max_length=200)
    room = models.IntegerField(default=1)
    date = models.CharField(max_length=20)
    passenger_name = models.CharField(max_length=200, blank=True, null=True)
    passenger_email = models.EmailField(blank=True, null=True)
    passenger_phone = models.CharField(max_length=20, blank=True, null=True)
    passenger_address = models.TextField(blank=True, null=True)
    passenger_id_number = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.date

class Passenger(models.Model):
    """Model to store individual passenger details for bookings with multiple seats/rooms"""
    booking_type = models.CharField(max_length=20, choices=[('flight', 'Flight'), ('hotel', 'Hotel'), ('package', 'Package')])
    booking_id = models.IntegerField()  # ID of the BookFlight, BookHotel, or BookPackage
    passenger_number = models.IntegerField(default=1)  # Which passenger (1st, 2nd, etc.)
    passenger_name = models.CharField(max_length=200)
    passenger_email = models.EmailField()
    passenger_phone = models.CharField(max_length=20)
    passenger_address = models.TextField()
    passenger_id_number = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        unique_together = ('booking_type', 'booking_id', 'passenger_number')

    def __str__(self):
        return f"{self.passenger_name} - {self.booking_type} #{self.booking_id}"
