from rest_framework.response import Response
from rest_framework import viewsets
import models, serializers
import datetime
import calendar_utils
from widget_processors import Widgets


class BattalionView(viewsets.ReadOnlyModelViewSet):
    queryset = models.Battalion.objects.all()
    serializer_class = serializers.BattalionSerializer


class PostView(viewsets.ReadOnlyModelViewSet):
    queryset = models.Post.objects.all()
    serializer_class = serializers.PostMorchaSerializer


class MorchaView(viewsets.ReadOnlyModelViewSet):
    queryset = models.Morcha.objects.all()
    serializer_class = serializers.MorchaSerializer


class MorchaDayView(viewsets.ViewSet):
    def retrieve(self, request, pk=None, date=None):
        self.widgets = Widgets(date=date, timespan='day', pk=pk, level='morcha')
        return Response({
            'count': self.widgets.total_count(),
            'intrusions': self.widgets.get_intrusion_report(),
            'area_secure': self.widgets.get_security_update()
        })


class MorchaWeekView(viewsets.ViewSet):
    def retrieve(self, request, pk=None, date=None):
        self.widgets = Widgets(date=date, timespan='week', pk=pk, level='morcha')
        return Response({
            'longest_intrusion': self.widgets.longest_intrusion(),
            'count': self.widgets.total_count(),
            'report': self.widgets.get_intrusion_report()
        })


class MorchaMonthView(viewsets.ViewSet):
    def retrieve(self, request, pk=None, date=None):
        self.widgets = Widgets(date=date, timespan='month', pk=pk, level='morcha')
        return Response({
            'longest_intrusion': self.widgets.longest_intrusion(),
            'count': self.widgets.total_count(),
            'report': self.widgets.get_intrusion_report(),
        })


class PostDayView(viewsets.ViewSet):
    def retrieve(self, request, pk=None, date=None):
        self.widgets = Widgets(date=date, timespan='day', pk=pk, level='post')
        return Response({
            'report': self.widgets.get_intrusion_report()
        })


class PostWeekView(viewsets.ViewSet):
    def retrieve(self, request, pk=None, date=None):
        self.widgets = Widgets(date=date, timespan='week', level='post', pk=pk)
        return Response({
            'count': self.widgets.total_count(),
            'longest': self.widgets.longest_intrusion(),
            'vulnerable': self.widgets.get_vulnerable_morcha(),
            'report': self.widgets.get_intrusion_report()
        })


class PostMonthView(viewsets.ViewSet):
    def retrieve(self, request, pk=None, date=None):
        self.widgets = Widgets(date=date, timespan='month', level='post', pk=pk)
        return Response({
            'count': self.widgets.total_count(),
            'longest': self.widgets.longest_intrusion(),
            'vulnerable': self.widgets.get_vulnerable_morcha(),
            'report': self.widgets.get_intrusion_report()
        })


class PostRecentView(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        self.widgets = Widgets(timespan='recent', level='post', pk=pk)
        return Response({
            'recent': self.widgets.get_intrusion_report(),
            'vulnerable': self.widgets.get_vulnerable_morcha(),
            'hour': self.widgets.get_hypersensitive_hour()
        })


class BattalionRecentView(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        self.widgets = Widgets(timespan='recent', level='battalion', pk=pk)
        return Response({
            'vulnerable': self.widgets.get_vulnerable_post(),
            'recent': self.widgets.get_intrusion_report()
        })


class BattalionWeekView(viewsets.ViewSet):
    def retrieve(self, request, pk=None, date=None):
        self.widgets = Widgets(date=date, timespan='week', level='battalion', pk=pk)
        return Response({
            'count': self.widgets.total_count(),
            'longest': self.widgets.longest_intrusion(),
            'vulnerable': self.widgets.get_vulnerable_post(),
            'report': self.widgets.get_intrusion_report()
        })


class BattalionMonthView(viewsets.ViewSet):
    def retrieve(self, request, pk=None, date=None):
        self.widgets = Widgets(date=date, timespan='month', level='battalion', pk=pk)
        return Response({
            'count': self.widgets.total_count(),
            'longest': self.widgets.longest_intrusion(),
            'vulnerable': self.widgets.get_vulnerable_post(),
            'report': self.widgets.get_intrusion_report()
        })


class BattalionDashboardView(viewsets.ViewSet):
    def retrieve(self, request):
        self.calendar = calendar_utils.calendar_iterators()
        start, end = self.calendar.lastmonthstartend()
        battalions = models.Battalion.objects.all()
        obj = {}
        for battalion in battalions:
            data = {}
            data['battalion_name'] = battalion.name
            posts = battalion.posts.all()
            data['post_count'] = posts.count()
            morcha_count = 0
            for post in posts:
                morcha_count += post.morchas.count()
            data['morcha_count'] = morcha_count
            pk = battalion.uuid
            data['intrusions'] = models.Intrusion.objects.filter(morcha__post__battalion = pk).count()
            obj[str(pk)] = data
        return Response(obj)



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

def test(request):
    return Response("nothing :P !!")
