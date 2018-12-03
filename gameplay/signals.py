from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import GameManager


@receiver(pre_save, sender=GameManager)
def clean_event(sender, instance, **kwargs):
    all_groupings = list(instance.event.grouping_set.all())
    for grouping in all_groupings:
        grouping.delete()


# @receiver(post_save, sender=GameManager)
# def set_max_groups(sender, instance, **kwargs):
#     nplayers = instance.event.user_count()
#     instance.max_groups = max_groups(
#         nplayers) if nplayers < 10 else float('inf')
