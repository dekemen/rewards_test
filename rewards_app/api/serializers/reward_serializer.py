from rest_framework import serializers

from rewards_app.models import RewardLog


class RewardsSerializer(serializers.ModelSerializer):
    given_at = serializers.DateTimeField(format='%d.%m.%Y %H:%M:%S')

    class Meta:
        model = RewardLog
        fields = ('id', 'amount', 'given_at', 'user')
