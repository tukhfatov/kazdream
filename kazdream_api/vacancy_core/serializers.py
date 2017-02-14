from vacancy_core.models import Vacancy
from rest_framework import serializers


class VacancySerializer(serializers.ModelSerializer):
	class Meta:
		model = Vacancy
		exclude = ('page',)