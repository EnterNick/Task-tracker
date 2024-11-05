from django.shortcuts import redirect
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSerializer


class UserView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'task_traker/register.html'

    def get(self, request):
        return Response({'serializer': UserSerializer()})

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            # serializer.save()
            return redirect('/')
        return Response({'serializer': UserSerializer(), 'errors': serializer.errors})