from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from django.forms import model_to_dict
from django.http import JsonResponse
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView
from django.core import serializers

from movies.models import FilmWork
from .serializers import FilmWorkSerializer


class MoviesApiMixin:
    model = FilmWork
    http_method_names = ['get']

    def get_queryset(self):
        return FilmWork.objects.prefetch_related('genres', 'persons')

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)


class MoviesListApi(MoviesApiMixin, BaseListView):

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = self.get_queryset()
        paginator, page, queryset, is_paginated = self.paginate_queryset(
            queryset,
            50
        )
        context = {
            'count': paginator.count,
            'total_pages': paginator.num_pages,
            'prev': page.number-1 if page.has_previous() else page.number,
            'next': page.number+1 if page.has_next() else page.number,
            'results': FilmWorkSerializer(page.object_list, many=True).data,
        }
        return context


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):
    pk_url_kwarg = 'uuid'

    def get_context_data(self, *, object=None, **kwargs):
        context = FilmWorkSerializer(object).data
        return context
