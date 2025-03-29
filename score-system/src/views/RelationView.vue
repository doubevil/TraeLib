<template>
  <div class="relation-system">
    <header-bar />
    
    <div class="main-content">
      <div class="toolbar">
        <import-data />
        <div class="date-display" v-if="isDataImported">
          当前查看: <span class="date-value">{{ formatDate(currentDate) }}</span>
        </div>
        <div class="statistics">
          <div class="stat-item">
            <div class="stat-label">项目负责人：</div>
            <div class="stat-value">{{ projectLeaderCount }}人</div>
          </div>
          <div class="stat-item">
            <div class="stat-label">项目组员：</div>
            <div class="stat-value">{{ projectMemberCount }}人</div>
          </div>
          <div class="stat-item">
            <div class="stat-label">自由人：</div>
            <div class="stat-value">{{ freePersonCount }}人</div>
          </div>
        </div>
      </div>
      
      <div class="content-wrapper" v-if="isDataImported">
        <a-tabs v-model:activeKey="activeTabKey">
          <a-tab-pane key="table" tab="表格视图">
            <personnel-table />
          </a-tab-pane>
          <a-tab-pane key="relation" tab="关系视图">
            <relation-view-component />
          </a-tab-pane>
        </a-tabs>
      </div>
      
      <div class="empty-state" v-else>
        <a-empty description="请先选择日期并导入数据" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRelationStore } from '../store/relation';
import HeaderBar from '../components/HeaderBar.vue';
import ImportData from '../components/relation/ImportData.vue';
import PersonnelTable from '../components/relation/PersonnelTable.vue';
import RelationViewComponent from '../components/relation/RelationView.vue';

const store = useRelationStore();
const activeTabKey = ref('table');

const projectLeaderCount = computed(() => store.projectLeaderCount);
const projectMemberCount = computed(() => store.projectMemberCount);
const freePersonCount = computed(() => store.freePersonCount);
const isDataImported = computed(() => store.isDataImported);
const currentDate = computed(() => store.currentDate);

const formatDate = (dateStr) => {
  if (!dateStr || dateStr.length !== 6) return dateStr;
  const year = dateStr.substring(0, 4);
  const month = dateStr.substring(4, 6);
  return `${year}年${month}月`;
};
</script>

<style scoped>
.relation-system {
  display: flex;
  flex-direction: column;
  height: 100vh;
  width: 100vw;
  overflow: hidden;
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
}

.main-content {
  display: flex;
  flex-direction: column;
  flex: 1;
  overflow: hidden;
  padding: 15px;
}

.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.date-display {
  font-size: 14px;
  color: #666;
}

.date-value {
  font-weight: bold;
  color: #1890ff;
}

.statistics {
  display: flex;
  gap: 20px;
}

.stat-item {
  display: flex;
  align-items: center;
}

.stat-label {
  font-weight: bold;
  margin-right: 5px;
}

.stat-value {
  color: #1890ff;
  font-weight: bold;
}

.content-wrapper {
  flex: 1;
  overflow: hidden;
}

.empty-state {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
}

:deep(.ant-tabs-content) {
  height: calc(100vh - 200px);
  overflow: auto;
}
</style>