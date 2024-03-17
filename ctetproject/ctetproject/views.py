from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response


def index(request):
    return render(request, "index.html")


class CtetAPIView(APIView):
    def get(self, request):
        return Response({})
