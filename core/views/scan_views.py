from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from core.serializers.scan_serializers import ScanSerializer
from core.serializers.scan_result_serializers import ScanResultSerializer

from core.tasks import scan

from core.models.scan import ScanTimeSeriesResult

from django_celery_beat.models import PeriodicTask

from django.shortcuts import get_list_or_404, get_object_or_404


class ScanListCreateView(generics.ListCreateAPIView):
    queryset  = PeriodicTask.objects.all()
    serializer_class = ScanSerializer

class ScanRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PeriodicTask.objects.all()
    serializer_class = ScanSerializer
    lookup_field = 'name'


@api_view(['GET'])
def get_scan_results(request, name):
    # by default return only the most recent result
    latest = int(request.query_params.get('latest', 1))

    if latest == 1:
        # return the most recent result if query params is not specified
        try:
            result = ScanTimeSeriesResult.objects.latest('created')
            serializer = ScanResultSerializer(result)
        except ScanTimeSeriesResult.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        result = get_list_or_404(ScanTimeSeriesResult.objects.order_by('created'),
                                 scan_name=name)

        if latest > 1:
            latest = latest * -1
            serializer = ScanResultSerializer(result[latest:], many=True)
        else:
            serializer = ScanResultSerializer(result, many=True)

    return Response(serializer.data)
