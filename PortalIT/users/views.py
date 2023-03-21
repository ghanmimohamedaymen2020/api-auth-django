from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from . serializres import UserSerializers
from rest_framework.views import  APIView
from . models import User
import jwt, datetime


class RegisterView(APIView):
    def post(self , request):
        serializers = UserSerializers(data=request.data)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response(serializers.data)
        

class LoginView(APIView):
    def post(self , request):
        email = request.data['email']
        password = request.data['password']


        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User is not found !')
        
        if not user.check_password(password):
            raise AuthenticationFailed('invalid password')
        
        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret',algorithm='HS256').encode('utf-8')

        response = Response()

        response.set_cookie(key='jwt',value=token , httponly=True)
        response.data = {
          'jwt': token
        }


        
        return response
    
class UserView(APIView):
    
    def get(self , request):
        pass
     