import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'score_system.settings')
django.setup()

from performance.models import Department, Employee, Project, EmployeeRelation, Indicator, Assessment, FinalScore

def clear_data():
    print("清除数据...")
    
    # 按依赖关系顺序删除数据
    print("删除最终得分数据...")
    FinalScore.objects.all().delete()
    
    print("删除考核评价数据...")
    Assessment.objects.all().delete()
    
    print("删除员工关系数据...")
    EmployeeRelation.objects.all().delete()
    
    print("删除考核指标数据...")
    Indicator.objects.all().delete()
    
    print("删除项目数据...")
    Project.objects.all().delete()
    
    print("删除员工数据...")
    Employee.objects.all().delete()
    
    print("删除部门数据...")
    Department.objects.all().delete()
    
    print("数据清除完成！")

if __name__ == "__main__":
    clear_data()