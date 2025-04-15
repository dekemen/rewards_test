from django.contrib import admin
from .models import ScheduledReward, RewardLog


@admin.register(ScheduledReward)
class ScheduledRewardAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'amount', 'execute_at')
    list_filter = ('execute_at',)
    search_fields = ('user__username', 'user__email')


@admin.register(RewardLog)
class RewardLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'amount', 'given_at')
    list_filter = ('given_at',)
    search_fields = ('user__username', 'user__email')
