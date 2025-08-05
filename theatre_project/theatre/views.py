from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Genre, Actor, Play, TheatreHall, Performance, Reservation, Ticket
from .serializers import (
    GenreSerializer, ActorSerializer, PlaySerializer,
    TheatreHallSerializer, PerformanceSerializer,
    ReservationSerializer, TicketSerializer
)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class ActorViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer


class PlayViewSet(viewsets.ModelViewSet):
    queryset = Play.objects.all()
    serializer_class = PlaySerializer


class TheatreHallViewSet(viewsets.ModelViewSet):
    queryset = TheatreHall.objects.all()
    serializer_class = TheatreHallSerializer


class PerformanceViewSet(viewsets.ModelViewSet):
    queryset = Performance.objects.all()
    serializer_class = PerformanceSerializer

    @action(detail=True, methods=["get"])
    def available_seats(self, request, pk=None):
        performance = self.get_object()
        hall = performance.theatre_hall
        taken_tickets = Ticket.objects.filter(performance=performance)
        taken = {(t.row, t.seat) for t in taken_tickets}

        available = []
        for row in range(1, hall.rows + 1):
            for seat in range(1, hall.seats_in_row + 1):
                if (row, seat) not in taken:
                    available.append({"row": row, "seat": seat})

        return Response(available)


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

class BookTicketsView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        performance_id = request.data.get("performance_id")
        tickets_data = request.data.get("tickets", [])

        if not performance_id or not tickets_data:
            return Response({"error": "Invalid data"}, status=400)

        performance = Performance.objects.get(id=performance_id)
        reservation = Reservation.objects.create(user=request.user)

        created_tickets = []
        for ticket in tickets_data:
            row = ticket["row"]
            seat = ticket["seat"]
            if Ticket.objects.filter(performance=performance, row=row, seat=seat).exists():
                return Response(
                    {"error": f"Seat row {row}, seat {seat} already taken"},
                    status=400
                )
            created = Ticket.objects.create(
                performance=performance,
                reservation=reservation,
                row=row,
                seat=seat
            )
            created_tickets.append({
                "row": row,
                "seat": seat
            })

        return Response({
            "reservation_id": reservation.id,
            "tickets": created_tickets
        }, status=status.HTTP_201_CREATED)

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if User.objects.filter(username=username).exists():
            return Response({"error": "User already exists"}, status=400)

        user = User.objects.create_user(username=username, password=password)
        return Response({"message": "User created"}, status=status.HTTP_201_CREATED)
