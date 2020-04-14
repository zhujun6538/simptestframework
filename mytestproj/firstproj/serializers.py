from rest_framework import serializers
from . import models
from django.contrib.auth.models import User


class ApiInfoSerializer(serializers.ModelSerializer):
    creater = serializers.ReadOnlyField(source='creater.username')

    class Meta:
        model = models.ApiInfo
        fields = []
        for field in model._meta.fields:
            fields.append(field.name)
        # fields = ('id', 'name', 'requestType', 'apiAddress', 'head', 'data', 'description', 'createtime', 'creater')

class TestCaseSerializer(serializers.ModelSerializer):
    creater = serializers.ReadOnlyField(source='creater.username')
    relateapi = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = models.TestCase
        fields = []
        for field in model._meta.fields:
            fields.append(field.name)
        # fields = ('id', 'casename', 'relateapi', 'examineType', 'expecthttpCode', 'expectdata', 'createtime', 'creater')

class TestSuiteSerializer(serializers.ModelSerializer):
    creater = serializers.ReadOnlyField(source='creater.username')

    class Meta:
        model = models.TestSuite
        # fields = []
        # for field in model._meta.fields:
        #     fields.append(field.name)
        fields = ('id', 'suitename', 'description','createtime', 'runcount', 'runtime','suitecase','creater')

class TestReportSerializer(serializers.ModelSerializer):
    testsuite = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = models.TestReport
        fields = []
        for field in model._meta.fields:
            fields.append(field.name)
        # fields = ('id', 'testsuite', 'result', 'reportname', 'error', 'msg', 'report_data', 'run_time')

class UserSerializer(serializers.HyperlinkedModelSerializer):
    createapi = serializers.StringRelatedField(many=True, read_only=True)
    createcase = serializers.StringRelatedField(many=True, read_only=True)
    createsuite = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('url','id', 'username', 'createapi','createcase','createsuite')