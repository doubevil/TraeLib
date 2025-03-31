from rest_framework import serializers
from .models import Department, Employee, Project, EmployeeRelation

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class EmployeeSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)
    
    class Meta:
        model = Employee
        fields = ['id', 'name', 'department', 'department_name', 'ip_address', 
                  'job_type', 'position', 'role', 'created_at', 'updated_at']

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

class EmployeeRelationSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.name', read_only=True)
    
    class Meta:
        model = EmployeeRelation
        fields = ['id', 'date', 'employee', 'employee_name', 'leaders', 
                  'leader_count', 'project_names', 'role', 'attributes', 
                  'created_at', 'updated_at']

class EmployeeRelationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeRelation
        fields = ['role', 'attributes', 'leaders']
    
    def validate_role(self, value):
        # 验证角色变更是否合法（只能由高向低变更）
        instance = self.instance
        if instance:
            current_role = instance.role
            # 角色等级: project_leader > project_member > free_person
            role_levels = {
                'project_leader': 3,
                'project_member': 2,
                'free_person': 1
            }
            
            if role_levels.get(value, 0) > role_levels.get(current_role, 0):
                raise serializers.ValidationError("角色只能由高向低变更")
        
        return value