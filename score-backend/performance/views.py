from rest_framework import generics, views, viewsets, filters
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from .models import *
from .serializers import (
    DepartmentSerializer, EmployeeSerializer, ProjectSerializer,
    EmployeeRelationSerializer, EmployeeRelationUpdateSerializer
)

# 员工信息管理
class EmployeeListCreateView(generics.ListCreateAPIView):
    """员工列表和创建视图"""
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['department', 'role']
    search_fields = ['name', 'job_type', 'position']
    ordering_fields = ['name', 'department', 'created_at']

class EmployeeDetailView(generics.RetrieveUpdateDestroyAPIView):
    """员工详情、更新和删除视图"""
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

# 考核指标管理
class IndicatorListCreateView(generics.ListCreateAPIView):
    """考核指标列表和创建视图"""
    # 待实现
    pass

class IndicatorDetailView(generics.RetrieveUpdateDestroyAPIView):
    """考核指标详情、更新和删除视图"""
    # 待实现
    pass

class IndicatorTemplateListCreateView(generics.ListCreateAPIView):
    """指标模板列表和创建视图"""
    # 待实现
    pass

class IndicatorTemplateDetailView(generics.RetrieveUpdateDestroyAPIView):
    """指标模板详情、更新和删除视图"""
    # 待实现
    pass

# 项目建设人员关系管理
class RelationListCreateView(generics.ListCreateAPIView):
    """人员关系列表和创建视图"""
    queryset = EmployeeRelation.objects.all()
    serializer_class = EmployeeRelationSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['date', 'employee', 'role']
    search_fields = ['employee__name', 'leaders', 'project_names']
    ordering_fields = ['date', 'employee__name', 'role']

    def get_queryset(self):
        queryset = super().get_queryset()
        date = self.request.query_params.get('date')
        if date:
            queryset = queryset.filter(date=date)
        return queryset

class RelationDetailView(generics.RetrieveUpdateDestroyAPIView):
    """人员关系详情、更新和删除视图"""
    queryset = EmployeeRelation.objects.all()
    serializer_class = EmployeeRelationSerializer
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return EmployeeRelationUpdateSerializer
        return EmployeeRelationSerializer
    
    @transaction.atomic
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        # 保存原始角色和项目负责人
        original_role = instance.role
        original_leaders = instance.leaders
        
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        
        # 获取新角色和项目负责人
        new_role = serializer.validated_data.get('role', original_role)
        new_leaders = serializer.validated_data.get('leaders', original_leaders)
        
        # 更新当前实例
        self.perform_update(serializer)
        
        # 如果角色发生变化，需要处理相关数据
        if original_role != new_role:
            employee_name = instance.employee.name
            
            # 如果从项目负责人变为其他角色，需要处理其他员工的关系
            if original_role == 'project_leader':
                # 获取所有以该员工为项目负责人的关系
                affected_relations = EmployeeRelation.objects.filter(
                    date=instance.date,
                    leaders__contains=employee_name
                ).exclude(employee=instance.employee)
                
                # 更新这些关系
                for relation in affected_relations:
                    # 从 leaders 字段中移除该员工姓名
                    leader_names = relation.leaders.split(',')
                    if employee_name in leader_names:
                        leader_names.remove(employee_name)
                    
                    relation.leaders = ','.join(leader_names)
                    
                    # 如果移除后没有项目负责人，则将角色设置为自由人
                    if not relation.leaders and relation.role != 'free_person':
                        relation.role = 'free_person'
                    
                    relation.save()
            
            # 如果变为自由人，清空项目负责人
            if new_role == 'free_person':
                instance.leaders = ""
                instance.leader_count = 0
                instance.save(update_fields=['leaders', 'leader_count'])
        
        return Response(EmployeeRelationSerializer(instance).data)

class RelationBulkImportView(views.APIView):
    """批量导入人员关系数据"""
    
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        data = request.data
        date = data.get('date')
        relations = data.get('relations', [])
        
        if not date or not relations:
            return Response(
                {"error": "缺少必要参数"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 清除该日期的现有数据
        EmployeeRelation.objects.filter(date=date).delete()
        
        created_relations = []
        errors = []
        
        for relation_data in relations:
            try:
                # 获取员工
                employee_name = relation_data.get('employee_name')
                employee = Employee.objects.filter(name=employee_name).first()
                if not employee:
                    # 如果员工不存在，返回错误
                    errors.append(f"员工 {employee_name} 不存在")
                    continue
                
                # 获取项目负责人姓名列表
                leader_names = relation_data.get('leader_names', [])
                leaders_str = ','.join(leader_names) if leader_names else ""
                
                # 确定角色
                role = relation_data.get('role', 'free_person')
                if not leader_names and role != 'free_person':
                    role = 'free_person'
                
                # 创建关系
                relation = EmployeeRelation.objects.create(
                    date=date,
                    employee=employee,
                    leaders=leaders_str,
                    project_names=relation_data.get('project_names', []),
                    role=role,
                    attributes=relation_data.get('attributes', [])
                )
                
                created_relations.append(relation)
            
            except Exception as e:
                errors.append(str(e))
        
        return Response({
            "success": True,
            "created_count": len(created_relations),
            "errors": errors
        })

class RelationStatisticsView(views.APIView):
    """人员关系统计视图"""
    
    def get(self, request, *args, **kwargs):
        date = request.query_params.get('date')
        
        if not date:
            return Response(
                {"error": "缺少日期参数"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 获取统计数据
        project_leader_count = EmployeeRelation.objects.filter(
            date=date, role='project_leader'
        ).count()
        
        project_member_count = EmployeeRelation.objects.filter(
            date=date, role='project_member'
        ).count()
        
        free_person_count = EmployeeRelation.objects.filter(
            date=date, role='free_person'
        ).count()
        
        return Response({
            "date": date,
            "project_leader_count": project_leader_count,
            "project_member_count": project_member_count,
            "free_person_count": free_person_count,
            "total_count": project_leader_count + project_member_count + free_person_count
        })

# 考核流程管理
class AssessmentListCreateView(generics.ListCreateAPIView):
    """考核列表和创建视图"""
    # 待实现
    pass

class AssessmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """考核详情、更新和删除视图"""
    # 待实现
    pass

class AssignAssessmentView(views.APIView):
    """考核任务分配视图"""
    # 待实现
    pass

# 绩效结果查询和统计
class StatisticsView(views.APIView):
    """统计分析视图"""
    # 待实现
    pass

class ReportGenerationView(views.APIView):
    """报告生成视图"""
    # 待实现
    pass
