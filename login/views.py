from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import user_serializer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication



@api_view(['POST'])
def login(request):
    
    # Function of django.shortcuts that validate if the user is created
    user = get_object_or_404(User, username=request.data['username'])
    
    if not user.check_password(request.data['password']):
        # If the password written is false
        return Response({"error": "Invalid Password", "message": "Incorrect password"}, status=status.HTTP_400_BAD_REQUEST)
    
    # Tuple (the token and a boolean variable called created)
    token, created = Token.objects.get_or_create(user=user)
    
    # User in json object
    serializer = user_serializer(instance=user)
    
    return Response({"token": token.key, "user": serializer.data, "message": "Login Succefull"}, status=status.HTTP_200_OK)



@api_view(['POST'])
def register(request):
    """This function validates if the user is created, if the user is in the database
    the user will have a generated token that is valid to acces

    Args:
        request (_type_): _description_

    Returns:
        Response: Depending on the situation returns a response with the data or with the error
    """
    
    serializer = user_serializer(data=request.data)
    
    #If the data sent by the front-end is valid (have acces with the token)
    if serializer.is_valid():
        serializer.save()
        
        user =User.objects.get(username=serializer.data['username'])
        user.set_password(serializer.data['password'])
        user.save()
        
        # Return the token and the user data
        token = Token.objects.create(user=user)
        return Response({'token': token.key, 'user': serializer.data}, status=status.HTTP_201_CREATED)
    
    # If the data sent by the front-end are not valid 
    return Response (serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    print(request.data)
    return Response({}) 

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def profile(request):
    
    print(request.user)
    
    
    return Response("You are login with: {}". format(request.user.username), status=status.HTTP_200_OK)