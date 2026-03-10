from .services import create_job, list_job, get_job, update_job, delete_job
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .serializers import JobOfferSerializer

# Create your views here.
class JobListCreateView(APIView):
    def get_permissions(self):
        if self.request.method in ['POST']:
            return [IsAdminUser()]
        return [IsAuthenticated()]
    
    def get(self, request):
        filters = {
            'location': request.query_params.get('location'),
            'seniority': request.query_params.get('seniority'),
            'skill': request.query_params.get('skill')
        }

        filters = {k:v for k,v in filters.items() if v}

        jobs = list_job(filters)
        serializer = JobOfferSerializer(jobs, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = JobOfferSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        job = create_job(serializer.validated_data)
        return Response(JobOfferSerializer(job).data, status=201)
    
class JobDetailView(APIView):
    def get_permissions(self):
        if self.request.method in ['PUT', 'DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def get(self, _, job_id):
        job = get_job(job_id)
        if not job:
            return Response({'error':'not found'}, status=404)
        return Response(JobOfferSerializer(job).data)
    
    def put(self, request, job_id):
        serializer = JobOfferSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)

        job = update_job(job_id, serializer.validated_data)
        if not job:
            return Response({'error':'not found'}, status=404)
        return Response(JobOfferSerializer(job).data)
    
    def delete(self, request, job_id):
        job = delete_job(job_id)
        print(job)
        if job is None:
            return Response(
                {'error': 'La oferta con ese ID no ha sido encontrada'},
                status=404
            )
        return Response(
            {'message': f"Oferta {job['name']} - {job['company']} eliminada exitosamente"},
            status=200
            )