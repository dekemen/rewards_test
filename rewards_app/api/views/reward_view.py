import datetime

from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from rewards_app.api.serializers.reward_serializer import RewardsSerializer
from rewards_app.models import RewardLog, ScheduledReward


class RewardsApiView(APIView):
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        summary="Получение списка наград пользователя",
        description="Возвращает список всех наград, связанных с текущим аутентифицированным пользователем.",
        responses={200: RewardsSerializer(many=True)},
        tags=["Rewards"],
    )
    def get(self, request):
        user_rewards = RewardLog.objects.filter(user=request.user)
        return Response(RewardsSerializer(user_rewards, many=True).data, status=status.HTTP_200_OK)

@extend_schema(
    summary="Добавляет пользователю награду по запросу",
    description="Добавляет пользователю награду по запросу",
    responses={200: RewardsSerializer(many=True)},
    tags=["Rewards"],
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reward_request(request):
    amount = int(request.data.get('amount', 10))
    if amount <= 0:
        return Response({"success": False, "error": "Количество монет не должно быть меньше 0"}, status=status.HTTP_400_BAD_REQUEST)
    last_user_reward = RewardLog.objects.filter(user=request.user).order_by('-given_at').first()
    now = timezone.now()
    if last_user_reward and last_user_reward.given_at + datetime.timedelta(days=1) >= now:
        remaining_time = (last_user_reward.given_at + datetime.timedelta(days=1)) - now
        hours, remainder = divmod(remaining_time.seconds, 3600)
        minutes = remainder // 60
        time_str = f"{remaining_time.days} days, {hours} hours, {minutes} minutes"
        return Response({"success": False, "result": f"Награда не добавлена! Подождите еще: {time_str}"},status=status.HTTP_200_OK)
    try:
        scheduled_reward = ScheduledReward.objects.create(
            user=request.user,
            amount=amount,
            execute_at=now + datetime.timedelta(minutes=5),
        )
        return Response({"success": True, "result": "Награда добавлена"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"success": False, "error": f"Ошибка при добавлении награды: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
