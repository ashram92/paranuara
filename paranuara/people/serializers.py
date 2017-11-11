from rest_framework import serializers

from paranuara.people.models import Person, Food


class FoodSerializer(serializers.ModelSerializer):

    class Meta:
        model = Food
        fields = ('name',)


class SimplePersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('id', 'name')


class PersonDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Person
        fields = ('username', 'age', 'fruits', 'vegetables')

    username = serializers.CharField()  # Created a unique username due to spec requirement
    age = serializers.CharField()  # Since the specs say return as string
    fruits = FoodSerializer(source='favourite_fruits', many=True)
    vegetables = FoodSerializer(source='favourite_vegetables', many=True)


class AlternatePersonDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Person
        fields = ('name', 'age', 'address', 'phone')


class CommonFriendsSerializer(serializers.Serializer):

    person_1 = AlternatePersonDetailsSerializer()
    person_2 = AlternatePersonDetailsSerializer()
    common_friends = SimplePersonSerializer(many=True)
