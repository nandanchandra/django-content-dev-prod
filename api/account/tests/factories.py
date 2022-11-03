import factory
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from faker import Factory as FakerFactory

from api.account.models import Profile

faker = FakerFactory.create()
User = get_user_model()


@factory.django.mute_signals(post_save)
class UserFactory(factory.django.DjangoModelFactory):
    first_name = factory.LazyAttribute(lambda x: faker.first_name())
    last_name = factory.LazyAttribute(lambda x: faker.last_name())
    username = factory.LazyAttribute(lambda x: faker.first_name().lower())
    email = factory.LazyAttribute(lambda o: "%s@gmail.com" % o.username)
    password = factory.LazyAttribute(lambda x: faker.password())
    is_active = True
    is_staff = False

    class Meta:
        model = User

    @classmethod
    def _create(cls, models_class, *args, **kwargs):
        manager = cls._get_manager(models_class)
        if "is_superuser" in kwargs:
            return manager.create_superuser(*args, **kwargs)
        else:
            return manager.create_user(*args, **kwargs)

@factory.django.mute_signals(post_save)
class ProfileFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    phone_number = factory.LazyAttribute(lambda x: faker.phone_number())
    about_me = factory.LazyAttribute(lambda x: faker.sentence(nb_words=5))
    gender = factory.LazyAttribute(lambda x: f"other")
    country = factory.LazyAttribute(lambda x: faker.country_code())
    city = factory.LazyAttribute(lambda x: faker.city())
    profile_photo = factory.LazyAttribute(lambda x: faker.file_extension(category="image"))
    twitter_handle = factory.LazyAttribute(lambda x: f"@example")
    facebook_handle = factory.LazyAttribute(lambda x: f"@example")
    instagram_handle = factory.LazyAttribute(lambda x: f"@example")

    class Meta:
        model = Profile

    @factory.post_generation
    def follows(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for follow in extracted:
                self.follows.add(follow)