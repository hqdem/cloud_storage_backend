from rest_framework import filters


class RootFilesFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        only_root = request.query_params.get('only_root', None)
        if only_root is None:
            return queryset
        return queryset.filter(directory=None)
