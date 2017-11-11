from rest_framework import serializers

from paranuara.people.models import Person, Food


class FoodSerializer(serializers.ModelSerializer):

    class Meta:
        model = Food
        fields = ('name',)


class PersonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Person
        fields = ('username', 'age', 'fruits', 'vegetables')

    username = serializers.CharField()  # Created a unique username due to spec requirement
    age = serializers.CharField()  # Since the specs say return as string
    fruits = FoodSerializer(source='favourite_fruits', many=True)
    vegetables = FoodSerializer(source='favourite_vegetables', many=True)
