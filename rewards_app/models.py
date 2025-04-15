from django.db import models
from manage_app.models import CustomUser
from rewards_app.celery_tasks.tasks import process_scheduled_reward


class ScheduledReward(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_scheduled_rewards')
    amount = models.IntegerField()
    execute_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        is_new = not self.pk
        super().save(*args, **kwargs)
        if is_new:
            process_scheduled_reward.apply_async(args=(self.id, ), eta=self.execute_at)

    class Meta:
        verbose_name = 'Scheduled Reward'
        verbose_name_plural = 'Scheduled Rewards'


class RewardLog(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_reward_log')
    amount = models.IntegerField()
    given_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Reward Log'
        verbose_name_plural = 'Reward Logs'
