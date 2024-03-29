from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer
from .models import User
from rest_framework.exceptions import AuthenticationFailed
import jwt,datetime
# Create your views here.
class RegisterView(APIView):
    def post(self,request):
        serializer = UserSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print(serializer.data)
        return Response(serializer.data)
        
class LoginView(APIView):
    def post(self,request):
        username = request.data['username']
        password = request.data['password']
        user = User.objects.filter(username=username).first()
        if user is None:
            raise AuthenticationFailed('user not found')
        if not user.check_password(password):
            raise AuthenticationFailed('incorrect password')
        payload = {
            'id':user.id,
            'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat':datetime.datetime.utcnow()
        }
        token = jwt.encode(payload,'secret', algorithm='HS256')
        response =  Response()
        response.set_cookie(key='jwt',value=token,httponly=True)
        response.data = {
            "jwt":token
        }
        return response 
        
class UserView(APIView):
    def get(self,request):
        token = request.COOKIES.get('jwt')
        # return Response(token)
        if not token:
             raise AuthenticationFailed('unauthenticated')
        try:
            payload = jwt.decode(token,'secret',algorithms='HS256')
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('unauthenticated')
        print(payload)
        user=  User.objects.get(id = payload['id'])
        serializer = UserSerializer(user)
        # print(serializer.data)
        return Response(serializer.data)
class LogoutView(APIView):
    def post(self,request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message':'logout success'
        }
        return response
        