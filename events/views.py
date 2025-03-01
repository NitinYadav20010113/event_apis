from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import User, Event, Ticket
from .serializers import UserSerializer, EventSerializer, TicketSerializer
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from . permissions import IsAdminUserRole


# This function is regsitering the user i have used the generic.CreateAPIView because it reduce the boiler code this can also be done 
# using the apiview 
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


# This view is for logging the user this code first checks the username and passowrd and then generate the token which is further used in logging
class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        user = authenticate(username=request.data["username"], password=request.data["password"])
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({"refresh": str(refresh), "access": str(refresh.access_token)})
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


# This generic view does two thing first if the request is get it lists the events 
# If the request is post it checks if the permission is admin permission if the user is admin it will create the event
class EventListCreateView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUserRole()]
        return super().get_permissions()


# This is a apiview which is used to create the ticket it checks if the quantity and ticket sold should not be greater than the total ticket 
class TicketPurchaseView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        user = request.user
        event = get_object_or_404(Event, id=id)
        quantity = int(request.data.get("quantity", 0))

        if event.tickets_sold + quantity > event.total_tickets:
            return Response({"error": "Not enough tickets available"}, status=status.HTTP_400_BAD_REQUEST)

        event.tickets_sold += quantity
        event.save()

        ticket = Ticket.objects.create(user=user, event=event, quantity=quantity)
        return Response(TicketSerializer(ticket).data, status=status.HTTP_201_CREATED)
