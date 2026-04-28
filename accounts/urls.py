from django.urls import path
from .views import *
urlpatterns = [
    path("hisoblar/", AccountListView.as_view(), name="accounts-list"),
    path("hisob-yaratish/", AccountCreateView.as_view(), name="account-create"),
    path("hisob-detal/<int:pk>/", AccountDetailView.as_view(), name="account-detail"),
    path("hisob-tahrir/<int:pk>/", AccountUpdateView.as_view(), name="account-update"),
    path("hisob-uchirish/<int:pk>", AccountDeleteView.as_view(), name="account-delete"),
    path("make-transfer/", MakeTransafer.as_view(), name="create_transfer"),
    path("transfer-list/", TransferListView.as_view(), name = "transfer_list"),
]
