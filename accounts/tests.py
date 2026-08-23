from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class AuthenticationFlowTests(TestCase):
    def test_logout_requires_post_and_logs_user_out(self):
        user = get_user_model().objects.create_user(username="customer", password="password123")
        self.client.force_login(user)

        response = self.client.post(reverse("accounts:logout"))

        self.assertRedirects(response, reverse("cars:car_list"))
        self.assertFalse(response.wsgi_request.user.is_authenticated)