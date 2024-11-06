from django.db import models


class Employee(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField(unique=True)
    address=models.TextField()
    department=models.CharField(max_length=100)
    salary=models.PositiveIntegerField()
    date_of_join=models.DateField()
    gender_choice=(
                    ("male","male"),
                    ("female","female"),
                    ("others","others")
                )
    gender=models.CharField(max_length=100,choices=gender_choice,default="male")
    picture=models.ImageField(upload_to="employee_images",null=True,blank=True)

    def __str__(self):
        return self.name
