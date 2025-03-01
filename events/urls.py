from django.urls import path
from .views import RegisterView, LoginView, EventListCreateView, TicketPurchaseView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("events/", EventListCreateView.as_view(), name="events"),
    path("events/<int:id>/purchase/", TicketPurchaseView.as_view(), name="ticket-purchase"),
]
