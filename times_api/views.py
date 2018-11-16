from django.shortcuts import render
from django.http import HttpResponse, Http404
from .models import Category
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CategorySerializer
from django.core.exceptions import FieldError
from rest_framework import status
from .tasks import send_email
from datetime import datetime, timedelta


# Create your views here.

class CategoryList(APIView):

    # /abc.com?params=id|name|is_featured
    def get_object_by_name(self, name):
        name = ''.join(name)
        try:
            return Category.objects.filter(name__icontains=name)
        except Category.DoesNotExist:
            raise Http404

    def get_object_by_featured(self, value):
        value = (''.join(value)).lower()
        boolean = False
        if value == 'true':
            boolean = True
        try:
            return Category.objects.filter(is_featured=boolean)
        except Category.DoesNotExist:
            raise Http404


    def get_object_by_featured_and_name(self, value, name):
        value = (''.join(value)).lower()
        name = ''.join(name)
        boolean = False
        if value == 'true':
            boolean = True
        try:
            return Category.objects.filter(is_featured=boolean,name__icontains=name)
        except Category.DoesNotExist:
            raise Http404

    def get(self, request):
        queryparams = dict(request.GET)
        print(queryparams)
        if len(queryparams) == 0:
            all_data = Category.objects.all()
            serializer = CategorySerializer(all_data, many=True)
            return Response({'data': serializer.data})
        else:
            if 'params' in queryparams:
                raw_query = queryparams['params']
                cleaned_list = ''.join(raw_query).split('|')
                try:
                    result = Category.objects.values(*cleaned_list)
                    serializer = CategorySerializer(result, many=True, partial=True)
                    return Response({'api_success': True, 'data': serializer.data})
                except FieldError as i:
                    return Response({'api_success': False, 'error': str(i)})
            if 'name' in queryparams and 'is_featured' in queryparams:
                result = self.get_object_by_featured_and_name(name=queryparams['name'],value=queryparams['is_featured'])
                serializer = CategorySerializer(result, many=True)
                return Response({'data': serializer.data})
            elif 'name' in queryparams:
                result = self.get_object_by_name(name=queryparams['name'])
                serializer = CategorySerializer(result, many=True)
                return Response({'data': serializer.data})
            elif 'is_featured' in queryparams:
                result = self.get_object_by_featured(value=queryparams['is_featured'])
                serializer = CategorySerializer(result, many=True)
                return Response({'data': serializer.data})

            else:
                return Response({'error': 'Invalid Request.'})

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            send_email.apply_async(('shivam.singhal212@gmail.com', serializer.data), countdown=900)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)