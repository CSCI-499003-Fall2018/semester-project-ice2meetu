from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import GameManager


@receiver(pre_save, sender=GameManager)
def clean_event(sender, instance, **kwargs):
    if instance.pk == None:
        all_groupings = list(instance.event.grouping_set.all())
        for grouping in all_groupings:
            grouping.delete()

