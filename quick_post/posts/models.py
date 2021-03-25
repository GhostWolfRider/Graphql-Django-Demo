import uuid
from django.db import models


class Person(models.Model):
    """
    Person model is for storing all the author details.
    """

    # UUID of person
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # title of the post
    name = models.CharField(max_length=100)

    # person age
    age = models.CharField(max_length=10)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Post(models.Model):
    """
    Person model is for storing all the author details.
    """

    # UUID of post
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # title of the post
    title = models.CharField(max_length=100)

    # post created by person
    author = models.ForeignKey(Person, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('title',)


