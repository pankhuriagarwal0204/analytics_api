from django.db.models import Q
from rest_framework.response import Response
from rest_framework import viewsets
from django.db.models import Sum, Count
from django.db.models.functions import ExtractHour
import models, serializers
import datetime, pytz
import calendar_utils


def get_daystart_time(_date=datetime.date.today()):
    today_beginning = datetime.datetime.combine(_date, datetime.time())
    return today_beginning


def get_filtered_data(start, end, pk):
    verified = models.Intrusion.objects.filter(verified_datetime__gte=start, verified_datetime__lt=end, morcha=pk)
    non_human = models.Intrusion.objects.filter(non_human_intrusion_datetime__gte=start,
                                                non_human_intrusion_datetime__lt=end, morcha=pk)
    neutralized = models.Intrusion.objects.filter(neutralized_datetime__gte=start,
                                                  neutralized_datetime__lt=end, morcha=pk)
    return verified, non_human, neutralized


def get_filtered_data_post(start, end, pk):
    print end
    verified = models.Intrusion.objects.filter(verified_datetime__gte=start, verified_datetime__lt=end, post=pk)
    non_human = models.Intrusion.objects.filter(non_human_intrusion_datetime__gte=start,
                                                non_human_intrusion_datetime__lt=end, post=pk)
    neutralized = models.Intrusion.objects.filter(neutralized_datetime__gte=start,
                                                  neutralized_datetime__lt=end, post=pk)
    detected = models.Intrusion.objects.filter(detected_datetime__gte=start, detected_datetime__lt=end, post=pk)
    return verified, non_human, neutralized, detected


def get_count(verified, non_human, neutralized):
    verified_count = len(verified)
    non_human_count = len(non_human)
    neutralized_count = len(neutralized)
    obj = {
        'verified': verified_count,
        'neutralized': neutralized_count,
        'non_human': non_human_count,
    }
    return obj


def get_longest_intrusion(data, start):
    filtered_by_detected_time = data.filter(detected_datetime__gte=start)
    longest = filtered_by_detected_time.order_by('-duration')[0]
    return serializers.LongestIntrusionSerializer(longest).data


def get_vulnerable_morcha(data):
    vulnerable = data.values('morcha__name', 'morcha__uuid').annotate(count=Count('morcha'))
    return vulnerable


def get_dangling_intrusion(end, pk):
    end = end - datetime.timedelta(days=1)
    monthdelta = datetime.timedelta(days=30)
    start = end - monthdelta
    verified = models.Intrusion.objects.filter(verified_datetime__gte=start,
                                               verified_datetime__lt=end, morcha=pk). \
        filter(neutralized_datetime__isnull=True)
    return verified


def get_area_secure_status(old, verified, end):
    old_data_status = False if old.count() > 0 else True
    verified_filtered_data = verified.filter(Q(neutralized_datetime__isnull=True) | Q(neutralized_datetime__gt=end))
    current_data_status = False if verified_filtered_data.count() > 0 else True
    print "old", old_data_status
    print "today", current_data_status
    return True if old_data_status and current_data_status else False


def get_report_by_day(start, end, pk):
    data = {}
    verified, non_human, neutralized = get_filtered_data(start, end, pk)

    while True:
        dayend = start + datetime.timedelta(days=1)
        verified_data = verified.filter(verified_datetime__gte=start, verified_datetime__lt=dayend)
        verified_count = verified_data.count()
        non_human_count = non_human.filter(non_human_intrusion_datetime__gte=start,
                                           non_human_intrusion_datetime__lt=dayend).count()
        neutralized_count = neutralized.filter(neutralized_datetime__gte=start,
                                               neutralized_datetime__lt=dayend).count()
        old = get_dangling_intrusion(dayend, pk)
        area_secure = get_area_secure_status(old=old, verified=verified_data, end=dayend)

        obj = {
            'verified_count': verified_count,
            'non_human_count': non_human_count,
            'neutralized_count': neutralized_count,
            'area_secure': area_secure
        }
        data[str(start)] = obj
        start = dayend
        if start == end:
            break
        else:
            pass
    return data


def get_report_by_day_post(start, end, pk):
    data = {}
    verified, non_human, neutralized, detected = get_filtered_data_post(start, end, pk)

    while True:
        dayend = start + datetime.timedelta(days=1)
        verified_data = verified.filter(verified_datetime__gte=start, verified_datetime__lt=dayend)
        verified_count = verified_data.count()
        non_human_count = non_human.filter(non_human_intrusion_datetime__gte=start,
                                           non_human_intrusion_datetime__lt=dayend).count()
        neutralized_count = neutralized.filter(neutralized_datetime__gte=start,
                                               neutralized_datetime__lt=dayend).count()
        obj = {
            'verified_count': verified_count,
            'non_human_count': non_human_count,
            'neutralized_count': neutralized_count
        }
        data[str(start)] = obj
        start = dayend
        if start == end:
            break
        else:
            pass
    return data


def group_report_by_week(start, end, pk):
    data = {}
    verified, non_human, neutralized = get_filtered_data(start, end, pk)

    while True:
        if start == end or start > end:
            break
        elif start + datetime.timedelta(days=7) > end:
            weekend = end
        else:
            weekend = start + datetime.timedelta(days=7)

        verified_count = verified.filter(verified_datetime__gte=start, verified_datetime__lt=weekend).count()
        non_human_count = non_human.filter(non_human_intrusion_datetime__gte=start,
                                           non_human_intrusion_datetime__lt=weekend).count()
        neutralized_count = neutralized.filter(neutralized_datetime__gte=start,
                                               neutralized_datetime__lt=weekend).count()
        obj = {
            'verified_count': verified_count,
            'non_human_count': non_human_count,
            'neutralized_count': neutralized_count,
        }
        data[str(start)] = obj
        start += datetime.timedelta(days=7)
    return data


def get_report_by_week_post(start, end, pk):
    data = {}
    verified, non_human, neutralized, detected = get_filtered_data_post(start, end, pk)
    while True:
        if start == end or start > end:
            break
        elif start + datetime.timedelta(days=7) > end:
            weekend = end
        else:
            weekend = start + datetime.timedelta(days=7)

        verified_count = verified.filter(verified_datetime__gte=start, verified_datetime__lt=weekend).count()
        non_human_count = non_human.filter(non_human_intrusion_datetime__gte=start,
                                           non_human_intrusion_datetime__lt=weekend).count()
        neutralized_count = neutralized.filter(neutralized_datetime__gte=start,
                                               neutralized_datetime__lt=weekend).count()
        obj = {
            'verified_count': verified_count,
            'non_human_count': non_human_count,
            'neutralized_count': neutralized_count,
        }
        data[str(start)] = obj
        start += datetime.timedelta(days=7)
    return data


class PostView(viewsets.ReadOnlyModelViewSet):
    queryset = models.Post.objects.all()
    serializer_class = serializers.PostSerializer


class MorchaView(viewsets.ReadOnlyModelViewSet):
    queryset = models.Morcha.objects.all()
    serializer_class = serializers.MorchaSerializer


class MorchaDayView(viewsets.ViewSet):
    def __init__(self):
        self.obj = calendar_utils.calendar_iterators()

    def retrieve(self, request, pk=None, date=None):
        start, end = self.obj.daystartend(date)
        verified, non_human, neutralized = get_filtered_data(start, end, pk)
        count = get_count(verified, non_human, neutralized)
        old = get_dangling_intrusion(end, pk)
        today = verified | non_human | neutralized
        today_intrusions = serializers.IntrusionSerializer(today, many=True)
        old_intrusions = serializers.IntrusionSerializer(old, many=True)
        area_secure = get_area_secure_status(old, verified, end)
        return Response({
            'count': count,
            'intrusions': today_intrusions.data + old_intrusions.data,
            'area_secure': area_secure
        })


class MorchaWeekView(viewsets.ViewSet):
    def __init__(self):
        self.obj = calendar_utils.calendar_iterators()

    def retrieve(self, request, pk=None, date=None):
        start, end = self.obj.weekstartend(date)
        verified, non_human, neutralized = get_filtered_data(start, end, pk)
        count = get_count(verified, non_human, neutralized)
        week = verified | non_human | neutralized
        longest = get_longest_intrusion(week, start)
        report = get_report_by_day(start, end, pk)
        return Response({
            'longest_intrusion': longest,
            'count': count,
            'report': report,
        })


class MorchaMonthView(viewsets.ViewSet):
    def __init__(self):
        self.obj = calendar_utils.calendar_iterators()

    def retrieve(self, request, pk=None, date=None):
        start, end = self.obj.monthstartend(date)
        verified, non_human, neutralized = get_filtered_data(start, end, pk)
        count = get_count(verified, non_human, neutralized)
        month = verified | non_human | neutralized
        longest = get_longest_intrusion(month, start)
        report = group_report_by_week(start, end, pk)
        return Response({
            'longest_intrusion': longest,
            'count': count,
            'report': report,
        })


class PostDayView(viewsets.ViewSet):
    def __init__(self):
        self.obj = calendar_utils.calendar_iterators()

    def retrieve(self, request, pk=None, date=None):
        start, end = self.obj.daystartend(date)
        verified, non_human, neutralized, detected = get_filtered_data_post(start, end, pk)
        today = verified | non_human | neutralized
        qs = today.values('morcha').annotate(verified=Count('verified_datetime'),
                                             non_human=Count('non_human_intrusion_datetime'),
                                             neutralized=Count('neutralized_datetime'))

        for i in qs:
            morcha = i['morcha']
            verified_by_morcha = verified.filter(morcha=morcha)
            old = get_dangling_intrusion(end, morcha)
            area_secure = get_area_secure_status(old=old, verified=verified_by_morcha, end=end)
            i['area_secure'] = area_secure

        return Response({
            'data': qs
        })


class PostWeekView(viewsets.ViewSet):
    def __init__(self):
        self.obj = calendar_utils.calendar_iterators()

    def retrieve(self, request, pk=None, date=None):
        start, end = self.obj.weekstartend(date)
        verified, non_human, neutralized, detected = get_filtered_data_post(start, end, pk)
        today = verified | non_human | neutralized
        count = get_count(verified=verified, non_human=non_human, neutralized=neutralized)
        longest = get_longest_intrusion(today, start)
        vulnerable = get_vulnerable_morcha(detected)
        report = get_report_by_day_post(start, end, pk)

        return Response({
            'count': count,
            'longest': longest,
            'vulnerable': vulnerable,
            'report': report
        })


class PostMonthView(viewsets.ViewSet):
    def __init__(self):
        self.obj = calendar_utils.calendar_iterators()

    def retrieve(self, request, pk=None, date=None):
        start, end = self.obj.monthstartend(date)
        verified, non_human, neutralized, detected = get_filtered_data_post(start, end, pk)
        today = verified | non_human | neutralized
        count = get_count(verified=verified, non_human=non_human, neutralized=neutralized)
        longest = get_longest_intrusion(today, start)
        vulnerable = get_vulnerable_morcha(detected)
        report = get_report_by_week_post(start, end, pk)

        return Response({
            'count': count,
            'longest': longest,
            'vulnerable': vulnerable,
            'report': report
        })


class PostRecentView(viewsets.ViewSet):
    def __init__(self):
        self.obj = calendar_utils.calendar_iterators()

    def retrieve(self, request, pk=None, date=None):
        start, end = self.obj.lastmonthstartend(date)
        verified, non_human, neutralized, detected = get_filtered_data_post(start, end, pk)
        today = verified | non_human | neutralized
        vulnerable = get_vulnerable_morcha(detected)
        recent = today.order_by('-detected_datetime')[:8]
        hour = today.annotate(hour=ExtractHour('detected_datetime', tzinfo=pytz.UTC)).values('hour').annotate(
            count=Count('id'))
        serializer = serializers.IntrusionSerializer(recent, many=True)
        return Response({
            'recent': serializer.data,
            'vulnerable': vulnerable,
            'hour': hour
        })


def insert(request):
    morcha_instance = models.Morcha.objects.get(name='morcha3')
    post_instance = models.Post.objects.get(name=morcha_instance.post)
    print post_instance
    obj = calendar_utils.calendar_iterators()
    counter = 1
    # date = datetime.datetime(2017, 1, 2).replace(tzinfo=pytz.UTC)
    for date in obj.lastmonthiterator('2017-02-01'):
        print date.tzinfo
        data = models.Intrusion()
        data.morcha = morcha_instance
        data.post = post_instance
        data.detected_datetime = date
        newdate = date + datetime.timedelta(hours=2, minutes=10)
        data.verified_datetime = newdate

        if (counter < 6):
            data.non_human_intrusion_datetime = newdate

        if (counter == 10 or counter == 15):
            data.neutralized_datetime = newdate + datetime.timedelta(days=1)
        elif (counter == 11):
            pass
        else:
            data.neutralized_datetime = newdate + datetime.timedelta(hours=2, minutes=10)
        data.duration = 2000.0
        data.save()
        counter += 1
