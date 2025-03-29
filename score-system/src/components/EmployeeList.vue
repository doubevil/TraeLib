<template>
  <div class="employee-list">
    <draggable 
      v-model="employeeList" 
      item-key="id"
      @end="onDragEnd"
      :animation="200"
      ghost-class="ghost"
      handle=".drag-handle"
    >
      <template #item="{ element }">
        <div 
          class="employee-item" 
          :class="{ 'selected': element.id === currentEmployeeId }"
          @click="selectEmployee(element.id)"
        >
          <div class="drag-handle">⋮⋮</div>
          <div class="employee-name">{{ element.name }}</div>
          <div class="employee-score">{{ element.totalScore }}分</div>
        </div>
      </template>
    </draggable>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useScoreStore } from '../store/score';
// 修正导入语句
import Draggable from 'vuedraggable';

const store = useScoreStore();

const employeeList = computed({
  get: () => store.employees,
  set: (value) => store.reorderEmployees(value)
});

const currentEmployeeId = computed(() => store.currentEmployeeId);

function selectEmployee(id) {
  store.setCurrentEmployee(id);
}

function onDragEnd() {
  // 拖拽结束后的处理
}
</script>

<style scoped>
.employee-list {
  padding: 15px;
  height: 100%;
  overflow-y: auto;
}

.employee-item {
  display: flex;
  align-items: center;
  padding: 12px 15px;
  margin-bottom: 8px;
  border-radius: 4px;
  background-color: #f9f9f9;
  cursor: pointer;
  transition: all 0.3s ease;
}

.drag-handle {
  cursor: move;
  margin-right: 10px;
  color: #999;
}

.employee-item:hover {
  background-color: #e6f7ff;
  transform: translateY(-2px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.09);
}

.employee-item.selected {
  background-color: #1890ff;
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  animation: pulse 1s;
}

@keyframes pulse {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.05);
  }
  100% {
    transform: scale(1);
  }
}

.employee-name {
  flex: 1;
  font-weight: bold;
}

.employee-score {
  font-weight: bold;
  margin-left: 10px;
}

.ghost {
  opacity: 0.5;
  background: #c8ebfb;
}
</style>