import os
import platform
import subprocess

from slugify import slugify
from rest_framework.renderers import JSONRenderer

import json, yaml

from webadmin.serializers import TotalConfigSerializers


class TasksManagerUtil(object):
    def __init__(self, task_obj):
        self.task_obj = task_obj

    @property
    def generator_folder_name(self):
        return '{name}_{task_id}'.format(
            name=slugify(self.task_obj.name, ok='_', only_ascii=True), task_id=self.task_obj.id)

    def generator_folder(self):
        try:
            os.mkdir(self.generator_folder_name)
        except FileExistsError:
            pass

    @property
    def log_file_path(self):
        return os.path.join(
            os.path.join(os.path.abspath(os.getcwd()), self.generator_folder_name),
            'tasks.log')

    def write_to_config_file(self):
        t = self.task_obj.config
        s = JSONRenderer().render(TotalConfigSerializers(t).data)
        config_string = yaml.dump(json.loads(s)).encode().decode("unicode_escape")
        with open(os.path.join(self.generator_folder_name, "config.yaml"), "w") as f:
            f.write(config_string)

    def run(self):
        self.generator_folder()
        self.write_to_config_file()
        kwargs = {}
        if platform.system() == 'Windows':
            # from msdn [1]
            CREATE_NEW_PROCESS_GROUP = 0x00000200  # note: could get it from subprocess
            DETACHED_PROCESS = 0x00000008  # 0x8 | 0x200 == 0x208
            kwargs.update(creationflags=DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP)
        else:  # Python 3.5+ and Unix
            kwargs.update(start_new_session=True)

        if self.task_obj.proxy:
            return subprocess.Popen("export https_proxy={proxy_url} && cd {folder_name} && py12306".format(
                proxy_url=self.task_obj.proxy.proxy_url,
                folder_name=self.generator_folder_name
            ), shell=True, stdout=open(self.log_file_path, "w"), **kwargs)
        else:
            return subprocess.Popen("cd {folder_name} && py12306".format(
                folder_name=self.generator_folder_name
            ), shell=True, stdout=open(self.log_file_path, "w"), **kwargs)

    def get_task_status(self):
        process = subprocess.Popen(['tail', '-n', '20', self.log_file_path], stdout=subprocess.PIPE)
        stdout = process.communicate()[0]
        if stdout:
            return stdout.decode("utf-8")
        else:
            return ""
