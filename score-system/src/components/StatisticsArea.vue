<template>
  <div class="statistics-area" v-if="showStatistics">
    <h3>分数统计</h3>
    <div class="statistics-grid">
      <div class="stat-item">
        <div class="stat-title">40分以下</div>
        <div class="stat-count">{{ statistics.below40.length }}人</div>
        <div class="stat-names">{{ getNames(statistics.below40) }}</div>
      </div>
      <div class="stat-item">
        <div class="stat-title">40~50分</div>
        <div class="stat-count">{{ statistics['40to50'].length }}人</div>
        <div class="stat-names">{{ getNames(statistics['40to50']) }}</div>
      </div>
      <div class="stat-item">
        <div class="stat-title">50~60分</div>
        <div class="stat-count">{{ statistics['50to60'].length }}人</div>
        <div class="stat-names">{{ getNames(statistics['50to60']) }}</div>
      </div>
      <div class="stat-item">
        <div class="stat-title">60~70分</div>
        <div class="stat-count">{{ statistics['60to70'].length }}人</div>
        <div class="stat-names">{{ getNames(statistics['60to70']) }}</div>
      </div>
      <div class="stat-item">
        <div class="stat-title">70~80分</div>
        <div class="stat-count">{{ statistics['70to80'].length }}人</div>
        <div class="stat-names">{{ getNames(statistics['70to80']) }}</div>
      </div>
      <div class="stat-item">
        <div class="stat-title">80~90分</div>
        <div class="stat-count">{{ statistics['80to90'].length }}人</div>
        <div class="stat-names">{{ getNames(statistics['80to90']) }}</div>
      </div>
      <div class="stat-item">
        <div class="stat-title">90分以上</div>
        <div class="stat-count">{{ statistics.above90.length }}人</div>
        <div class="stat-names">{{ getNames(statistics.above90) }}</div>
      </div>
    </div>
    <div class="shortcut-hint">
      按 Ctrl+Shift+Alt+F10 隐藏统计区域
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useScoreStore } from '../store/score';

const store = useScoreStore();

const showStatistics = computed(() => store.showStatistics);
const statistics = computed(() => store.scoreStatistics);

function getNames(employees) {
  return employees.map(emp => emp.name).join(', ');
}
</script>

<style scoped>
.statistics-area {
  padding: 15px;
  background-color: #f0f2f5;
  border-top: 1px solid #e8e8e8;
}

.statistics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 15px;
  margin-top: 10px;
}

.stat-item {
  background-color: white;
  padding: 10px;
  border-radius: 4px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.stat-title {
  font-weight: bold;
  margin-bottom: 5px;
}

.stat-count {
  font-size: 18px;
  color: #1890ff;
  margin-bottom: 5px;
}

.stat-names {
  font-size: 12px;
  color: #666;
}

.shortcut-hint {
  text-align: center;
  margin-top: 10px;
  color: #999;
  font-size: 12px;
}
</style>