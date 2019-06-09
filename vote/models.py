from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class House(models.Model):
    """A simple table for each House"""

    name = models.CharField(max_length=30)
    motto = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

class Grade(models.Model):
    """A simple table for each Grade or Class"""

    name = models.CharField(max_length=10)
    level = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class Student(models.Model):
    """A table for students. Every student is linked with a user through a foreign key. The User table
    (Django built-in) must contain an entry for every Student. Only a username and Password are required to be in 
    the User table. Rest of the info is stored in this Student table."""

    user = models.ForeignKey(User, None)
    name = models.CharField(max_length=30)
    grade = models.ForeignKey(Grade, None)
    
    def __str__(self):
        return "{} ({})".format(self.name, self.grade)
    
class Candidate(models.Model):
    """A table to store the data of Students contesting for any poll. The student field is linked to a Student entry. This
    means that every Candidate must also be in the Student table"""

    student = models.ForeignKey(Student, None)
    slogan = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.student.name


class Poll(models.Model):
    """A table for storing the data for every poll. It doesn't store the casted votes but for each Poll, it stores data such as
    category of the poll (HR/CR), the House (a foreign key), the Grade (a foreign key), the Candidates contesting for the poll
    (a Many-Many Field), a boolean representing whether the poll is active or not, and a Many-Many field containing the voted Students."""

    category = models.CharField(max_length=2)
    house = models.ForeignKey(House, None)
    grade = models.ForeignKey(Grade, None)
    candidates = models.ManyToManyField(Candidate)
    active = models.BooleanField()
    voted = models.ManyToManyField(Student, blank=True)

    def __str__(self):
        return "{} ({} - {})".format(self.category, self.grade, self.house)

class Vote(models.Model):
    """A table which stores all the instances of casted votes. To ensure anonymity, the data of the voters are not stored. Only the record
    of the poll, the candidate voted for and the time voted is stored."""

    poll = models.ForeignKey(Poll, None)
    candidate = models.ForeignKey(Candidate, None)
    poll_date = models.DateField()
    poll_time = models.TimeField()

    def __str__(self):
        return self.candidate.student.name
