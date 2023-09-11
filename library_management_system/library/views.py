from django.contrib.auth import authenticate, login
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.http import HttpResponse 
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from .models import Book
from .serializers import BookSerializer
from django.conf import settings
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import AccessToken
import jwt

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_books(request):
    try:
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response({'books': serializer.data})
    except Exception as e:
        return Response({"error": e})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_books_checked_out_by_user(request):
    username = request.user.username
    books = Book.objects.filter(checkOutUser = username)
    serializer = BookSerializer(books, many=True)
    return Response({'books': serializer.data})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def checked_out_books(request):
    books = Book.objects.filter(checkedOut=True)
    serializer = BookSerializer(books, many=True)
    return Response({"books": serializer})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def check_out_book(request, book_id):
    dateTime = request.data['datetime']
    checkingOutUser = request.user.username
    print(dateTime)
    try:
        book = Book.objects.get(id=book_id)
        book.checkedOut = True
        book.checkOutUser = checkingOutUser
        book.checkOutTime = dateTime
        book.save()
        print(book.checkOutTime)
        return Response({"message": "Check out has been successfull"})
    except:
        return Response({"message": "CheckOut has been Unsuccessfull"})
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def return_book(request, book_id):
    try:
        book = Book.objects.get(id=book_id)
        book.checkedOut = False
        book.save()
        return Response({"message": "Check out has been successfull"})
    except:
        return Response({"message": "CheckOut has been Unsuccessfull"})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_book(request, book_id):
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return Response({'error': 'Book Not Found'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = BookSerializer(book)
    return Response({'book': serializer.data}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_book(request):
    serializer = BookSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        print(serializer.errors)  # Print the errors here
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_book(request, book_id):
    try:
        book=Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return Response({'error': 'Book not Found'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = BookSerializer(book, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_book(request, book_id):
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)
    
    book.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@permission_classes([AllowAny])
def Login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(request, username=username, password=password)

    if user is not None:
        access_token = AccessToken.for_user(user)
        return Response({'token': str(access_token)}, status = status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if User.objects.filter(username=username).exists():
        return Response({"error": 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = User.objects.create_user(username=username, password=password)
    # access_token = AccessToken.for_user(user)

    # return Response({'token': str(access_token)}, status=status.HTTP_201_CREATED)
    return Response({"message": "Successfully Registered"})