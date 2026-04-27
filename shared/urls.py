from django.urls import path
from .views import HomepageView, DashboardView
urlpatterns = [
    path("", HomepageView.as_view(), name = "home"),
    path("dashboard/", DashboardView.as_view(), name="dashboard")
]
