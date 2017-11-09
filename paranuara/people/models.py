from django.db import models

from paranuara.companies.models import Company


class Person(models.Model):
    """"A person living on Paranuara"""

    MALE = 'M'
    FEMALE = 'F'
    OTHER = 'O'

    GENDER_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHER, 'Other'),
    )

    id = models.IntegerField(primary_key=True)
    hash_id = models.CharField(max_length=25, unique=True)
    guid = models.UUIDField(unique=True)
    has_died = models.BooleanField(default=False)
    balance = models.IntegerField()
    picture_url = models.CharField(max_length=255)
    age = models.IntegerField(null=False)
    eye_color = models.CharField(max_length=50)
    name = models.CharField(max_length=255)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES,
                              null=False)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=1000)
    about = models.TextField()
    greeting = models.TextField()
    registered_at = models.DateTimeField()

    company = models.ForeignKey(Company, null=True, blank=True)


class FriendRelationship(models.Model):
    """Defines a friendship between two Persons"""

    class Meta:
        unique_together = ('person_1', 'person_2',)

    person_1 = models.ForeignKey(Person, null=False, related_name='person1')
    person_2 = models.ForeignKey(Person, null=False, related_name='person2')


class Tag(models.Model):
    """Tag related to a single Person"""

    person = models.ForeignKey(Person, null=False)
    tag_name = models.CharField(max_length=100, null=False)


class Food(models.Model):
    """Fruit or Vegetable"""

    FRUIT = 'F'
    VEGETABLE = 'V'

    FOOD_TYPE_CHOICES = (
        (FRUIT, 'Fruit'),
        (VEGETABLE, 'Vegetable'),
    )

    name = models.CharField(max_length=50, null=False, unique=True)
    type = models.CharField(null=True, blank=True, max_length=1,
                            choices=FOOD_TYPE_CHOICES)


class FavouriteFood(models.Model):

    class Meta:
        unique_together = ('person', 'food',)

    person = models.ForeignKey(Person, null=False)
    food = models.ForeignKey(Food, null=False)
