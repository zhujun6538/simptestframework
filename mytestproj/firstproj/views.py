from rest_framework import viewsets
from . import models
from . import serializers
from rest_framework import renderers
from django.contrib.auth.models import User
from rest_framework.response import Response
from django.forms import modelform_factory
from rest_framework.reverse import reverse
from django.shortcuts import redirect
from rest_framework.routers import APIRootView
from rest_framework import permissions
from .permissions import IsOwnerOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from django.forms.widgets import SelectDateWidget
from rest_framework.decorators import action
from .testrunner import runner
import os


class RootView(APIRootView):
    renderer_classes = (renderers.TemplateHTMLRenderer,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request, *args, **kwargs):
        return Response(status=200,template_name='test_framework/index.html')

# Create your views here.
class ApiInfoViewSet(viewsets.ModelViewSet):
    queryset = models.ApiInfo.objects.all()
    serializer_class = serializers.ApiInfoSerializer
    renderer_classes = (renderers.TemplateHTMLRenderer,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('name','requestType')

    def list(self, request, *args, **kwargs):
        api_list = super().list(request=request).data
        apititle = {}
        #获取字段名在前台表格列示
        for field in models.ApiInfo._meta.fields:
            apititle[field.name] = field.verbose_name
        # 创建表单，自定义样式
        ApiForm = modelform_factory(models.ApiInfo,exclude = ('creater',))
        createform = ApiForm()
        #将api的表单对象放入data便于模板使用
        for slz in api_list:
            api = models.ApiInfo.objects.get(id=slz['id'])
            apiform = ApiForm(instance = api)
            slz['apiform']=apiform
        return Response({'apilist':api_list,'apititle':apititle,'createform':createform},status=200,template_name='test_framework/apiinfo.html')

    # 重写视图集create方法
    def create(self, request, *args, **kwargs):
        request.data.url = reverse('apiinfo-list')
        super().create(request=request)
        return redirect('apiinfo-list')

    def perform_create(self, serializer):
        serializer.save(creater=self.request.user)

    # 重写视图集destroy方法
    def destroy(self, request, *args, **kwargs):
        request.data.url = reverse('apiinfo-list')
        super().destroy(request=request)
        return Response(status=200)

    # 重写视图集retrieve方法
    def retrieve(self, request, *args, **kwargs):
        return redirect('apiinfo-list')


    # 重写视图集update方法
    def update(self, request, *args, **kwargs):
        request.data.url = reverse('apiinfo-list')
        super().update(request=request)
        return Response(status=200)

class TestCaseViewSet(viewsets.ModelViewSet):
    """
    此视图自动提供`list`，`create`，`retrieve`，`update`和`destroy`操作。

    另外我们还提供了一个额外的`highlight`操作。
    """
    queryset = models.TestCase.objects.all()
    serializer_class = serializers.TestCaseSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly,)
    renderer_classes = (renderers.TemplateHTMLRenderer,)
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('casename','relateapi')

    def list(self, request, *args, **kwargs):
        case_list = super().list(request=request).data
        casetitle = {}
        #获取字段名在前台表格列示
        for field in models.TestCase._meta.fields:
            casetitle[field.name] = field.verbose_name
        # 创建表单，自定义样式
        CaseForm = modelform_factory(models.TestCase,exclude = ('creater',))
        createform = CaseForm()
        #将api的表单对象放入data便于模板使用
        for slz in case_list:
            case = models.TestCase.objects.get(id=slz['id'])
            caseform = CaseForm(instance = case)
            slz['caseform']=caseform
        return Response({'caselist':case_list,'casetitle':casetitle,'createform':createform},status=200,template_name='test_framework/caseinfo.html')

    # 重写get_queryset方法
    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        # queryset = models.TestCase.objects.all()
        queryset = self.queryset
        suitename = self.request.query_params.get('case_suite', None)
        if suitename is not None:
            suite = models.TestSuite.objects.filter(suitename__contains = suitename)[0]
            queryset = queryset.filter(case_suite = suite)
        return queryset

    # 重写视图集create方法
    def create(self, request, *args, **kwargs):
        request.data.url = reverse('testcase-list')
        super().create(request=request)
        return redirect('testcase-list')

    def perform_create(self, serializer):
        relateapi = models.ApiInfo.objects.get(pk=self.request.data['relateapi'])
        serializer.save(creater=self.request.user,relateapi=relateapi)

    # 重写视图集destroy方法
    def destroy(self, request, *args, **kwargs):
        request.data.url = reverse('testcase-list')
        super().destroy(request=request)
        return Response(status=200)

    # 重写视图集retrieve方法
    def retrieve(self, request, *args, **kwargs):
        return redirect('testcase-list')

    # 重写视图集update方法
    def update(self, request, *args, **kwargs):
        request.data.url = reverse('testcase-list')
        super().update(request=request)
        return Response(status=200)

    def perform_update(self, serializer):
        relateapi = models.ApiInfo.objects.get(pk=self.request.data['relateapi'])
        serializer.save(relateapi=relateapi)

class TestSuiteViewSet(viewsets.ModelViewSet):
    queryset = models.TestSuite.objects.all()
    serializer_class = serializers.TestSuiteSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly,)
    renderer_classes = (renderers.TemplateHTMLRenderer,)
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('suitename','suitecase')


    def list(self, request, *args, **kwargs):
        suite_list = super().list(request=request).data
        suitetitle = {}
        #获取字段名在前台表格列示
        for field in models.TestSuite._meta.fields:
            suitetitle[field.name] = field.verbose_name
        # 创建表单，自定义样式
        SuiteForm = modelform_factory(models.TestSuite,exclude = ('creater',),widgets={"createtime": SelectDateWidget()})
        createform = SuiteForm()
        #将api的表单对象放入data便于模板使用
        for slz in suite_list:
            suite = models.TestSuite.objects.get(id=slz['id'])
            suiteform = SuiteForm(instance = suite)
            slz['suiteform']=suiteform
        return Response({'suitelist':suite_list,'suitetitle':suitetitle,'createform':createform},status=200,template_name='test_framework/suiteinfo.html')

    # 重写视图集create方法
    def create(self, request, *args, **kwargs):
        request.data.url = reverse('testsuite-list')
        super().create(request=request)
        return redirect('testsuite-list')

    def perform_create(self, serializer):
        serializer.save(creater=self.request.user)

    # 重写视图集destroy方法
    def destroy(self, request, *args, **kwargs):
        request.data.url = reverse('testsuite-list')
        super().destroy(request=request)
        return Response(status=200)

    # 重写视图集retrieve方法
    def retrieve(self, request, *args, **kwargs):
        return redirect('testsuite-list')

    # 重写视图集update方法
    def update(self, request, *args, **kwargs):
        request.data.url = reverse('testsuite-list')
        super().update(request=request)
        return Response(status=200)

    # 运行套件
    @action(methods=['post'],detail='testsuite-detail',url_path='run',url_name='testsuite-run')
    def runsuite(self,request, *args, **kwargs):
        # 根据套件获取用例信息
        thissuite = models.TestSuite.objects.get(pk=kwargs['pk'])
        cases = thissuite.suitecase.all()
        suites = []
        for testcase in cases:
            casedict = {}
            caseslz = serializers.TestCaseSerializer(testcase)
            apislz = serializers.ApiInfoSerializer(testcase.relateapi)
            casedict['case'] = caseslz.data
            casedict['api'] = apislz.data
            suites.append(casedict)
        # 运行套件
        result = runner.run_suite(suites,thissuite.suitename)
        print(result.fields)
        casedict = {}
        casedict['succees'] = []
        casedict['fail'] = []
        casedict['error'] = []
        casedict['skip'] = []
        for field in result.fields['testResult']:
            if field['status'] == '成功':casedict['succees'].append(field['description'])
            if field['status'] == '失败':casedict['fail'].append(field['description'])
            if field['status'] == '错误': casedict['error'].append(field['description'])
        succees_case = models.TestCase.objects.filter(casename__in = casedict['succees'])
        fail_case = models.TestCase.objects.filter(casename__in=casedict['fail'])
        error_case = models.TestCase.objects.filter(casename__in=casedict['error'])
        thissuite.runcount += 1
        thissuite.runtime = result.begin_time
        thissuite.save()
        # 记录测试结果
        try:
            thisreport = models.TestReport.objects.create(testsuite=thissuite,
                                             result=result.wasSuccessful(),
                                             reportname = result.title,
                                             succees_count=result.success_count,
                                             fail_count=result.failure_count,
                                             error_count=result.error_count,
                                             skip_count=result.skipped,
                                             report_data=os.path.join(result.report_dir,result.filename),
                                             run_time=result.begin_time)
            thisreport.succees_case.set(succees_case)
            thisreport.fail_case.set(fail_case)
            thisreport.error_case.set(error_case)
        except Exception as e:
            print(e)
        return redirect('testsuite-list')


class TestReportViewSet(viewsets.ModelViewSet):
    queryset = models.TestReport.objects.all()
    serializer_class = serializers.TestReportSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    renderer_classes = (renderers.TemplateHTMLRenderer,)
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('testsuite','result')

    def list(self, request, *args, **kwargs):
        report_list = super().list(request=request).data
        reporttitle = {}
        #获取字段名在前台表格列示
        for field in models.TestReport._meta.fields:
            reporttitle[field.name] = field.verbose_name
        # 创建表单，自定义样式
        ReportForm = modelform_factory(models.TestReport,fields = ('__all__'),widgets={"run_time": SelectDateWidget()})
        createform = ReportForm()
        #将api的表单对象放入data便于模板使用
        for slz in report_list:
            report = models.TestReport.objects.get(id=slz['id'])
            reportform = ReportForm(instance = report)
            slz['reportform']=reportform
        return Response({'reportlist':report_list,'reporttitle':reporttitle,'createform':createform},status=200,template_name='test_framework/reportinfo.html')

    # 重写视图集destroy方法
    def destroy(self, request, *args, **kwargs):
        request.data.url = reverse('testreport-list')
        super().destroy(request=request)
        return Response(status=200)

    # 重写视图集retrieve方法
    def retrieve(self, request, *args, **kwargs):
        return redirect('testreport-list')

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    此视图自动提供`list`和`detail`操作。
    """
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    renderer_classes = (renderers.TemplateHTMLRenderer,)
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('')

    def list(self, request, *args, **kwargs):
        user_list = super().list(request=request).data
        usertitle = {}
        #获取字段名在前台表格列示
        for field in User._meta.fields:
            usertitle[field.name] = field.verbose_name
        # 创建表单，自定义样式
        UserForm = modelform_factory(User,fields=('id', 'username'))
        createform = UserForm()
        #将api的表单对象放入data便于模板使用
        for slz in user_list:
            user = User.objects.get(id=slz['id'])
            userform = UserForm(instance = user)
            slz['userform']=userform
        return Response({'userlist':user_list,'usertitle':usertitle,'createform':createform},status=200,template_name='test_framework/userinfo.html')
