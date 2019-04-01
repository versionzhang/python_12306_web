from django.db import models
from django_better_admin_arrayfield.models.fields import ArrayField


class PresaleConfig(models.Model):
    name = models.CharField(verbose_name="预售模式配置名称", max_length=30)
    travel_date = models.DateField()
    query_left_ticket_time= models.PositiveSmallIntegerField(
        "预售模式下查询余票时间间隔 单位秒", default=5)
    stop_time = models.PositiveSmallIntegerField(
        "预售模式下提前多久停止正常模式的查询只查询预售模式的日期的票, 单位分钟", default=5)
    # 预售模式下提前多久停止正常模式的查询只查询预售模式的日期的票, 单位分钟
    continue_time = models.PositiveSmallIntegerField(
        "预售模式下持续时间,过了持续时间之后,变为正常查询,按照正常查询的模式, 单位分钟", default=5)
    start_times = ArrayField(models.CharField(max_length=30),
                             verbose_name="预售时间点, 可以为多个, 格式如下所示,%H:%M 小时:分钟")


class BasicConfig(models.Model):
    name = models.CharField(verbose_name="基本配置名称", max_length=30)
    fast_submit = models.BooleanField("快速下单接口, True or False", default=False)
    debug = models.BooleanField("调试模式, True or False", default=True)
    travel_dates = ArrayField(models.TimeField(), verbose_name="出发日期(list)，格式: 2018-01-06, 按照优先级排列")
    ticket_type = models.CharField(verbose_name="票种, 目前取值有两种, 成人票或者学生票",
                                   choices=[("成人票", "成人票"), ("学生票", "学生票")],
                                   default="成人票", max_length=30)
    manual_trainnum_enable = models.BooleanField(verbose_name="manual_trainnum_enable, 是否根据时间范围 和 乘车类型 购票, 否则将需要手动填写车次")
    train_types = ArrayField(models.CharField(choices=
            [("G", "G"), ("D", "D"), ("K", "K"), ("T", "T"), ("C", "C"),
             ("Z", "Z"), ("L", "L"), ("S", "S")], max_length=30),
                             verbose_name="列车类型: 高铁 G 动车 D 普快K, 特快T, C城际 Z 直达 L 临客 普通纯数字车次 "
                                          "用S代替, manual_trainnum_enable 选项为 False时有效")
    earliest_time = models.TimeField(verbose_name='可接受最早出发时间 格式ex："00:00" 24小时格式, manual_trainnum_enable 选项为 False时有效')
    latest_time = models.TimeField(verbose_name="可接受最晚抵达时间, manual_trainnum_enable 选项为 False时有效")
    train_list = ArrayField(models.CharField(max_length=30), verbose_name="过滤车次(list)，manual_trainnum_enable选项为True时启用")

    use_station_group = models.BooleanField("是否使用站点组")
    from_stations = ArrayField(models.CharField(max_length=30), verbose_name="出发城市列表，比如深圳北，就填深圳就搜得到")
    to_stations = ArrayField(models.CharField(max_length=30), verbose_name="到达城市列表, 比如深圳北，就填深圳就搜得到")
    station_groups = ArrayField(ArrayField(models.CharField(max_length=30), size=2), verbose_name="出发到达城市组")
    ticket_types = ArrayField(models.CharField(max_length=30), verbose_name="座位(list) 多个座位, 可选列表有: 商务特等座, 一等座, 二等座, 硬座, 软座, 无座, 高级软卧, 软卧, 硬卧, 动卧")
    ticket_people_list = ArrayField(models.CharField(max_length=30),
                                    verbose_name="乘车人(list) 多个乘车人")

    query_left_ticket_time = models.SmallIntegerField("查询余票时间间隔, 单位秒", default=5)
    retry_login_time = models.SmallIntegerField("重试登录次数", default=3)
    black_train_time = models.SmallIntegerField("加入小黑屋时间，此功能为了防止僵尸票导致一直下单不成功错过正常的票, 单位为分钟", default=3)

