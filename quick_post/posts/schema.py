import graphene
from graphene_django.types import ObjectType
from quick_post.types import PersonType, PostType
from .models import Post, Person


class Query(ObjectType):
    """
        Query
    """
    person = graphene.Field(PersonType, person_id=graphene.UUID())
    post = graphene.Field(PostType, post_id=graphene.UUID())
    persons = graphene.List(PersonType)
    posts = graphene.List(PostType)

    @staticmethod
    def resolve_person(self, info, **kwargs):
        person_id = kwargs.get('person_id')

        if person_id is not None:
            return Person.objects.get(pk=person_id)

        return None

    @staticmethod
    def resolve_post(self, info, **kwargs):
        post_id = kwargs.get('post_id')

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
    """
        Person Input
    """
    name = graphene.String()
    age = graphene.Int()


class CreatePerson(graphene.Mutation):
    """
        Create Person
    """
    class Arguments:
        person_input = PersonInput(required=True)

    ok = graphene.Boolean()
    person = graphene.Field(PersonType)

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
    """
        Update Person
    """
    class Arguments:
        person_id = graphene.UUID(required=True)
        person_input = PersonInput(required=True)

    ok = graphene.Boolean()
    person = graphene.Field(PersonType)

    @staticmethod
    def mutate(root, info, person_id, person_input=None):
        ok = False
        person_instance = Person.objects.get(pk=person_id)
        if person_instance:
            if person_input.name:
                person_instance.name = person_input.name
            if person_input.age:
                person_instance.age = person_input.age
            person_instance.save()
            ok = True
            return UpdatePerson(ok=ok, person=person_instance)
        return UpdatePerson(ok=ok, person=None)


class DeletePerson(graphene.Mutation):
    """
        Delete Person
    """
    class Arguments:
        person_id = graphene.UUID(required=True)

    ok = graphene.Boolean()

    @staticmethod
    def mutate(root, info, person_id):
        ok = True
        person_instance = Person.objects.filter(pk=person_id).first()
        if person_instance:
            person_instance.delete()
        return DeletePerson(ok=ok)


class PostInput(graphene.InputObjectType):
    """
        Post input
    """
    title = graphene.String()
    person_id = graphene.UUID()


class CreatePost(graphene.Mutation):
    """
        Create Post
    """
    class Arguments:
        post_input = PostInput(required=True)

    ok = graphene.Boolean()
    post = graphene.Field(PostType)

    @staticmethod
    def mutate(root, info, post_input=None):
        ok = False
        author = Person.objects.get(pk=post_input.person_id)
        if author is None:
            return CreatePost(ok=ok, post=None)
        post_instance = Post(
            title=post_input.title,
            author=author
          )
        post_instance.save()
        if post_instance:
            ok = True
            return CreatePost(ok=ok, post=post_instance)
        return CreatePost(ok=ok, post=None)


class UpdatePost(graphene.Mutation):
    """
        Update Post
    """
    class Arguments:
        post_id = graphene.UUID(required=True)
        post_input = PostInput(required=True)

    ok = graphene.Boolean()
    post = graphene.Field(PostType)

    @staticmethod
    def mutate(root, info, post_id, post_input=None):
        ok = False
        post_instance = Post.objects.get(pk=post_id)
        if post_instance:
            post_instance.title = post_input.title
            post_instance.save()
            ok = True
            return UpdatePost(ok=ok, post=post_instance)
        return UpdatePost(ok=ok, post=None)


class Mutation(graphene.ObjectType):
    create_person = CreatePerson.Field()
    update_person = UpdatePerson.Field()
    delete_person = DeletePerson.Field()
    create_post = CreatePost.Field()
    update_post = UpdatePost.Field()
