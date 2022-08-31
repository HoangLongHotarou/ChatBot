from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import ChatbotSerializer,CategoriesSerializer, TypesSerializer, AnswersSerializer,ReadExcelSerializer
from .models import *
from .pagination import DefaultPagination
from .filters import CategoryFilter, AnswerFilter
# Create your views here.


class ChatbotViewSet(viewsets.ViewSet):
    http_method_names = ['post']

    serializer_class = ChatbotSerializer

    def create(self, request):
        serializers = ChatbotSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        test = serializers.save()
        print(test)
        test = {"Dest": test}
        return Response(test)


class CategoriesViewSet(viewsets.ModelViewSet):
    http_method_names = ['get']
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer
    
    filter_backends = [DjangoFilterBackend]
    filter_class = CategoryFilter
    pagination_class = DefaultPagination

class TypesViewSet(viewsets.ModelViewSet):
    http_method_names = ['get']
    queryset = Type.objects.all()
    serializer_class = TypesSerializer
    pagination_class = DefaultPagination

class AnswersViewSet(viewsets.ModelViewSet):
    http_method_names = ['get']
    queryset = Answer.objects.all()
    serializer_class = AnswersSerializer
    filter_backends = [DjangoFilterBackend]
    filter_class = AnswerFilter
    pagination_class = DefaultPagination

class ReadExcelViewSet(viewsets.ViewSet):
    http_method_names = ['post']
    serializer_class = ReadExcelSerializer
    def create(self, request):    
        serializers = ReadExcelSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        test = serializers.save()
        return Response(test)