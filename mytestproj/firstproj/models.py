from django.db import models

# Create your models here.
class ApiInfo(models.Model):
    REQUEST_TYPE_CHOICE = (
        ('GET', 'GET'),
        ('POST', 'POST'),
    )

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name='接口名称')
    requestType = models.CharField(max_length=50, verbose_name='请求方式', choices=REQUEST_TYPE_CHOICE)
    apiAddress = models.CharField(max_length=1024, verbose_name='接口地址')
    head = models.TextField(blank=True, null=True, verbose_name='头信息')
    data = models.TextField(blank=True, null=True, verbose_name='内容')
    description = models.TextField(max_length=1024, blank=True, null=True, verbose_name='描述')
    createtime = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    creater = models.ForeignKey('auth.User', related_name='createapi', on_delete=models.CASCADE, verbose_name='创建人')


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '接口'
        verbose_name_plural = '接口管理'

class TestCase(models.Model):
    EXAMINE_TYPE_CHOICE =(
    ('assertEqual_func', 'assertEqual'),
    ('assertNotEqual_func', 'assertNotEqual'),
    ('assertIn_func', 'assertIn'),
    ('assertNotIn_func', 'assertNotIn'),
    ('assertRegexpMatches_func', 'assertRegexpMatches'),
)

    id = models.AutoField(primary_key=True)
    casename = models.CharField(max_length=50, verbose_name='用例名称')
    relateapi = models.ForeignKey(ApiInfo,on_delete=models.CASCADE, verbose_name="关联接口", related_name="api_case")
    examineType = models.CharField(default='no_check', max_length=50, verbose_name='校验方式', choices=EXAMINE_TYPE_CHOICE)
    expecthttpCode = models.CharField(max_length=50, blank=True, null=True, verbose_name='HTTP状态')
    expectdata = models.TextField(blank=True, null=True, verbose_name='返回内容')
    createtime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    creater = models.ForeignKey('auth.User', on_delete=models.CASCADE,  verbose_name="创建人",related_name="createcase")



    def __str__(self):
        return self.casename

    class Meta:
        verbose_name = '用例'
        verbose_name_plural = '测试用例管理'

class TestSuite(models.Model):
    id = models.AutoField(primary_key=True)
    suitename = models.CharField(max_length=50,verbose_name='测试套件名')
    description = models.TextField(max_length=1024, blank=True, null=True, verbose_name='描述')
    createtime = models.DateField(auto_now_add=True, verbose_name='创建时间')
    runcount = models.IntegerField(verbose_name='运行次数',default=0)
    runtime = models.DateTimeField(auto_now=True,verbose_name='最后运行时间',null=True)
    suitecase = models.ManyToManyField(TestCase,related_name='case_suite',verbose_name='关联用例',blank=True)
    creater = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name="创建人",related_name="createsuite")

    def __str__(self):
        return self.suitename

    class Meta:
        verbose_name = '测试套件'
        verbose_name_plural = '测试套件管理'


class TestReport(models.Model):
    RESULT_CHOICE =(
    (True, '完成'),
    (False, '失败'),
)


    id = models.AutoField(primary_key=True)
    testsuite = models.ForeignKey(TestSuite,on_delete=models.CASCADE,verbose_name="测试套件", related_name="testsuite_result")
    result = models.BooleanField(verbose_name='测试进度',choices=RESULT_CHOICE)
    reportname = models.CharField(max_length=1024,verbose_name='测试报告名')
    succees_count = models.IntegerField(verbose_name='成功用例数量',null=True)
    succees_case = models.ManyToManyField(TestCase,related_name='succees_case_report',verbose_name='成功用例',blank=True)
    fail_count = models.IntegerField(verbose_name='失败用例数量',null=True)
    fail_case = models.ManyToManyField(TestCase, related_name='fail_case_report', verbose_name='失败用例', blank=True)
    error_count = models.IntegerField(verbose_name='错误用例数量', null=True)
    error_case = models.ManyToManyField(TestCase, related_name='error_case_report', verbose_name='错误用例', blank=True)
    skip_count = models.IntegerField(verbose_name='跳过用例数量', null=True)
    report_data = models.FileField(verbose_name='测试报告文件')
    run_time = models.DateTimeField(auto_now_add=True,verbose_name='测试时间')

    def __str__(self):
        return self.reportname

    class Meta:
        verbose_name = '测试报告'
        verbose_name_plural = '测试报告管理'

