from rest_framework import views, status
from rest_framework.response import Response
from .serializers import WeatherApiSerializer, UserSerializer, TokenSerializer
from .models import Weather
from .utils import request_to_weatherapi
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import TokenAuthentication

class CodeExplainView(views.APIView):
    serializer_class = WeatherApiSerializer
    permission_classes = [IsAuthenticated]
    def get(self, request):
        city = request.data["city"]
        print("=============", city)
        output = request_to_weatherapi(city)
        if city:
            qset = Weather.objects.filter(city__iexact=city)
            if qset.exists():
                instance = Weather.objects.get(city__iexact=city)
                serializer = WeatherApiSerializer(instance, data=output)
            else:
                # print("=============", output)
                serializer = WeatherApiSerializer(data=output)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class UserView(views.APIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        qs = User.objects.all()
        serializer = self.serializer_class(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TokenView(ObtainAuthToken):
    serializer_class = TokenSerializer

