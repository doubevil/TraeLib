from django.db import models

class Department(models.Model):
    """部门模型"""
    name = models.CharField(max_length=100, verbose_name="部门名称")
    description = models.TextField(blank=True, null=True, verbose_name="部门描述")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "部门"
        verbose_name_plural = "部门"
        ordering = ['name']

    def __str__(self):
        return self.name

class Employee(models.Model):
    """员工模型"""
    ROLE_CHOICES = (
        ('department_leader', '部门负责人'),
        ('project_leader', '项目负责人'),
        ('project_member', '项目组员'),
        ('free_person', '自由人'),  # 添加自由人角色
    )
    
    name = models.CharField(max_length=100, verbose_name="姓名")
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="employees", verbose_name="所属部门")
    ip_address = models.GenericIPAddressField(verbose_name="IP地址")
    job_type = models.CharField(max_length=100, verbose_name="工种")
    position = models.CharField(max_length=100, verbose_name="职位")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, verbose_name="角色")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "员工"
        verbose_name_plural = "员工"
        ordering = ['department', 'name']

    def __str__(self):
        return f"{self.name} ({self.department.name})"

class Indicator(models.Model):
    """考核指标模型 - 根据scoreCategories.js修改"""
    KIND_CHOICES = (
        ('0', '基础项'),
        ('1', '加分项'),
        ('2', '减分项'),
    )
    
    dept = models.CharField(max_length=100, verbose_name="部门")
    kind = models.CharField(max_length=10, choices=KIND_CHOICES, verbose_name="项点类别")
    title = models.CharField(max_length=100, verbose_name="项点类别标题")
    seq = models.IntegerField(verbose_name="项点序号")
    cot = models.CharField(max_length=200, verbose_name="项点内容")
    cotdtl = models.TextField(verbose_name="项点详细说明")
    deft = models.FloatField(default=0, verbose_name="项点默认值")
    min_score = models.FloatField(default=0, verbose_name="项点最小值")
    max_score = models.FloatField(default=100, verbose_name="项点最大值")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "考核指标"
        verbose_name_plural = "考核指标"
        ordering = ['dept', 'kind', 'seq']
        unique_together = ('dept', 'seq')

    def __str__(self):
        return f"{self.title} - {self.cot} ({self.dept})"

class Project(models.Model):
    """项目模型"""
    name = models.CharField(max_length=100, verbose_name="项目名称")
    description = models.TextField(blank=True, null=True, verbose_name="项目描述")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "项目"
        verbose_name_plural = "项目"
        ordering = ['name']

    def __str__(self):
        return self.name

# 删除 EmployeeProjectParticipation 模型

class EmployeeRelation(models.Model):
    """员工关系模型 - 根据README-Relation.md修改"""
    ROLE_CHOICES = (
        ('project_leader', '项目负责人'),
        ('project_member', '项目组员'),
        ('free_person', '自由人'),
    )
    
    ATTRIBUTE_CHOICES = (
        ('tech_dev', '技术开发'),
        ('project_manager', '项目管理'),
        ('test', '测试'),
        ('design', '设计'),
        ('operation', '运营'),
        ('market', '市场'),
        ('other', '其他'),
    )
    
    date = models.CharField(max_length=6, verbose_name="数据日期")  # 格式：YYYYMM
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="relations", verbose_name="组员")
    # 修改为 CharField 类型，存储项目负责人姓名，用逗号分隔
    leaders = models.CharField(max_length=500, blank=True, default="", verbose_name="项目负责人")
    leader_count = models.IntegerField(default=0, verbose_name="负责人数量")
    # 修改为直接存储项目名称列表
    project_names = models.JSONField(default=list, verbose_name="参与项目名称")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, verbose_name="人员角色")
    attributes = models.JSONField(default=list, verbose_name="人员属性")  # 存储多个属性值的列表
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "员工关系"
        verbose_name_plural = "员工关系"
        ordering = ['-date', 'employee__name']
        unique_together = ('employee', 'date')

    def __str__(self):
        return f"{self.employee.name} - {self.date} ({self.get_role_display()})"
    
    def save(self, *args, **kwargs):
        # 如果角色是自由人，清空项目负责人
        if self.role == 'free_person':
            self.leaders = ""
            self.leader_count = 0
        else:
            # 更新负责人数量
            if self.leaders:
                self.leader_count = len(self.leaders.split(','))
            else:
                self.leader_count = 0
        
        super().save(*args, **kwargs)

class Assessment(models.Model):
    """考核模型 - 修改为包含考核详情"""
    STATUS_CHOICES = (
        ('pending', '待评价'),
        ('in_progress', '评价中'),
        ('completed', '已完成'),
    )
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="assessments", verbose_name="被考核员工")
    evaluator = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="evaluations", verbose_name="评价人")
    period = models.CharField(max_length=6, verbose_name="考核周期")  # 格式：YYYYMM
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="状态")
    # 新增考核详情字段，通过键值对方式存储考核明细，格式为{"1":80,"2":90}
    scores = models.JSONField(default=dict, verbose_name="考核得分")
    total_score = models.FloatField(default=0, verbose_name="总分")
    comment = models.TextField(blank=True, null=True, verbose_name="评语")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "考核"
        verbose_name_plural = "考核"
        ordering = ['-period', 'employee__name']
        unique_together = ('employee', 'evaluator', 'period')

    def __str__(self):
        return f"{self.employee.name} - {self.period} ({self.evaluator.name})"
    
    def calculate_total_score(self):
        """计算总分"""
        if not self.scores:
            return 0
        
        # 获取所有指标
        indicators = {str(ind.seq): ind for ind in Indicator.objects.filter(dept=self.employee.department.name)}
        
        total = 0
        for seq, score in self.scores.items():
            if seq in indicators:
                # 根据指标类型计算得分
                indicator = indicators[seq]
                if indicator.kind == '0':  # 基础项
                    total += float(score)
                elif indicator.kind == '1':  # 加分项
                    total += float(score)
                elif indicator.kind == '2':  # 减分项
                    total -= float(score)
        
        return total
    
    def save(self, *args, **kwargs):
        # 计算总分
        self.total_score = self.calculate_total_score()
        super().save(*args, **kwargs)

# 删除 AssessmentDetail 模型

class FinalScore(models.Model):
    """最终得分模型"""
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="final_scores", verbose_name="员工")
    period = models.CharField(max_length=6, verbose_name="考核周期")  # 格式：YYYYMM
    department_leader_score = models.FloatField(default=0, verbose_name="部门负责人评分")
    project_leader_score = models.FloatField(default=0, verbose_name="项目负责人评分")
    self_score = models.FloatField(default=0, verbose_name="自评分")
    final_score = models.FloatField(default=0, verbose_name="最终得分")
    rank = models.IntegerField(default=0, verbose_name="排名")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "最终得分"
        verbose_name_plural = "最终得分"
        ordering = ['-period', '-final_score']
        unique_together = ('employee', 'period')

    def __str__(self):
        return f"{self.employee.name} - {self.period} ({self.final_score})"
