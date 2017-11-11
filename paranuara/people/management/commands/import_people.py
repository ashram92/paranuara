import json
from collections import namedtuple
from datetime import datetime

from django.core.management.base import BaseCommand
from django.db import IntegrityError

from paranuara.companies.models import Company
from paranuara.people import constants
from paranuara.people.models import (
    Person, FriendRelationship, Tag, Food, FavouriteFood
)


FriendshipSet = namedtuple('FriendshipSet', ['person_1_id', 'person_2_id'])


def normalise_balance(balance):
    normalised = balance.replace('$', '')  # Strip `$`
    normalised = normalised.replace('.', '')  # Strip `.`
    normalised = normalised.replace(',', '')  # Strip `,`
    return normalised


class Command(BaseCommand):
    help = 'Import all people and relationships ' \
           'from a specified raw json file.'

    def __init__(self):
        super(Command, self).__init__()
        self.friendship_sets = []
        """:type: List[FriendshipSet]"""

        self.fruit_map = {}  # name -> id

        self.company_ids = [c.id for c in Company.objects.all()]

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str)

    def _import_all_friendships(self):
        for friendship_set in self.friendship_sets:
            try:
                FriendRelationship(person_1_id=friendship_set.person_1_id,
                                   person_2_id=friendship_set.person_2_id
                                   ).save(force_insert=True)
            except IntegrityError:
                pass

    def _import_food(self, name):

        # Fruit ID is already cached
        if name in self.fruit_map:
            return self.fruit_map[name]

        food = Food.objects.filter(name=name).first()
        if not food:
            if name in constants.FRUITS:
                food_type = Food.FRUIT
            elif name in constants.VEGETABLES:
                food_type = Food.VEGETABLE
            else:
                food_type = None
            food = Food(name=name, type=food_type)
            food.save()

        self.fruit_map[name] = food.id

        return food.id

    def _build_person_model(self, person_data):
        person = Person(
            id=person_data["index"],
            hash_id=person_data["_id"],
            guid=person_data["guid"],
            has_died=person_data["has_died"],
            balance=normalise_balance(person_data["balance"]),
            picture_url=person_data["picture"],
            age=person_data["age"],
            eye_color=person_data["eyeColor"],
            name=person_data["name"],
            email=person_data["email"],
            phone=person_data["phone"],
            address=person_data["address"],
            about=person_data["about"],
            greeting=person_data["greeting"]
        )

        if person_data['gender'] == 'female':
            person.gender = Person.FEMALE
        elif person_data['gender'] == 'male':
            person.gender = Person.MALE
        else:
            person.gender = Person.OTHER

        # Remove the last ':'
        date_str = person_data['registered'][:-3] + person_data['registered'][
                                                    -2:]

        person.registered_at = datetime.strptime(
            date_str,
            '%Y-%m-%dT%H:%M:%S %z'
        )

        if person_data['company_id'] in self.company_ids:
            person.company_id = person_data['company_id']
        else:
            person.company_id = None

        return person

    def _import_person_foods(self, person, foods):
        # Import all Food & Favourite Food
        for food_name in foods:
            food_id = self._import_food(food_name)

            try:
                FavouriteFood(person_id=person.id,
                              food_id=food_id).save(force_insert=True)
            except IntegrityError:
                pass

    def _import_person_tags(self, person, tags):
        # Import all Tags
        for tag in tags:
            try:
                Tag(person=person,
                    tag_name=tag).save(force_insert=True)
            except IntegrityError:
                pass

    def _update_friendship_sets(self, person, person_friends):
        for friend in person_friends:
            self.friendship_sets.append(
                FriendshipSet(person_1_id=person.id,
                              person_2_id=friend['index'])
            )

    def _import_person(self, person_data):
        person = self._build_person_model(person_data)

        try:
            person.save(force_insert=True)
        except IntegrityError:
            self.stderr('{} already exists. Skipping.'.format(person))

        self._import_person_foods(person, person_data['favouriteFood'])
        self._import_person_tags(person, person_data['tags'])
        self._update_friendship_sets(person, person_data['friends'])

    def handle(self, *args, **options):
        with open(options['file_path']) as f:
            data = json.load(f)
            for person_data in data:
                self._import_person(person_data)
            self._import_all_friendships()

        self.stdout.write(self.style.SUCCESS('People import complete.'))
