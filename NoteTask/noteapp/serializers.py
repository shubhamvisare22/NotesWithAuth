from .models import NoteModel
from rest_framework import serializers
from django.contrib.auth.models import User

'''-------- Note Ralated Serializer ---------'''


class NoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = NoteModel
        fields = ['id', 'title', 'content',  'created_at', 'updated_at']

    def validate(self, data):
        title = data.get('title')
        content = data.get('content')

        if self.partial:

            if str(title).strip() == '':
                raise serializers.ValidationError('Please Enter the Title.')

            if str(content).strip() == '':
                raise serializers.ValidationError('Please Enter the Content.')

            return data
        else:

            if not title or str(title).strip() == '':
                raise serializers.ValidationError('Please Enter the Title.')

            if not content or str(content).strip() == '':
                raise serializers.ValidationError('Please Enter the Content.')

            return data
