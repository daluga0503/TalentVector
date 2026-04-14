from rest_framework_permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import FavsJobsSerializer

# Create your views here.
class FavsJobsView(APIView):
    permissions_classes = [IsAuthenticated]

    def post_fav(self, request):
        fav = FavsJobsSerializer.create(data=request.data)
        if fav:
            return Response(fav, status=201)
        else:
            return Response({'error': 'Failed to create fav'}, status=400)

    def delete_fav(self, request):
        fav = FavsJobsSerializer.delete(data=request.data)
        if fav:
            return Response({'message': 'Fav deleted successfully'}, status=200)
        else:
            return Response({'error': 'Fav not found'}, status=404)
    
    def get_favs_by_user_id(self, request):
        favs = FavsJobsSerializer.get_favs_by_user_id(data=request.data)
        if favs:
            return Response(favs, status=200)
        else:
            return Response({'error': 'No favs found for the user'}, status=404)