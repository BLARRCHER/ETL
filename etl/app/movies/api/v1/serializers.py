from rest_framework import serializers
from movies.models import FilmWork


class FilmWorkSerializer(serializers.ModelSerializer):

    class Meta:
        model = FilmWork
        fields = '__all__'
        depth = 1
