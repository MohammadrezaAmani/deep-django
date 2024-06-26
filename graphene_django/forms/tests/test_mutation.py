from django import forms
from django.core.exceptions import ValidationError
from graphene import Field, ObjectType, Schema, String
from pytest import raises

from graphene_django import DjangoObjectType
from graphene_django.tests.forms import PetForm
from graphene_django.tests.models import Pet
from graphene_django.tests.mutations import PetMutation

from ..mutation import DjangoFormMutation, DjangoModelFormMutation


class MyForm(forms.Form):
    text = forms.CharField()

    def clean_text(self):
        text = self.cleaned_data["text"]
        if text == "INVALID_INPUT":
            raise ValidationError("Invalid input")
        return text

    def save(self):
        pass


def test_needs_form_class():
    with raises(Exception) as exc:

        class MyMutation(DjangoFormMutation):
            pass

    assert exc.value.args[0] == "form_class is required for DjangoFormMutation"


def test_has_output_fields():
    class MyMutation(DjangoFormMutation):
        class Meta:
            form_class = MyForm

    assert "errors" in MyMutation._meta.fields


def test_has_input_fields():
    class MyMutation(DjangoFormMutation):
        class Meta:
            form_class = MyForm

    assert "text" in MyMutation.Input._meta.fields


def test_mutation_error_camelcased(graphene_settings):
    class ExtraPetForm(PetForm):
        test_field = forms.CharField(required=True)

    class PetType(DjangoObjectType):
        class Meta:
            model = Pet
            fields = "__all__"

    class PetMutation(DjangoModelFormMutation):
        pet = Field(PetType)

        class Meta:
            form_class = ExtraPetForm

    result = PetMutation.mutate_and_get_payload(None, None)
    assert {f.field for f in result.errors} == {"name", "age", "testField"}
    graphene_settings.CAMELCASE_ERRORS = False
    result = PetMutation.mutate_and_get_payload(None, None)
    assert {f.field for f in result.errors} == {"name", "age", "test_field"}


class MockQuery(ObjectType):
    a = String()


def test_form_invalid_form():
    class MyMutation(DjangoFormMutation):
        class Meta:
            form_class = MyForm

    class Mutation(ObjectType):
        my_mutation = MyMutation.Field()

    schema = Schema(query=MockQuery, mutation=Mutation)

    result = schema.execute(
        """ mutation MyMutation {
            myMutation(input: { text: "INVALID_INPUT" }) {
                errors {
                    field
                    messages
                }
                text
            }
        }
        """
    )

    assert result.errors is None
    assert result.data["myMutation"]["errors"] == [
        {"field": "text", "messages": ["Invalid input"]}
    ]


def test_form_valid_input():
    class MyMutation(DjangoFormMutation):
        class Meta:
            form_class = MyForm

    class Mutation(ObjectType):
        my_mutation = MyMutation.Field()

    schema = Schema(query=MockQuery, mutation=Mutation)

    result = schema.execute(
        """ mutation MyMutation {
            myMutation(input: { text: "VALID_INPUT" }) {
                errors {
                    field
                    messages
                }
                text
            }
        }
        """
    )

    assert result.errors is None
    assert result.data["myMutation"]["errors"] == []
    assert result.data["myMutation"]["text"] == "VALID_INPUT"


def test_default_meta_fields():
    assert PetMutation._meta.model is Pet
    assert PetMutation._meta.return_field_name == "pet"
    assert "pet" in PetMutation._meta.fields


def test_default_input_meta_fields():
    assert PetMutation._meta.model is Pet
    assert PetMutation._meta.return_field_name == "pet"
    assert "name" in PetMutation.Input._meta.fields
    assert "client_mutation_id" in PetMutation.Input._meta.fields
    assert "id" in PetMutation.Input._meta.fields


def test_exclude_fields_input_meta_fields():
    class PetType(DjangoObjectType):
        class Meta:
            model = Pet
            fields = "__all__"

    class PetMutation(DjangoModelFormMutation):
        pet = Field(PetType)

        class Meta:
            form_class = PetForm
            exclude_fields = ["id"]

    assert PetMutation._meta.model is Pet
    assert PetMutation._meta.return_field_name == "pet"
    assert "name" in PetMutation.Input._meta.fields
    assert "age" in PetMutation.Input._meta.fields
    assert "client_mutation_id" in PetMutation.Input._meta.fields
    assert "id" not in PetMutation.Input._meta.fields


def test_custom_return_field_name():
    class PetType(DjangoObjectType):
        class Meta:
            model = Pet
            fields = "__all__"

    class PetMutation(DjangoModelFormMutation):
        pet = Field(PetType)

        class Meta:
            form_class = PetForm
            model = Pet
            return_field_name = "animal"

    assert PetMutation._meta.model is Pet
    assert PetMutation._meta.return_field_name == "animal"
    assert "animal" in PetMutation._meta.fields


def test_model_form_mutation_mutate_existing():
    class Mutation(ObjectType):
        pet_mutation = PetMutation.Field()

    schema = Schema(query=MockQuery, mutation=Mutation)

    pet = Pet.objects.create(name="Axel", age=10)

    result = schema.execute(
        """ mutation PetMutation($pk: ID!) {
            petMutation(input: { id: $pk, name: "Mia", age: 10 }) {
                pet {
                    name
                    age
                }
            }
        }
        """,
        variable_values={"pk": pet.pk},
    )

    assert result.errors is None
    assert result.data["petMutation"]["pet"] == {"name": "Mia", "age": 10}

    assert Pet.objects.count() == 1
    pet.refresh_from_db()
    assert pet.name == "Mia"


def test_model_form_mutation_creates_new():
    class Mutation(ObjectType):
        pet_mutation = PetMutation.Field()

    schema = Schema(query=MockQuery, mutation=Mutation)

    result = schema.execute(
        """ mutation PetMutation {
            petMutation(input: { name: "Mia", age: 10 }) {
                pet {
                    name
                    age
                }
                errors {
                    field
                    messages
                }
            }
        }
        """
    )
    assert result.errors is None
    assert result.data["petMutation"]["pet"] == {"name": "Mia", "age": 10}

    assert Pet.objects.count() == 1
    pet = Pet.objects.get()
    assert pet.name == "Mia"
    assert pet.age == 10


def test_model_form_mutation_invalid_input():
    class Mutation(ObjectType):
        pet_mutation = PetMutation.Field()

    schema = Schema(query=MockQuery, mutation=Mutation)

    result = schema.execute(
        """ mutation PetMutation {
            petMutation(input: { name: "Mia", age: 99 }) {
                pet {
                    name
                    age
                }
                errors {
                    field
                    messages
                }
            }
        }
        """
    )
    assert result.errors is None
    assert result.data["petMutation"]["pet"] is None
    assert result.data["petMutation"]["errors"] == [
        {"field": "age", "messages": ["Too old"]}
    ]

    assert Pet.objects.count() == 0


def test_model_form_mutation_mutate_invalid_form():
    result = PetMutation.mutate_and_get_payload(None, None)

    # A pet was not created
    assert Pet.objects.count() == 0

    fields_w_error = [e.field for e in result.errors]
    assert len(result.errors) == 2
    assert result.errors[0].messages == ["This field is required."]
    assert result.errors[1].messages == ["This field is required."]
    assert "age" in fields_w_error
    assert "name" in fields_w_error


def test_model_form_mutation_multiple_creation_valid():
    class Mutation(ObjectType):
        pet_mutation = PetMutation.Field()

    schema = Schema(query=MockQuery, mutation=Mutation)

    result = schema.execute(
        """
        mutation PetMutations {
            petMutation1: petMutation(input: { name: "Mia", age: 10 }) {
                pet {
                    name
                    age
                }
                errors {
                    field
                    messages
                }
            }
            petMutation2: petMutation(input: { name: "Enzo", age: 0 }) {
                pet {
                    name
                    age
                }
                errors {
                    field
                    messages
                }
            }
        }
        """
    )
    assert result.errors is None
    assert result.data["petMutation1"]["pet"] == {"name": "Mia", "age": 10}
    assert result.data["petMutation2"]["pet"] == {"name": "Enzo", "age": 0}

    assert Pet.objects.count() == 2

    pet1 = Pet.objects.first()
    assert pet1.name == "Mia"
    assert pet1.age == 10

    pet2 = Pet.objects.last()
    assert pet2.name == "Enzo"
    assert pet2.age == 0


def test_model_form_mutation_multiple_creation_invalid():
    class Mutation(ObjectType):
        pet_mutation = PetMutation.Field()

    schema = Schema(query=MockQuery, mutation=Mutation)

    result = schema.execute(
        """
        mutation PetMutations {
            petMutation1: petMutation(input: { name: "Mia", age: 99 }) {
                pet {
                    name
                    age
                }
                errors {
                    field
                    messages
                }
            }
            petMutation2: petMutation(input: { name: "Enzo", age: 0 }) {
                pet {
                    name
                    age
                }
                errors {
                    field
                    messages
                }
            }
        }
        """
    )
    assert result.errors is None

    assert result.data["petMutation1"]["pet"] is None
    assert result.data["petMutation1"]["errors"] == [
        {"field": "age", "messages": ["Too old"]}
    ]

    assert result.data["petMutation2"]["pet"] == {"name": "Enzo", "age": 0}

    assert Pet.objects.count() == 1

    pet = Pet.objects.get()
    assert pet.name == "Enzo"
    assert pet.age == 0
