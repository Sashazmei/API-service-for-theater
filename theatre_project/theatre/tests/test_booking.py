from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from theatre.models import Performance, TheatreHall, Play

class BookingTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        hall = TheatreHall.objects.create(name="Main", rows=5, seats_in_row=5)
        play = Play.objects.create(title="Hamlet", description="Classic")
        play.actors.set([])  # empty M2M
        play.genres.set([])

        self.performance = Performance.objects.create(
            play=play, theatre_hall=hall, show_time="2030-01-01T19:00:00Z"
        )

    def test_register_login_book_ticket(self):
        # Login
        response = self.client.post("/api/token/", {"username": "testuser", "password": "testpass"})
        self.assertEqual(response.status_code, 200)
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        # Book tickets
        response = self.client.post("/api/book/", {
            "performance_id": self.performance.id,
            "tickets": [{"row": 1, "seat": 1}]
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data["tickets"]), 1)
