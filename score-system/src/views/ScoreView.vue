<template>
  <div class="score-system">
    <header-bar />
    
    <div class="main-content">
      <div class="sidebar">
        <employee-list />
      </div>
      <div class="content">
        <score-detail />
      </div>
    </div>
    
    <!-- 移除按钮控制，仅通过快捷键控制 -->
    <statistics-area />
  </div>
</template>

<script setup>
import { computed, onMounted, onUnmounted } from 'vue';
import { useScoreStore } from '../store/score';
import HeaderBar from '../components/HeaderBar.vue';
import EmployeeList from '../components/EmployeeList.vue';
import ScoreDetail from '../components/ScoreDetail.vue';
import StatisticsArea from '../components/StatisticsArea.vue';

const store = useScoreStore();

// 添加键盘快捷键监听
function handleKeyDown(event) {
  // 检测 Ctrl+Shift+Alt+F10 组合键
  if (event.ctrlKey && event.shiftKey && event.altKey && event.key === 'F10') {
    store.toggleStatistics();
  }
}

onMounted(() => {
  window.addEventListener('keydown', handleKeyDown);
});

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeyDown);
});
</script>

<style scoped>
.score-system {
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
  flex: 1;
  overflow: hidden;
}

.sidebar {
  width: 250px;
  min-width: 250px; /* 确保最小宽度 */
  border-right: 1px solid #e8e8e8;
  background-color: #f9f9f9;
}

.content {
  flex: 1;
  overflow: auto;
}

@media (max-width: 768px) {
  .main-content {
    flex-direction: column;
  }
  
  .sidebar {
    width: 100%;
    min-height: 200px;
    border-right: none;
    border-bottom: 1px solid #e8e8e8;
  }
}
</style>