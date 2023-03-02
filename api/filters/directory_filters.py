from rest_framework import filters


class RootDirectoryFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        only_root = request.query_params.get('only_root', None)
        if only_root is None:
            return queryset
        return queryset.filter(parent_dir=None)
