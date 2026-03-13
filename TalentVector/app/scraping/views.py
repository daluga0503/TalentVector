from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser



from rest_framework.response import Response

from .services import run_scraping
from .serializers  import ScrapingResultSerialzer

class RunScrappingJobs(APIView):
    permission_classes = [IsAdminUser]

    def post(self, _):
        result = run_scraping()
        serializer = ScrapingResultSerialzer(result)
        return Response(serializer.data)