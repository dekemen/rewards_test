from django.urls import path

from rewards_app.api.views.reward_view import RewardsApiView, reward_request

urlpatterns = [
    path('rewards/', RewardsApiView.as_view(), name='rewards-list'),
    path('rewards/request/', reward_request, name='rewards-request'),
]