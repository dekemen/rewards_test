from django.urls import path
from manage_app.api.views.user_view import UserApiView

urlpatterns = [
    path('profile/', UserApiView.as_view(), name='user-profile'),
]