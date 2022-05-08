from django.contrib.auth import get_user_model
#this one is refer to customized user model if AUTH_USER_MODEL changed to a different user model
User = get_user_model()
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions

#api view is most generic, viewsets better for clearer CRUDs

class SignupView(APIView):
    
    permission_classes = (permissions.AllowAny,)
    
    def post(self, request, format=None):
        data = self.request.data

        name = data['name']
        email = data['email']
        password = data['password']
        password2 = data['password2']
        
        if password == password2:
            if User.objects.filter(email= email).exists():
                return Response({'error':'email already exists'})
            else:
                if len(password)<6:
                    return Response({'error':'Password must be at least 6 chars'})
                else:
                    user= User.objects.create_user(email=email,name=name,password=password)
                    
                    user.save()
                    return Response({'success':'User created succesfully'})
        
        else:
            return Response({'error':'Passwords do not match}'})