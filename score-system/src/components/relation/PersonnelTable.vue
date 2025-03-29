<template>
  <div class="personnel-table">
    <a-table 
      :dataSource="personnelData" 
      :columns="columns"
      :pagination="{ pageSize: 10 }"
      :rowKey="record => record.memberName"
      :scroll="{ y: 'calc(100vh - 250px)', x: 1200 }"
    >
      <!-- 姓名列 -->
      <template #bodyCell="{ column, record }">
        <template v-if="column.dataIndex === 'memberName'">
          <span>{{ record.memberName }}</span>
        </template>
        
        <!-- 项目负责人列 -->
        <template v-if="column.dataIndex === 'leaderNames'">
          <template v-if="record.leaderNames && record.leaderNames.length > 0">
            <a-tag v-for="leader in record.leaderNames" :key="leader" color="blue">
              {{ leader }}
            </a-tag>
          </template>
          <template v-else>
            <span>-</span>
          </template>
        </template>
        
        <!-- 角色列 -->
        <template v-if="column.dataIndex === 'role'">
          <a-select 
            v-model:value="record.role" 
            style="width: 120px"
            :options="getAvailableRoles(record)"
            @change="(value) => updateRole(record.memberName, value)"
          />
        </template>
        
        <!-- 项目列 -->
        <template v-if="column.dataIndex === 'projects'">
          <template v-if="record.projects && record.projects.length > 0">
            <a-tag v-for="project in record.projects" :key="project" color="green">
              {{ project }}
            </a-tag>
          </template>
          <template v-else>
            <span>-</span>
          </template>
        </template>
        
        <!-- 属性列 -->
        <template v-if="column.dataIndex === 'attributes'">
          <a-select 
            v-model:value="record.attributes" 
            mode="multiple" 
            style="width: 100%"
            :options="attributeOptions.map(attr => ({ value: attr, label: attr }))"
            @change="(value) => updateAttributes(record.memberName, value)"
          />
        </template>
      </template>
    </a-table>
    
    <div class="table-footer">
      <a-button type="primary" @click="saveChanges">保存更改</a-button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useRelationStore } from '../../store/relation';
import { message } from 'ant-design-vue';

const store = useRelationStore();
const personnelData = computed(() => store.personnelData);
const roleOptions = computed(() => store.roleOptions);
const attributeOptions = computed(() => store.attributeOptions);
const roleRanking = computed(() => store.roleRanking);

const columns = [
  {
    title: '组员姓名',
    dataIndex: 'memberName',
    key: 'memberName',
    width: 100,
    fixed: 'left',
    sorter: (a, b) => a.memberName.localeCompare(b.memberName),
  },
  {
    title: '项目负责人',
    dataIndex: 'leaderNames',
    key: 'leaderNames',
    width: 200,
  },
  {
    title: '负责人数量',
    dataIndex: 'leaderCount',
    key: 'leaderCount',
    width: 100,
    sorter: (a, b) => a.leaderCount - b.leaderCount,
  },
  {
    title: '项目参与情况',
    dataIndex: 'projects',
    key: 'projects',
    width: 250,
  },
  {
    title: '人员角色',
    dataIndex: 'role',
    key: 'role',
    width: 150,
    filters: roleOptions.value.map(role => ({ text: role, value: role })),
    onFilter: (value, record) => record.role === value,
  },
  {
    title: '人员属性',
    dataIndex: 'attributes',
    key: 'attributes',
    width: 300,
  }
];

// 根据当前角色获取可用的角色选项（只能由高向低变更）
const getAvailableRoles = (record) => {
  const currentRoleRank = roleRanking.value[record.role];
  return roleOptions.value
    .filter(role => roleRanking.value[role] <= currentRoleRank)
    .map(role => ({ value: role, label: role }));
};

const updateRole = async (personName, newRole) => {
  try {
    await store.updatePersonRole(personName, newRole);
    message.success(`已将 ${personName} 的角色更新为 ${newRole}`);
  } catch (error) {
    message.error(error.message);
    // 刷新数据，恢复原始状态
    await store.importData(store.currentDate);
  }
};

const updateAttributes = async (personName, attributes) => {
  try {
    await store.updatePersonAttributes(personName, attributes);
    message.success(`已更新 ${personName} 的人员属性`);
  } catch (error) {
    message.error(error.message);
  }
};

const saveChanges = async () => {
  try {
    await store.saveChanges();
    message.success('所有更改已保存');
  } catch (error) {
    message.error('保存失败: ' + error.message);
  }
};
</script>

<style scoped>
.personnel-table {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.table-footer {
  margin-top: 16px;
  display: flex;
  justify-content: flex-end;
}
</style>