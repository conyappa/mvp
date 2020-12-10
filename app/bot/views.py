from rest_framework import generics
from rest_framework.response import Response


# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


class Bot(generics.GenericAPIView):
    def post(self, request):
        message = request.body.decode()
        logger.error(message)
        return Response()
