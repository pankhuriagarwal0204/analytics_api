from django.conf import settings
settings.configure()
import django
django.setup()
import serializers
import models
import calendar_utils


class QuerysetProcessors:
    def __init__(self):
        self.calendar = calendar_utils.calendar_iterators()

    def get_filtered_data_morcha(self, start, end, pk):
        verified = models.Intrusion.objects.filter(verified_datetime__gte=start, verified_datetime__lt=end, morcha=pk)
        non_human = models.Intrusion.objects.filter(non_human_intrusion_datetime__gte=start,
                                                    non_human_intrusion_datetime__lt=end, morcha=pk)
        neutralized = models.Intrusion.objects.filter(neutralized_datetime__gte=start,
                                                      neutralized_datetime__lt=end, morcha=pk)
        return verified, non_human, neutralized

    def get_filtered_data_post(self, start, end, pk):
        post = models.Post.objects.get(uuid = pk)
        morchas = post.morcha_set
        print morchas



o = QuerysetProcessors()
o.get_filtered_data_post('s','s', '6b18f78a-f73a-4784-b5af-e9705325e0bf')