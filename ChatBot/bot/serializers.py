import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from django.shortcuts import redirect
from fpdf import FPDF
from pdfminer.high_level import extract_text
from rest_framework import serializers
from django.conf import settings
from django.db import transaction, DatabaseError
import pandas as pd
from .models import *


def reverseString(str):
    return str[::-1]


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class TypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = '__all__'

class AnswersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('content',)

class ChatbotSerializer(serializers.Serializer):
    client_name = serializers.CharField(max_length=200)
    chat = serializers.CharField(max_length=1024)
    categories_id = serializers.CharField(max_length=1024)

    def save(self, **kwargs):
        categories_dict = {'1': 'feature 1', '2': 'feature 2',
                           '3': 'feature 3', '4': 'feature 4'}
        client_name = self.validated_data["client_name"]
        chat = self.validated_data["chat"]
        categories_id = self.validated_data["categories_id"]
        getID = categories_id.split(',')
        categories = ''
        for i in getID:
            categories += f'{categories_dict.get(i)},'
        text = f"Client: {client_name} - Categories: {categories} - Chat: {reverseString(chat)}"
        return text


class ReadExcelSerializer(serializers.Serializer):
    file = serializers.FileField()
    
    def bulk_create_object(self, Object, array_src, key='name'):
        array = list(array_src)
        bulk_object = Object.objects.filter(**{f'{key}__in':array})
        for object in bulk_object.values():
            if object[key] in array:
                array.remove(object[key])
        if len(array)>0:
            array = [Object(**{key:value}) for value in array]
            Object.objects.bulk_create(array)
        return Object.objects.filter(**{f'{key}__in':array_src}).values()
    
    def bulk_create_question(self,Category,dict,array_ids):
        questions_query = Category.objects.filter(Q(name__in=dict.keys())&Q(parent_id__in=array_ids))
        for question in questions_query.values():
            if question['name'] in dict.keys():
                dict.pop(question['name'], None)
        if len(dict)>0:
            array = []
            for key in dict:
                for id in dict[key]:
                    array.append(Category(name=key, parent_id=id))
            return Category.objects.bulk_create(array)
        return Category.objects.all()
        
    def save(self,**kwargs):
        upload = self.validated_data['file']
        if not upload.name.endswith(('.xlsx')):
            return "invalid uploaded"
        media_files = os.path.join(settings.MEDIA_ROOT,'files')
        file_path = os.path.join(media_files, 'text2')
        xl = pd.ExcelFile(upload.file.read())
        sheets_name = [xl.sheet_names[0],xl.sheet_names[2]]
        print(sheets_name)
        with transaction.atomic():
            for sheet_name in sheets_name:
                sheet = xl.parse(sheet_name)
                title = list(sheet.keys())
                current_types = self.bulk_create_object(Object=Type, array_src=title[3:])
                categories_name = title[0]
                categories_verbose = [str(category).lower().replace('\n','').replace('\t','') for category in sheet[categories_name]]
                categories = list(set(categories_verbose))
                current_categories = self.bulk_create_object(Object=Category, array_src=categories)
                questions_name = title[1]
                questions = [str(question).lower().replace('\n','').replace('\t','') for question in sheet[questions_name]]
                dict_parent_id_and_question = {}
                array_ids = set()
                print(current_categories)
                for i in range(len(questions)):
                    for current_category in current_categories:
                        if current_category['name'] == categories_verbose[i]:
                            array_ids.add(current_category['id'])
                            dict_parent_id_and_question[questions[i]] = [*dict_parent_id_and_question.get(questions[i],[]),current_category['id']]
                            break
                self.bulk_create_question(Category=Category,dict=dict_parent_id_and_question,array_ids=array_ids)
                categories_all = Category.objects.all()
                types_all = Type.objects.all()
                dict_categories = {categories['name']: categories['id'] for categories in categories_all.values()}
                dict_types = {types['name']: types['id'] for types in types_all.values()}
                types_name = list(title[3:])
                bulk_answer = []
                for type_name in types_name:
                    type_sheet = sheet[type_name]
                    for i in range(len(type_sheet)):
                        content = str(type_sheet[i]).lower().strip('\t')
                        id_category = None
                        if questions[i] == 'nan':
                            id_category = dict_categories[categories_verbose[i]]
                        else:
                            id_category = dict_categories[questions[i]]
                        id_type = dict_types[type_name]
                        bulk_answer.append(Answer(content=content,category_id=id_category,type_id=id_type))
                Answer.objects.bulk_create(bulk_answer)