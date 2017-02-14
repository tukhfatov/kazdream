from vacancy_core.models import Vacancy
from rest_framework import viewsets
from rest_framework.response import Response
from vacancy_core.serializers import VacancySerializer


# Create your views here.
class VacancyViewSet(viewsets.ModelViewSet):

	queryset = Vacancy.objects.all().order_by('-page')	
	serializer_class = VacancySerializer

vacancy_list = VacancyViewSet.as_view({'get': 'list'})