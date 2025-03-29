<template>
  <div class="import-data">
    <a-space>
      <a-select
        v-model:value="selectedDate"
        style="width: 120px"
        placeholder="选择日期"
        :disabled="importing"
      >
        <a-select-option v-for="date in availableDates" :key="date" :value="date">
          {{ formatDate(date) }}
        </a-select-option>
      </a-select>
      
      <a-button 
        type="primary" 
        @click="importData" 
        :loading="importing"
      >
        {{ buttonText }}
      </a-button>
    </a-space>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRelationStore } from '../../store/relation';
import { message } from 'ant-design-vue';

const store = useRelationStore();
const importing = ref(false);
const selectedDate = ref('');

const availableDates = computed(() => store.availableDates);
const isDataImported = computed(() => store.isDataImported);
const currentDate = computed(() => store.currentDate);

const buttonText = computed(() => {
  if (importing.value) return '导入中...';
  if (isDataImported.value && selectedDate.value === currentDate.value) {
    return '已导入';
  }
  return '导入数据';
});

const formatDate = (dateStr) => {
  if (!dateStr || dateStr.length !== 6) return dateStr;
  const year = dateStr.substring(0, 4);
  const month = dateStr.substring(4, 6);
  return `${year}年${month}月`;
};

const importData = async () => {
  if (!selectedDate.value) {
    message.warning('请先选择日期');
    return;
  }
  
  if (isDataImported.value && selectedDate.value === currentDate.value) {
    message.info('当前日期数据已导入');
    return;
  }
  
  importing.value = true;
  try {
    await store.importData(selectedDate.value);
    message.success(`${formatDate(selectedDate.value)}数据导入成功`);
  } catch (error) {
    message.error(`数据导入失败: ${error.message}`);
    console.error(error);
  } finally {
    importing.value = false;
  }
};
</script>

<style scoped>
.import-data {
  margin-right: 20px;
}
</style>