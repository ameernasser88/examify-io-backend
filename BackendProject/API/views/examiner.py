from django.shortcuts import render
from requests.models import to_key_val_list
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from ..serializers import ExamSerializer
from ..models import Exam,Examiner

class ExamApi(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            user = Examiner.objects.get(user = request.user)
            # request.data['examiner'] = user
            serializer = ExamSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                exam_id = serializer.data['id']
                exam = Exam.objects.get(pk = exam_id)
                exam.examiner = user
                exam.save() 
                return Response(serializer.data,status= status.HTTP_201_CREATED)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Examiner.DoesNotExist:
            return Response(status = status.HTTP_403_FORBIDDEN)