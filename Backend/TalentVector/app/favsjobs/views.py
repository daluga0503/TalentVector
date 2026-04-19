from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import FavsJobs

# Create your views here.
class FavsJobsView(APIView):
    permissions_classes = [IsAuthenticated]

    def get(self, request):
        favs = FavsJobs.objects.filter(user = request.user).values_list('job_id', flat=True)
        return Response(list(favs), status=200)

    def post(self, request):
        job_id = request.data.get('job_id')
        fav, created = FavsJobs.objects.get_or_create(user=request.user, job_id=job_id)
        if created:
            return Response({'message':'Añadido'}, status=201)
        return Response({'message': 'Ya existía'}, status=200)

    def delete(self, request):
        job_id = request.data.get('job_id')
        deleted, _ = FavsJobs.objects.filter(user=request.user, job_id=job_id).delete()
        if deleted:
            return Response({'message': 'Eliminado'}, status=200)
        return Response({'error': 'No encontrado'}, status=404)