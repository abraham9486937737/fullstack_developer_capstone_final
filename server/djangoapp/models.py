from django.db import models
from django.utils.timezone import now
from django.core.validators import MaxValueValidator, MinValueValidator


# Car Make model 
class CarMake(models.Model): 
    name = models.CharField(max_length=100) 
    description = models.TextField() 
    
    # Other fields can be added if needed (e.g., country, founded_year) 
    
    def __str__(self): 
        return self.name # Return the name as the string representation 

# Car Model model 
class CarModel(models.Model): 
    # Many-to-One relationship to CarMake 
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE) 
    
    name = models.CharField(max_length=100) 
    
    CAR_TYPES = [ 
        ('SEDAN', 'Sedan'), 
        ('SUV', 'SUV'), 
        ('WAGON', 'Wagon'), 
        ('COUPE', 'Coupe'), 
    ] 
    
    type = models.CharField(max_length=10, choices=CAR_TYPES, default='SUV') 
    
    dealer_id = models.IntegerField() # Refers to dealer in Cloudant/MongoDB 
    
    year = models.IntegerField( 
        default=2023, 
        validators=[ 
            MaxValueValidator(2023), 
            MinValueValidator(2015) 
        ] 
    ) 
    
    def __str__(self): 
        return f"{self.car_make.name} {self.name} ({self.year})"
