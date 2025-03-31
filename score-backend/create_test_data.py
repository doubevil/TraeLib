import os
import django
import random
import json
from datetime import datetime

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'score_system.settings')
django.setup()

from performance.models import Department, Employee, Project, EmployeeRelation, Indicator, Assessment, FinalScore
from django.contrib.auth.models import User

# 创建超级用户
def create_superuser():
    print("创建超级用户...")
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print("超级用户创建成功")
    else:
        print("超级用户已存在")

# 创建部门数据
def create_departments():
    print("创建部门数据...")
    departments = [
        {"name": "研发部", "description": "负责产品研发"},
        {"name": "测试部", "description": "负责产品测试"},
        {"name": "运维部", "description": "负责系统运维"},
        {"name": "产品部", "description": "负责产品设计"},
        {"name": "市场部", "description": "负责市场推广"}
    ]
    
    created_departments = []
    for dept in departments:
        department, created = Department.objects.get_or_create(
            name=dept["name"],
            defaults={"description": dept["description"]}
        )
        created_departments.append(department)
        print(f"创建部门: {department.name}")
    
    return created_departments

# 生成真实中文姓名
def generate_chinese_name():
    surnames = [
        "李", "王", "张", "刘", "陈", "杨", "赵", "黄", "周", "吴",
        "徐", "孙", "胡", "朱", "高", "林", "何", "郭", "马", "罗",
        "梁", "宋", "郑", "谢", "韩", "唐", "冯", "于", "董", "萧",
        "程", "曹", "袁", "邓", "许", "傅", "沈", "曾", "彭", "吕"
    ]
    
    names = [
        "伟", "芳", "娜", "秀英", "敏", "静", "丽", "强", "磊", "军",
        "洋", "勇", "艳", "杰", "娟", "涛", "明", "超", "秀兰", "霞",
        "平", "刚", "桂英", "文", "辉", "建华", "宇", "鑫", "燕", "玲",
        "桂兰", "浩", "凯", "秀珍", "健", "俊", "帆", "雪", "帅", "慧"
    ]
    
    return random.choice(surnames) + random.choice(names)

# 创建员工数据
def create_employees(departments):
    print("创建员工数据...")
    employees = []
    
    # 为每个部门创建一个部门负责人
    for dept in departments:
        leader_name = generate_chinese_name()
        leader, created = Employee.objects.get_or_create(
            name=leader_name,
            defaults={
                "department": dept,
                "ip_address": "192.168.1.1",
                "job_type": "管理",
                "position": "部门经理",
                "role": "department_leader"
            }
        )
        employees.append(leader)
        print(f"创建部门负责人: {leader.name}")
    
    # 为每个部门创建项目负责人和项目组员
    roles = ["project_leader", "project_member", "project_member", "free_person"]
    positions = ["高级工程师", "中级工程师", "初级工程师", "实习生"]
    job_types = ["开发", "测试", "运维", "设计", "产品"]
    
    for dept in departments:
        for i in range(5):  # 每个部门创建5个员工
            role = roles[i % len(roles)]
            position = positions[i % len(positions)]
            job_type = job_types[i % len(job_types)]
            
            employee_name = generate_chinese_name()
            employee, created = Employee.objects.get_or_create(
                name=employee_name,
                defaults={
                    "department": dept,
                    "ip_address": f"192.168.1.{random.randint(2, 254)}",
                    "job_type": job_type,
                    "position": position,
                    "role": role
                }
            )
            employees.append(employee)
            print(f"创建员工: {employee.name}, 角色: {role}")
    
    return employees

# 创建项目数据
def create_projects():
    print("创建项目数据...")
    projects = [
        {"name": "智能客服系统", "description": "基于AI的智能客服系统"},
        {"name": "数据分析平台", "description": "企业级数据分析平台"},
        {"name": "移动办公APP", "description": "企业移动办公应用"},
        {"name": "电子商务平台", "description": "B2B电子商务交易平台"},
        {"name": "企业内控系统", "description": "企业内部控制管理系统"}
    ]
    
    created_projects = []
    for proj in projects:
        project, created = Project.objects.get_or_create(
            name=proj["name"],
            defaults={"description": proj["description"]}
        )
        created_projects.append(project)
        print(f"创建项目: {project.name}")
    
    return created_projects

# 创建考核指标数据
def create_indicators(departments):
    # 保持不变
    print("创建考核指标数据...")
    
    for dept in departments:
        dept_name = dept.name
        
        # 创建基础项
        Indicator.objects.get_or_create(
            dept=dept_name,
            seq=1,
            defaults={
                "kind": "0",
                "title": "工作质量",
                "cot": "工作成果的质量和准确性",
                "cotdtl": "评估工作成果是否符合要求，是否有错误或需要返工",
                "deft": 80,
                "min_score": 0,
                "max_score": 100
            }
        )
        
        Indicator.objects.get_or_create(
            dept=dept_name,
            seq=2,
            defaults={
                "kind": "0",
                "title": "工作效率",
                "cot": "完成工作的速度和效率",
                "cotdtl": "评估工作完成的及时性和效率",
                "deft": 80,
                "min_score": 0,
                "max_score": 100
            }
        )
        
        Indicator.objects.get_or_create(
            dept=dept_name,
            seq=3,
            defaults={
                "kind": "0",
                "title": "团队协作",
                "cot": "与团队成员的协作能力",
                "cotdtl": "评估与团队成员的沟通和协作情况",
                "deft": 80,
                "min_score": 0,
                "max_score": 100
            }
        )
        
        # 创建加分项
        Indicator.objects.get_or_create(
            dept=dept_name,
            seq=4,
            defaults={
                "kind": "1",
                "title": "创新能力",
                "cot": "提出创新想法和解决方案",
                "cotdtl": "评估在工作中提出的创新想法和解决方案",
                "deft": 0,
                "min_score": 0,
                "max_score": 20
            }
        )
        
        Indicator.objects.get_or_create(
            dept=dept_name,
            seq=5,
            defaults={
                "kind": "1",
                "title": "知识分享",
                "cot": "分享知识和经验",
                "cotdtl": "评估在团队中分享知识和经验的情况",
                "deft": 0,
                "min_score": 0,
                "max_score": 10
            }
        )
        
        # 创建减分项
        Indicator.objects.get_or_create(
            dept=dept_name,
            seq=6,
            defaults={
                "kind": "2",
                "title": "违规行为",
                "cot": "违反公司规定或工作纪律",
                "cotdtl": "因违反公司规定或工作纪律而扣分",
                "deft": 0,
                "min_score": 0,
                "max_score": 0
            }
        )
        
        Indicator.objects.get_or_create(
            dept=dept_name,
            seq=7,
            defaults={
                "kind": "2",
                "title": "工作失误",
                "cot": "工作中的重大失误",
                "cotdtl": "因工作中的重大失误而扣分",
                "deft": 0,
                "min_score": -15,
                "max_score": 0
            }
        )
    
    print(f"已为每个部门创建7个考核指标")

# 创建员工关系数据
def create_employee_relations(employees, projects):
    print("创建员工关系数据...")
    
    # 获取当前月份，格式为 YYYYMM
    current_period = datetime.now().strftime("%Y%m")
    
    # 获取所有项目负责人
    project_leaders = [emp for emp in employees if emp.role == "project_leader"]
    
    # 确保每个项目负责人在员工关系中的角色也是项目负责人
    for employee in employees:
        # 跳过部门负责人
        if employee.role == "department_leader":
            continue
        
        # 确定角色
        role = employee.role
        
        # 确定项目名称列表
        if role == "free_person":
            project_names = []
        else:
            # 随机选择1-3个项目
            num_projects = random.randint(1, 3)
            selected_projects = random.sample(projects, min(num_projects, len(projects)))
            project_names = [proj.name for proj in selected_projects]
        
        # 确定属性
        attributes = []
        if employee.job_type == "开发":
            attributes.append("tech_dev")
        elif employee.job_type == "测试":
            attributes.append("test")
        elif employee.job_type == "产品":
            attributes.append("project_manager")
        elif employee.job_type == "设计":
            attributes.append("design")
        elif employee.job_type == "运维":
            attributes.append("operation")
        
        # 随机添加1-2个额外属性
        possible_attributes = ["tech_dev", "project_manager", "test", "design", "operation", "market", "other"]
        possible_attributes = [attr for attr in possible_attributes if attr not in attributes]
        num_extra_attrs = random.randint(0, 2)
        if num_extra_attrs > 0 and possible_attributes:
            extra_attrs = random.sample(possible_attributes, min(num_extra_attrs, len(possible_attributes)))
            attributes.extend(extra_attrs)
        
        # 确定项目负责人
        if role == "free_person":
            leaders_str = ""
        elif role == "project_leader":
            # 如果是项目负责人，则自己也是自己的负责人
            leaders_str = employee.name
        else:
            # 随机选择1-2个项目负责人
            num_leaders = random.randint(1, min(2, len(project_leaders)))
            selected_leaders = random.sample(project_leaders, num_leaders)
            leaders_str = ",".join([leader.name for leader in selected_leaders])
        
        # 创建员工关系
        relation, created = EmployeeRelation.objects.get_or_create(
            date=current_period,
            employee=employee,
            defaults={
                "leaders": leaders_str,
                "project_names": project_names,
                "role": role,
                "attributes": attributes
            }
        )
        
        # 确保leader_count与leaders字段一致
        if created:
            relation.leader_count = len(relation.leaders.split(',')) if relation.leaders else 0
            relation.save()
        
        print(f"创建员工关系: {employee.name}, 角色: {role}, 项目数: {len(project_names)}")

# 创建考核数据
def create_assessments(employees):
    print("创建考核数据...")
    
    # 获取当前月份，格式为 YYYYMM
    current_period = datetime.now().strftime("%Y%m")
    
    # 获取所有部门负责人
    department_leaders = {emp.department.id: emp for emp in employees if emp.role == "department_leader"}
    
    # 获取所有项目负责人
    project_leaders = [emp for emp in employees if emp.role == "project_leader"]
    
    for employee in employees:
        # 跳过部门负责人
        if employee.role == "department_leader":
            continue
        
        # 获取该员工的部门负责人
        dept_leader = department_leaders.get(employee.department.id)
        
        if dept_leader:
            # 创建部门负责人评价
            scores = {}
            indicators = Indicator.objects.filter(dept=employee.department.name)
            
            for indicator in indicators:
                if indicator.kind == "0":  # 基础项
                    scores[str(indicator.seq)] = random.randint(70, 95)
                elif indicator.kind == "1":  # 加分项
                    scores[str(indicator.seq)] = random.randint(0, int(indicator.max_score))
                elif indicator.kind == "2":  # 减分项
                    scores[str(indicator.seq)] = random.randint(int(indicator.min_score), 0)
            
            assessment, created = Assessment.objects.get_or_create(
                employee=employee,
                evaluator=dept_leader,
                period=current_period,
                defaults={
                    "status": "completed",
                    "scores": scores,
                    "comment": f"{dept_leader.name}对{employee.name}的评价"
                }
            )
            
            if created:
                assessment.total_score = assessment.calculate_total_score()
                assessment.save()
            
            print(f"创建部门负责人评价: {dept_leader.name} -> {employee.name}")
        
        # 创建项目负责人评价
        if employee.role != "project_leader" and project_leaders:
            # 随机选择一个项目负责人
            project_leader = random.choice(project_leaders)
            
            scores = {}
            indicators = Indicator.objects.filter(dept=employee.department.name)
            
            for indicator in indicators:
                if indicator.kind == "0":  # 基础项
                    scores[str(indicator.seq)] = random.randint(70, 95)
                elif indicator.kind == "1":  # 加分项
                    scores[str(indicator.seq)] = random.randint(0, int(indicator.max_score))
                elif indicator.kind == "2":  # 减分项
                    scores[str(indicator.seq)] = random.randint(int(indicator.min_score), 0)
            
            assessment, created = Assessment.objects.get_or_create(
                employee=employee,
                evaluator=project_leader,
                period=current_period,
                defaults={
                    "status": "completed",
                    "scores": scores,
                    "comment": f"{project_leader.name}对{employee.name}的评价"
                }
            )
            
            if created:
                assessment.total_score = assessment.calculate_total_score()
                assessment.save()
            
            print(f"创建项目负责人评价: {project_leader.name} -> {employee.name}")
        
        # 创建自评
        scores = {}
        indicators = Indicator.objects.filter(dept=employee.department.name)
        
        for indicator in indicators:
            if indicator.kind == "0":  # 基础项
                scores[str(indicator.seq)] = random.randint(80, 100)
            elif indicator.kind == "1":  # 加分项
                scores[str(indicator.seq)] = random.randint(0, int(indicator.max_score))
            elif indicator.kind == "2":  # 减分项
                scores[str(indicator.seq)] = 0  # 自评通常不会给自己减分
        
        assessment, created = Assessment.objects.get_or_create(
            employee=employee,
            evaluator=employee,  # 自评
            period=current_period,
            defaults={
                "status": "completed",
                "scores": scores,
                "comment": f"{employee.name}的自评"
            }
        )
        
        if created:
            assessment.total_score = assessment.calculate_total_score()
            assessment.save()
        
        print(f"创建自评: {employee.name}")

def create_final_scores(employees):
    print("创建最终得分数据...")
    
    # 获取当前月份，格式为 YYYYMM
    current_period = datetime.now().strftime("%Y%m")
    
    for employee in employees:
        # 跳过部门负责人
        if employee.role == "department_leader":
            continue
        
        # 获取该员工的所有评价
        assessments = Assessment.objects.filter(
            employee=employee,
            period=current_period
        )
        
        if assessments:
            # 获取部门负责人评分
            dept_leader_assessment = assessments.filter(
                evaluator__role="department_leader"
            ).first()
            
            dept_leader_score = dept_leader_assessment.total_score if dept_leader_assessment else 0
            
            # 获取项目负责人评分
            project_leader_assessment = assessments.filter(
                evaluator__role="project_leader"
            ).first()
            
            project_leader_score = project_leader_assessment.total_score if project_leader_assessment else 0
            
            # 获取自评分
            self_assessment = assessments.filter(
                evaluator=employee
            ).first()
            
            self_score = self_assessment.total_score if self_assessment else 0
            
            # 计算最终得分
            # 部门负责人评分占50%，项目负责人评分占30%，自评分占20%
            final_score = dept_leader_score * 0.5 + project_leader_score * 0.3 + self_score * 0.2
            
            # 创建最终得分
            final_score_obj, created = FinalScore.objects.get_or_create(
                employee=employee,
                period=current_period,
                defaults={
                    "department_leader_score": dept_leader_score,
                    "project_leader_score": project_leader_score,
                    "self_score": self_score,
                    "final_score": final_score,
                    "rank": 0  # 排名将在后面更新
                }
            )
            
            print(f"创建最终得分: {employee.name}, 得分: {final_score:.2f}")
    
    # 更新排名
    update_ranks(current_period)

# 更新排名
def update_ranks(period):
    print("更新排名...")
    
    # 按部门分组，更新排名
    departments = Department.objects.all()
    
    for dept in departments:
        # 获取该部门所有员工的最终得分，按得分降序排序
        final_scores = FinalScore.objects.filter(
            employee__department=dept,
            period=period
        ).order_by('-final_score')
        
        # 更新排名
        for i, final_score in enumerate(final_scores):
            final_score.rank = i + 1
            final_score.save()
    
    print("排名更新完成")

# 主函数
def main():
    create_superuser()
    departments = create_departments()
    employees = create_employees(departments)
    projects = create_projects()
    create_indicators(departments)
    create_employee_relations(employees, projects)
    create_assessments(employees)
    create_final_scores(employees)
    
    print("测试数据创建完成！")

if __name__ == "__main__":
    main()