from graphene_django.types import DjangoObjectType
from posts.models import Post, Person


# type for the Person model
class PersonType(DjangoObjectType):
    class Meta:
        model = Person


# type for the Post model
class PostType(DjangoObjectType):
    class Meta:
        model = Post
