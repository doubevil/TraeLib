<template>
  <div class="import-data">
    <a-space>
      <a-date-picker
        v-model:value="selectedDate"
        :format="dateFormat"
        picker="month"
        placeholder="选择月份"
        @change="handleDateChange"
      />
      <a-upload
        name="file"
        :beforeUpload="beforeUpload"
        :showUploadList="false"
      >
        <a-button type="primary" :loading="loading">
          <upload-outlined />
          导入数据
        </a-button>
      </a-upload>
      <a-button @click="saveData" :disabled="!canSave">
        <save-outlined />
        保存数据
      </a-button>
    </a-space>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue';
import { UploadOutlined, SaveOutlined } from '@ant-design/icons-vue';
import { message } from 'ant-design-vue';
import { useRelationStore } from '../../store/relation';
import * as XLSX from 'xlsx';
import dayjs from 'dayjs';

const store = useRelationStore();
const loading = computed(() => store.loading);
const selectedDate = ref(null);
const dateFormat = 'YYYY-MM';

// 格式化日期为YYYYMM格式
const formattedDate = computed(() => {
  if (!selectedDate.value) return '';
  return dayjs(selectedDate.value).format('YYYYMM');
});

// 判断是否可以保存数据
const canSave = computed(() => {
  // 修改这里，使用 store.relations 而不是直接访问 relations
  return store.relations && store.relations.length > 0 && formattedDate.value;
});

// 处理日期变更
const handleDateChange = async (date) => {
  selectedDate.value = date;
  if (formattedDate.value) {
    await fetchData();
  }
};

// 获取数据
const fetchData = async () => {
  if (!formattedDate.value) {
    message.warning('请先选择日期');
    return;
  }
  
  await store.fetchRelationsByDate(formattedDate.value);
};

// 保存数据
const saveData = async () => {
  if (!canSave.value) {
    message.warning('没有可保存的数据');
    return;
  }
  
  try {
    await store.saveRelations(formattedDate.value);
    message.success('数据保存成功');
  } catch (error) {
    message.error(`保存数据失败: ${error.message}`);
    console.error('保存数据失败:', error);
  }
};

// 处理文件上传前的逻辑
const beforeUpload = (file) => {
  if (!formattedDate.value) {
    message.warning('请先选择日期');
    return false;
  }
  
  const reader = new FileReader();
  reader.onload = (e) => {
    const data = e.target.result;
    const workbook = XLSX.read(data, { type: 'array' });
    const firstSheetName = workbook.SheetNames[0];
    const worksheet = workbook.Sheets[firstSheetName];
    const json = XLSX.utils.sheet_to_json(worksheet);
    
    // 处理导入数据
    processImportData(json);
  };
  reader.readAsArrayBuffer(file);
  
  // 阻止默认上传行为
  return false;
};

// 处理导入数据
const processImportData = (data) => {
  if (!data || data.length === 0) {
    message.error('导入数据为空');
    return;
  }
  
  // 转换数据格式
  const relations = data.map(item => {
    // 处理项目负责人，可能是逗号分隔的字符串
    const leaderNames = item['项目负责人'] ? 
      item['项目负责人'].split(/[,，、]/).filter(Boolean) : [];
    
    // 处理项目参与情况，可能是逗号分隔的字符串
    const projectNames = item['组员项目参与情况'] ? 
      item['组员项目参与情况'].split(/[,，、]/).filter(Boolean) : [];
    
    // 处理人员属性，可能是逗号分隔的字符串
    const attributes = item['人员属性'] ? 
      item['人员属性'].split(/[,，、]/).filter(Boolean) : [];
    
    // 确定角色
    let role = item['人员角色'] || 'free_person';
    if (!leaderNames.length && role !== 'free_person') {
      role = 'free_person';
    }
    
    return {
      employee_name: item['组员姓名'],
      leader_names: leaderNames,
      project_names: projectNames,
      role: mapRoleToValue(role),
      attributes: mapAttributesToValues(attributes)
    };
  });
  
  // 导入数据
  store.importRelations({
    date: formattedDate.value,
    relations: relations
  });
};

// 映射角色名称到值
const mapRoleToValue = (roleName) => {
  const roleMap = {
    '项目负责人': 'project_leader',
    '项目组员': 'project_member',
    '自由人': 'free_person'
  };
  return roleMap[roleName] || 'free_person';
};

// 映射属性名称到值
const mapAttributesToValues = (attributes) => {
  const attributeMap = {
    '技术开发': 'tech_dev',
    '项目管理': 'project_manager',
    '测试': 'test',
    '设计': 'design',
    '运营': 'operation',
    '市场': 'market',
    '其他': 'other'
  };
  
  return attributes.map(attr => attributeMap[attr] || 'other');
};
</script>

<style scoped>
.import-data {
  display: flex;
  align-items: center;
}
</style>