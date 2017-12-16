from rest_framework.views import APIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from .serializers import WebHookSerializer


class WebHookView(APIView):
    parser_classes = (FormParser, MultiPartParser)

    def get(self, request):
        data = request.data
        serializer = WebHookSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Received and saved"}, 200)
        else:
            return Response({"message": "Error", "errors": serializer.errors}, 400)

