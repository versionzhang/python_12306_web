import os
import signal

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from webadmin.models import BuyTasks
import psutil
from psutil import NoSuchProcess

from .serializers import BuyTasksSerializers
from .utils import TasksManagerUtil

class HomepageView(TemplateView):
    template_name = "homepage.html"

    def get_context_data(self, **kwargs):
        return {"test": '{\n  "origin": "172.96.239.57, 172.96.239.57"\n}\n'}

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class BuyTaskViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = BuyTasksSerializers
    queryset = BuyTasks.objects.all()

    @action(methods=["post"], detail=True, url_name="run-tasks")
    def run_tasks(self, request, pk):
        instance = self.get_object()
        if instance.status == "pending":
            util = TasksManagerUtil(instance)
            p = util.run()
            instance.pid = p.pid
            instance.status = 'running'
            instance.save()
            return Response({"status": 0, "msg": "程序运行成功"})
        return Response({"status": -1, "msg": "程序当前已经处于运行状态"})

    @action(methods=["post"], detail=True, url_name="run-tasks")
    def stop_tasks(self, request, pk):
        instance = self.get_object()
        if instance.status == "running":
            try:
                p = psutil.Process(instance.pid)
                os.killpg(instance.pid, signal.SIGTERM)
                instance.pid = None
                instance.status = "pending"
                instance.save()
                return Response({"status": 0, "msg": "停止任务成功"})
            except NoSuchProcess:
                return Response({"status": 0, "msg": "任务已经停止, 无需重新停止"})
        return Response({"status": -1, "msg": "任务现在不在运行状态"})

    @action(methods=["get"], detail=True, url_name="tasks-logs")
    def tasks_logs(self, request, pk):
        instance = self.get_object()
        if instance.status == "running":
            util = TasksManagerUtil(instance)
            status, msg = util.get_task_status()
            if msg:
                return Response({"status": status, "msg": msg})
            if status == -2:
                return Response({"status": status, "msg": "任务已完成,或者任务失败,重新刷新页面"})
        return Response({"status": -1, "msg": "当前任务未运行"})


