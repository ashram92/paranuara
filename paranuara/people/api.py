from collections import namedtuple

from django.db.models import Q

from paranuara.people.models import Person, FriendRelationship

CommonFriends = namedtuple('CommonFriends',
                           ['person_1', 'person_2', 'common_friends'])


def retrieve_common_friends_between_users(person_1_id, person_2_id):
    """Given 2 people retrieve a list of their friends in common
    which have brown eyes and are still alive.

    Query I replicated:

     SELECT `people_person`.`id`,
    `people_person`.`hash_id`, `people_person`.`guid`,
    `people_person`.`has_died`, `people_person`.`balance`,
    `people_person`.`picture_url`, `people_person`.`age`,
    `people_person`.`eye_color`, `people_person`.`name`,
    `people_person`.`gender`, `people_person`.`email`,
    `people_person`.`phone`, `people_person`.`address`,
    `people_person`.`about` , `people_person`.`greeting`,
    `people_person`.`registered_at`, `people_person`.`company_id` FROM
    `people_person` WHERE ((`people_person`.`id` IN (SELECT U0.`person_2_id`
    AS Col1 FROM `people_friendrelationship` U0 WHERE U0.`person_1_id` = 1)
    OR `people_person`.`id` IN (SELECT U0.`person_1_id` AS Col1 FROM
    `people_friendrelationship` U0 WHERE U0.`person_2_id` = 1)) AND (
    `people_person`.`id` IN (SELECT U0.`person_2_id` AS Col1 FROM
    `people_friendrelationship` U0 WHERE U0.`person_1_id` = 2) OR
    `people_person`.`id` IN (SELECT U0.`person_1_id` AS Col1 FROM
    `people_friendrelationship` U0 WHERE U0.`person_2_id` = 2)) AND
    `people_person`.`has_died` = False AND `people_person`.`eye_color` =
    "brown")

    Since Mysql has some constraints regarding unions and intersects, I
    implemented this using the AND and OR clauses.

    """

    person_1 = Person.objects.get(pk=person_1_id)
    person_2 = Person.objects.get(pk=person_2_id)

    q1 = FriendRelationship.objects.filter(
        person_1_id=person_1_id).values_list('person_2_id', flat=True)
    q2 = FriendRelationship.objects.filter(
        person_2_id=person_1_id).values_list('person_1_id', flat=True)

    q3 = FriendRelationship.objects.filter(
        person_1_id=person_2_id).values_list('person_2_id', flat=True)
    q4 = FriendRelationship.objects.filter(
        person_2_id=person_2_id).values_list('person_1_id', flat=True)

    final_query = Person.objects.filter(
        Q(Q(id__in=q1) | Q(id__in=q2)) &
        Q(Q(id__in=q3) | Q(id__in=q4))
    ).filter(has_died=False, eye_color='brown')

    return CommonFriends(person_1=person_1,
                         person_2=person_2,
                         common_friends=list(final_query))
