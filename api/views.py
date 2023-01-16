from django.shortcuts import render
from api.serializers import UserRegistrationSerializer,UserLoginSerializer,UserProfileSerializer,UserChangePasswordSerializer,SendPasswordResetEmailSerializer,UserPasswordRestSerializer
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.views import APIView
from api.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated  
def get_token_for_user(user):
    refresh=RefreshToken.for_user(user)
    return {
        'refresh':str(refresh),
        'access':str(refresh.access_token)
    }

class UserRegistrationView(APIView):
  renderer_classes=[UserRenderer]  
  def post(self, request, format=None):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        user = serializer.save()
        token=get_token_for_user(user)
        return Response({'token':token,'msg':'Registration Successful'}, status=201)

    return Response(serializer.errors, status=400)    


class UserLoginView(APIView):
  renderer_classes=[UserRenderer]  
  def post(self, request, format=None):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        email = serializer.data.get('email')
        password = serializer.data.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
         token=get_token_for_user(user)
         return Response({'token':token,'msg':'Login Success'}, status=200)
        else:
         return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}}, status=404)
    
    return Response(serializer.error_messages, status=400)


class UserProfileView(APIView):
    renderer_classes=[UserRenderer]
    permission_classes=[IsAuthenticated]
    def get(self,request,format=None):
        serializer=UserProfileSerializer(request.user)
        return Response(serializer.data,status=200)  


class UserChangePasswordView(APIView):
    renderer_classes=[UserRenderer]
    permission_classes=[IsAuthenticated]
    def post(self,request,format=None):
        serializer=UserChangePasswordSerializer(data=request.data,
        context={'user':request.user})

        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password changed Successfuly'})

        return Response(serializer.error_messages, status=400)    


class SendPasswordResetEmailView(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request,format=None):
        serializer=SendPasswordResetEmailSerializer(data=request.data) 
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password reset link send.Please check your Email'},status=200)    
        return Response(serializer.error_messages,status=400)


class UserPasswordResetView(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request,uid,token,format=None):
        serializer=UserPasswordRestSerializer(data=request.data,context={'uid':uid,'token':token})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password changed Successfuly now'})

        return Response(serializer.errors, status=400)  

