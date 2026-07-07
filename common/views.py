from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView


class BaseAPIView(GenericAPIView):

    def success_response(self, data=None, message="Success", status_code=status.HTTP_200_OK):
        return Response(
            {
                "success": True,
                "message": message,
                "data": data
            },
            status=status_code
        )

    def error_response(self, message="Error", data=None, status_code=status.HTTP_400_BAD_REQUEST):
        return Response(
            {
                "success": False,
                "message": message,
                "data": data
            },
            status=status_code
        )
