from django.db import models
from django_better_admin_arrayfield.models.fields import ArrayField


class BaseModel(models.Model):
    c_time = models.DateTimeField(auto_now_add=True)
    m_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class PresaleConfig(BaseModel):
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

    def __str__(self):
        return '预售模式配置: {}'.format(self.name)

    class Meta:
        verbose_name = "预售模式配置"

class BasicConfig(BaseModel):
    name = models.CharField(verbose_name="基本配置名称", max_length=30)
    fast_submit = models.BooleanField("快速下单接口, True or False", default=False)
    debug = models.BooleanField("调试模式, True or False", default=True)
    travel_dates = ArrayField(models.CharField(max_length=30), verbose_name="出发日期(list)，格式: 2018-01-06, 按照优先级排列")
    ticket_type = models.CharField(verbose_name="票种, 目前取值有两种, 成人票或者学生票",
                                   choices=[("成人票", "成人票"), ("学生票", "学生票")],
                                   default="成人票", max_length=30)
    manual_trainnum_enable = models.BooleanField(verbose_name="manual_trainnum_enable, 是否根据时间范围 和 乘车类型 购票, 否则将需要手动填写车次")
    train_types = ArrayField(models.CharField(choices=
            [("G", "G"), ("D", "D"), ("K", "K"), ("T", "T"), ("C", "C"),
             ("Z", "Z"), ("L", "L"), ("S", "S")], max_length=30),
                             verbose_name="列车类型: 高铁 G 动车 D 普快K, 特快T, C城际 Z 直达 L 临客 普通纯数字车次 "
                                          "用S代替, manual_trainnum_enable 选项为 False时有效")
    earliest_time = models.CharField(verbose_name='可接受最早出发时间 格式ex："00:00" 24小时格式, manual_trainnum_enable 选项为 False时有效',
                                     max_length=30, default='06:00')
    latest_time = models.CharField(verbose_name="可接受最晚抵达时间, manual_trainnum_enable 选项为 False时有效",
                                   max_length=30, default='23:00')
    train_list = ArrayField(models.CharField(max_length=30), verbose_name="过滤车次(list)，manual_trainnum_enable选项为True时启用")

    use_station_group = models.BooleanField("是否使用站点组", default=True)
    from_stations = ArrayField(models.CharField(max_length=30), verbose_name="出发城市列表，比如深圳北，就填深圳就搜得到")
    to_stations = ArrayField(models.CharField(max_length=30), verbose_name="到达城市列表, 比如深圳北，就填深圳就搜得到")
    station_groups = ArrayField(models.CharField(max_length=30),
        verbose_name="出发到达城市组,格式为 深圳,广州 为一组,表示从深圳到广州")
    ticket_types = ArrayField(models.CharField(max_length=30), verbose_name="座位(list) 多个座位, 可选列表有: 商务特等座, 一等座, 二等座, 硬座, 软座, 无座, 高级软卧, 软卧, 硬卧, 动卧")
    ticket_people_list = ArrayField(models.CharField(max_length=30),
                                    verbose_name="乘车人(list) 多个乘车人")

    query_left_ticket_time = models.SmallIntegerField("查询余票时间间隔, 单位秒", default=5)
    retry_login_time = models.SmallIntegerField("重试登录次数", default=3)
    black_train_time = models.SmallIntegerField("加入小黑屋时间，此功能为了防止僵尸票导致一直下单不成功错过正常的票, 单位为分钟", default=3)

    def __str__(self):
        return '基本模式配置: {}'.format(self.name)

    class Meta:
        verbose_name = "基本模式配置"


class TrainAccount(BaseModel):
    name = models.CharField(verbose_name="配置备注", max_length=30)
    user = models.CharField(verbose_name="用户名", max_length=50)
    pwd = models.CharField(verbose_name="密码", max_length=30)

    def __str__(self):
        return '账户配置: {}'.format(self.name)

    class Meta:
        verbose_name = "12306账户配置"

class AutoCodeAccount(BaseModel):
    name = models.CharField(verbose_name="配置备注", max_length=30)
    user = models.CharField(verbose_name="用户名", max_length=50)
    pwd = models.CharField(verbose_name="密码", max_length=30)

    def __str__(self):
        return '打码平台用户名密码配置: {}'.format(self.name)

    class Meta:
        verbose_name = "打码平台用户名密码配置"


class EmailConfig(BaseModel):
    name = models.CharField(verbose_name="基本配置名称", max_length=30)
    from_email = models.EmailField(verbose_name="发件人邮箱")
    notice_email_list = ArrayField(models.EmailField(), verbose_name="收件人邮箱列表")
    username = models.CharField(verbose_name="用户名(发送邮件的邮箱用户名)", max_length=50)
    password = models.CharField(verbose_name="密码(发送邮件的邮箱密码)", max_length=200)
    email_gateway = models.CharField(verbose_name="邮件网关", max_length=200)
    email_port = models.PositiveIntegerField(verbose_name="邮件网关端口")

    def __str__(self):
        return '邮箱配置: {}'.format(self.name)

    class Meta:
        verbose_name = "邮箱配置"

class ProxyConfig(BaseModel):
    name = models.CharField(verbose_name="代理配置名称", max_length=30)
    proxy_url = models.CharField(
        verbose_name="代理url, scheme://user:passwd@ip:port, ex: http://aaa:bbb@127.0.0.1:1234 或者不加用户名密码http://127.0.0.1:1234",
    max_length = 30)

    def __str__(self):
        return '代理配置: {}'.format(self.name)

    class Meta:
        verbose_name = "代理配置"

class TotalConfig(BaseModel):
    name = models.CharField(verbose_name="总配置文件备注", max_length=30)
    presale_enable = models.BooleanField(verbose_name="预售模式: 预售模式为抢票模式, 在抢票模式下的查询时间间隔可以配置的低一点",
                                         default=False)
    presale_config = models.ForeignKey(PresaleConfig, blank=True, null=True, on_delete=models.SET_NULL)

    basic_config = models.ForeignKey(BasicConfig, on_delete=models.CASCADE)
    train_account = models.ForeignKey(TrainAccount, on_delete=models.CASCADE)
    auto_code_enable = models.BooleanField(verbose_name="是否启用自动打码", default=True)
    auto_code_method = models.CharField(verbose_name="自动打码方式",
                                        max_length=30,
                                        choices=[("freeapi", "免费打码"), ("ruokuai", "若快")])
    auto_code_account = models.ForeignKey(AutoCodeAccount, blank=True, null=True, on_delete=models.SET_NULL)
    email_notice_enable = models.BooleanField(verbose_name="是否开启邮件通知",
                                              default=False)
    email_config = models.ForeignKey(EmailConfig, blank=True, null=True, on_delete=models.SET_NULL)

    cdn_enable = models.BooleanField(verbose_name="是否开启cdn", default=False)
    multi_threading_enable = models.BooleanField(verbose_name="是否开启多线程", default=False)

    online_check_time = models.PositiveIntegerField(verbose_name="在线检测时间, 单位秒, 启用自动打码有效", default=60)

    save_img_enable = models.BooleanField(verbose_name="手动打码识别时候是否保存图片到本地进行识别", default=True)
    weixin_notice_enable = models.BooleanField(verbose_name="是否开启微信通知, 使用server酱服务", default=False)
    weixin_sckey = models.CharField(verbose_name="微信通知key", blank=True, null=True, max_length=300)

    def __str__(self):
        return '总配置: {}'.format(self.name)

    class Meta:
        verbose_name = "总配置"

class BuyTasks(BaseModel):
    name = models.CharField(verbose_name="购票任务名称", max_length=30, unique=True)
    proxy = models.ForeignKey(ProxyConfig, blank=True, null=True, on_delete=models.SET_NULL)
    config = models.ForeignKey(TotalConfig, on_delete=models.CASCADE)
    status = models.CharField(verbose_name="任务状态", max_length=40,
                              choices=[
                                  ("pending", "未运行"),
                                  ("running", "运行中")
                              ])
    pid = models.PositiveIntegerField(verbose_name="pid,进程号", blank=True, null=True)

    def __str__(self):
        return '购买任务配置: {}'.format(self.name)

    class Meta:
        verbose_name = "购买任务配置"
