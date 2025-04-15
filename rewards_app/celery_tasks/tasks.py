from celery import shared_task
from django.utils import timezone


@shared_task
def process_scheduled_reward(reward_id):
    from rewards_app.models import ScheduledReward, RewardLog  # циклический импорт
    try:
        reward = ScheduledReward.objects.get(id=reward_id)
        if reward.execute_at <= timezone.now():
            reward.user.add_coins(reward.amount)
            RewardLog.objects.create(
                user=reward.user,
                amount=reward.amount
            )
            reward.save()
    except ScheduledReward.DoesNotExist:
        pass
