<template>
  <div class="personnel-table">
    <a-spin :spinning="loading">
      <a-table
        :dataSource="relations"
        :columns="columns"
        :pagination="{ pageSize: 20 }"
        :rowKey="record => record.id"
        bordered
      >
        <!-- 组员姓名 -->
        <template #bodyCell="{ column, record }">
          <!-- 项目负责人 -->
          <template v-if="column.dataIndex === 'leaders'">
            <span>{{ record.leaders }}</span>
          </template>
          
          <!-- 项目参与情况 -->
      <template v-if="column.dataIndex === 'project_names'">
            <a-tag v-for="project in record.project_names" :key="project" color="blue">
              {{ project }}
            </a-tag>
          </template>
          
          <!-- 人员角色 -->
          <template v-if="column.dataIndex === 'role'">
            <a-select
              v-model:value="record.role"
              style="width: 120px"
              @change="value => handleRoleChange(record, value)"
            >
              <a-select-option 
                v-for="option in getRoleOptions(record.role)" 
                :key="option.value" 
                :value="option.value"
              >
                {{ option.label }}
              </a-select-option>
            </a-select>
          </template>
          
          <!-- 人员属性 -->
          <template v-if="column.dataIndex === 'attributes'">
            <a-select
              v-model:value="record.attributes"
              mode="multiple"
              style="width: 100%"
              @change="value => handleAttributesChange(record, value)"
            >
              <a-select-option v-for="option in attributeOptions" :key="option.value" :value="option.value">
                {{ option.label }}
              </a-select-option>
            </a-select>
          </template>
        </template>
      </a-table>
    </a-spin>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue';
import { useRelationStore } from '../../store/relation';

const store = useRelationStore();
const loading = computed(() => store.loading);
const relations = computed(() => store.relations);

// 表格列定义
const columns = [
  {
    title: '组员姓名',
    dataIndex: 'employee_name',
    key: 'employee_name',
    sorter: (a, b) => a.employee_name.localeCompare(b.employee_name),
  },
  {
    title: '项目负责人',
    dataIndex: 'leaders',
    key: 'leaders',
  },
  {
    title: '负责人数量',
    dataIndex: 'leader_count',
    key: 'leader_count',
    sorter: (a, b) => a.leader_count - b.leader_count,
  },
  {
    title: '项目参与情况',
    dataIndex: 'project_names',
    key: 'project_names',
  },
  {
    title: '人员角色',
    dataIndex: 'role',
    key: 'role',
    filters: [
      { text: '项目负责人', value: 'project_leader' },
      { text: '项目组员', value: 'project_member' },
      { text: '自由人', value: 'free_person' },
    ],
    onFilter: (value, record) => record.role === value,
  },
  {
    title: '人员属性',
    dataIndex: 'attributes',
    key: 'attributes',
  },
];

// 角色选项
const roleOptions = [
  { value: 'project_leader', label: '项目负责人' },
  { value: 'project_member', label: '项目组员' },
  { value: 'free_person', label: '自由人' },
];

// 属性选项
const attributeOptions = [
  { value: 'tech_dev', label: '技术开发' },
  { value: 'project_manager', label: '项目管理' },
  { value: 'test', label: '测试' },
  { value: 'design', label: '设计' },
  { value: 'operation', label: '运营' },
  { value: 'market', label: '市场' },
  { value: 'other', label: '其他' },
];

// 格式化项目负责人显示
const formatLeaders = (leaders) => {
  console.log(leaders)
  if (!leaders || !leaders.length) return '无';
  return leaders.map(leader => leader.name).join('、');
};

// 根据当前角色获取可选的角色选项（只能由高向低变更）
const getRoleOptions = (currentRole) => {
  const roleLevels = {
    'project_leader': 3,
    'project_member': 2,
    'free_person': 1
  };
  
  return roleOptions.filter(option => 
    roleLevels[option.value] <= roleLevels[currentRole]
  );
};

// 处理角色变更
const handleRoleChange = async (record, newRole) => {
  if (record.role === newRole) return;
  
  // 更新角色
  await store.updateRelation(record.id, {
    role: newRole
  });
};

// 处理属性变更
const handleAttributesChange = async (record, newAttributes) => {
  // 更新属性
  await store.updateRelation(record.id, {
    attributes: newAttributes
  });
};
</script>

<style scoped>
.personnel-table {
  width: 100%;
}
</style>