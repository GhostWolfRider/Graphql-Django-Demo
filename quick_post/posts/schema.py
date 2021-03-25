import graphene
from graphene_django.types import ObjectType
from quick_post.types import PersonType, PostType
from .models import Post, Person


class Query(ObjectType):
    """
        Query
    """
    person = graphene.Field(PersonType, id=graphene.Int())
    post = graphene.Field(PostType, id=graphene.Int())
    persons = graphene.List(PersonType)
    posts = graphene.List(PostType)

    @staticmethod
    def resolve_person(info, **kwargs):
        person_id = kwargs.get('id')

        if person_id is not None:
            return Person.objects.get(pk=person_id)

        return None

    @staticmethod
    def resolve_post(self, info, **kwargs):
        post_id = kwargs.get('id')

        if post_id is not None:
            return Post.objects.get(pk=post_id)

        return None

    @staticmethod
    def resolve_persons(self, info, **kwargs):
        return Person.objects.all()

    @staticmethod
    def resolve_posts(self, info, **kwargs):
        return Post.objects.all()


"""
 Mutation
"""


class PersonInput(graphene.InputObjectType):
    name = graphene.String()
    age = graphene.Int()


class CreatePerson(graphene.Mutation):
    ok = graphene.Boolean()
    person = graphene.Field(PersonType)

    class Arguments:
        person_input = PersonInput(required=True)

    @staticmethod
    def mutate(root, info, person_input=None):
        ok = False
        person_instance = Person(name=person_input.name, age=person_input.age)
        person_instance.save()
        if person_instance:
            ok = True
            return CreatePerson(ok=ok, person=person_instance)
        return CreatePerson(ok=ok, person=person_instance)


class UpdatePerson(graphene.Mutation):
    ok = graphene.Boolean()
    person = graphene.Field(PersonType)

    class Arguments:
        person_id = graphene.UUID(required=True)
        person_input = PersonInput(required=True)

    @staticmethod
    def mutate(root, info, person_id, person_input=None):
        ok = False
        person_instance = Person.objects.get(pk=person_id)
        if person_instance:
            person_instance.name = person_input.name
            person_instance.save()
            ok = True
            return UpdatePerson(ok=ok, person=person_instance)
        return UpdatePerson(ok=ok, person=None)

#
# class CreatePost(graphene.Mutation):
#     title = graphene.String()
#     authors = graphene.List(PersonType)
#     class Arguments:
#         input = MovieInput(required=True)
#
#     ok = graphene.Boolean()
#     movie = graphene.Field(MovieType)
#
#     @staticmethod
#     def mutate(root, info, input=None):
#         ok = True
#         actors = []
#         for actor_input in input.actors:
#           actor = Actor.objects.get(pk=actor_input.id)
#           if actor is None:
#             return CreateMovie(ok=False, movie=None)
#           actors.append(actor)
#         movie_instance = Movie(
#           title=input.title,
#           year=input.year
#           )
#         movie_instance.save()
#         movie_instance.actors.set(actors)
#         return CreateMovie(ok=ok, movie=movie_instance)
#
#
# class UpdateMovie(graphene.Mutation):
#     class Arguments:
#         id = graphene.Int(required=True)
#         input = MovieInput(required=True)
#
#     ok = graphene.Boolean()
#     movie = graphene.Field(MovieType)
#
#     @staticmethod
#     def mutate(root, info, id, input=None):
#         ok = False
#         movie_instance = Movie.objects.get(pk=id)
#         if movie_instance:
#             ok = True
#             actors = []
#             for actor_input in input.actors:
#               actor = Actor.objects.get(pk=actor_input.id)
#               if actor is None:
#                 return UpdateMovie(ok=False, movie=None)
#               actors.append(actor)
#             movie_instance.title=input.title
#             movie_instance.year=input.year
#             movie_instance.save()
#             movie_instance.actors.set(actors)
#             return UpdateMovie(ok=ok, movie=movie_instance)
#         return UpdateMovie(ok=ok, movie=None)


class Mutation(graphene.ObjectType):
    create_person = CreatePerson.Field()
    update_person = UpdatePerson.Field()
    # create_post = CreatePost.Field()
    # update_post = UpdatePost.Field()
