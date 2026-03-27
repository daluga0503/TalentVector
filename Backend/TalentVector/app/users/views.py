from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.authentication import JWTAuthentication

from .services import get_all_users

from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import RegisterSerializer, CustomTokenSerializer, UserListSerializer

User = get_user_model()

# Es el controller en Java

class UserListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, _): # Usamos '_' porque request no se usa, es una buena práctica
        users = get_all_users()
        # 2. Instanciamos el serializer con los datos obtenidos
        # many=True es obligatorio porque users_queryset es una lista de objetos
        serializer = UserListSerializer(users, many=True)
        
        # 3. Retornamos la respuesta con los datos transformados en JSON
        return Response(
            serializer.data, 
            status=status.HTTP_200_OK
        )

class RegisterView(APIView):
# Definimos que cualquier persona puede registrarse
    permission_classes = [AllowAny]
    authentication_classes = [] # Importante dejarlo vacío para el registro

    def post(self, request):
        # 1. Pasamos los datos al serializer
        serializer = RegisterSerializer(data=request.data)
        
        # 2. Validamos
        if serializer.is_valid():
            # 3. Guardamos (esto llamará al método create de tu serializer o a tu service)
            user = serializer.save()
            return Response({
                "message": "Usuario creado con éxito",
                "email": user.email
            }, status=status.HTTP_201_CREATED)
        
        # 4. Si hay errores (email duplicado, pass corta, etc.)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProfileView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        return Response({
            'email': user.email,
            'name': user.name,
            'surname': user.surname,
            'username': user.username
        })

class CustomTokenView(TokenObtainPairView):
    serializer_class = CustomTokenSerializer
    permission_classes = [AllowAny]
