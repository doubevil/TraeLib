from django.urls import path
from . import views

urlpatterns = [
    # 员工管理
    path('employees/', views.EmployeeListCreateView.as_view(), name='employee-list'),
    path('employees/<int:pk>/', views.EmployeeDetailView.as_view(), name='employee-detail'),
    
    # 人员关系管理
    path('relations/', views.RelationListCreateView.as_view(), name='relation-list'),
    path('relations/<int:pk>/', views.RelationDetailView.as_view(), name='relation-detail'),
    path('relations/import/', views.RelationBulkImportView.as_view(), name='relation-import'),
    path('relations/statistics/', views.RelationStatisticsView.as_view(), name='relation-statistics'),
    
    # 考核流程管理
    path('assessments/', views.AssessmentListCreateView.as_view(), name='assessment-list-create'),
    path('assessments/<int:pk>/', views.AssessmentDetailView.as_view(), name='assessment-detail'),
    path('assessments/assign/', views.AssignAssessmentView.as_view(), name='assessment-assign'),
    
    # 绩效结果查询和统计
    path('statistics/', views.StatisticsView.as_view(), name='statistics'),
    path('reports/', views.ReportGenerationView.as_view(), name='report-generation'),
]