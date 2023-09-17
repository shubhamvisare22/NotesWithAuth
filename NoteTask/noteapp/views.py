from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status, permissions
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


# custom imports
from .serializers import NoteSerializer
from .models import NoteModel
from .paginations import CustomPagination

'''---------- User Related view --------'''


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password)
        # Generate a token for the user
        token, _ = Token.objects.get_or_create(user=user)

        return Response({'token': token.key}, status=status.HTTP_201_CREATED)
    return Response({'error': 'Invalid Request Method'}, status=status.HTTP_400_BAD_REQUEST)


'''-------- Notes Related Views --------'''


def sort_notes(queryset, sort_param):
    if sort_param not in ['created_at', 'updated_at']:
        return queryset
    return queryset.order_by(f'-{sort_param}')  # recently updated or created

# Create Notes


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_note(request):
    serializer = NoteSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response({'msg': 'Note created successfully.'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# List Note
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def list_notes(request):
    if request.method == 'GET':

        # sorting on update_at or created_at (default:created_at)
        sort_param = request.GET.get('sort', 'created_at')
        note_objs = NoteModel.objects.filter(user=request.user)
        sorted_note_objs = sort_notes(note_objs, sort_param)

        # pagination here
        paginator = CustomPagination()
        result_pages = paginator.paginate_queryset(sorted_note_objs, request)
        serializer = NoteSerializer(result_pages, many=True)

        msg = 'All Note fetched successfully.'
        if serializer.data == []:
            msg = 'No Notes Found!'

        return paginator.get_paginated_response({'msg': msg, 'notes': serializer.data})
    return Response({'msg': 'Invalid Request Method'}, status=status.HTTP_400_BAD_REQUEST)


# Retrieve Note
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def retrieve_note(request, id):
    if request.method == 'GET':
        try:
            retrive_obj = NoteModel.objects.get(id=id, user=request.user)
            serializer = NoteSerializer(retrive_obj)
            return Response({'msg': ' Note fetched successfully.', 'notes': serializer.data}, status=status.HTTP_200_OK)
        except NoteModel.DoesNotExist:
            return Response({'msg': 'Given Id does not exists.'}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'msg': 'Invalid Request Method'}, status=status.HTTP_400_BAD_REQUEST)


# Update Note
@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def update_note(request, id):
    if request.method == 'PUT':
        try:
            retrive_obj = NoteModel.objects.get(id=id, user=request.user)
            serializer = NoteSerializer(retrive_obj, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'msg': ' Note Updated successfully.', 'notes': serializer.data}, status=status.HTTP_200_OK)
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except NoteModel.DoesNotExist:
            return Response({'msg': 'Given Id does not exists.'}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'msg': 'Invalid Request Method'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
@permission_classes([permissions.IsAuthenticated])
def patch_note(request, id):
    if request.method == 'PATCH':

        try:
            retrive_obj = NoteModel.objects.get(id=id, user=request.user)
        except NoteModel.DoesNotExist:
            return Response({'msg': 'Given Id does not exist or you do not have permission to update this note.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = NoteSerializer(
            retrive_obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Note Updated successfully.', 'notes': serializer.data}, status=status.HTTP_200_OK)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    return Response({'msg': 'Invalid Request Method'}, status=status.HTTP_400_BAD_REQUEST)


# Delete Note
@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def delete_note(request, id):
    if request.method == 'DELETE':
        try:
            retrive_obj = NoteModel.objects.get(id=id, user=request.user)
            retrive_obj.delete()
            return Response({'msg': ' Note Deleted successfully.'}, status=status.HTTP_200_OK)
        except NoteModel.DoesNotExist:
            return Response({'msg': 'Given Id does not exists.'}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'msg': 'Invalid Request Method'}, status=status.HTTP_400_BAD_REQUEST)
