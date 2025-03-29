<template>
  <div class="header-bar">
    <div class="system-title">
      <router-link to="/" class="nav-link">
        [考核系统] <span class="month-highlight">{{ previousMonthName }}月</span>月度绩效
      </router-link>
      <span class="separator">|</span>
      <router-link to="/relation" class="nav-link">
        人员关系管理
      </router-link>
    </div>
    <div class="user-info">
      <span class="user-name">{{ userName }}</span>
      <span class="separator">|</span>
      <span class="user-ip">{{ userIP }}</span>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useScoreStore } from '../store/score';
import { useRoute } from 'vue-router';

const store = useScoreStore();
const route = useRoute();

const userName = computed(() => store.userName);
const userIP = computed(() => store.userIP);
const previousMonthName = computed(() => store.previousMonth + 1);
</script>

<style scoped>
.header-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  background-color: #f0f2f5;
  border-bottom: 1px solid #e8e8e8;
}

.system-title {
  font-size: 18px;
  font-weight: bold;
  display: flex;
  align-items: center;
}

.month-highlight {
  color: #1890ff;
  font-weight: bold;
}

.user-info {
  display: flex;
  align-items: center;
}

.user-name {
  font-weight: bold;
  font-size: 16px;
}

.separator {
  margin: 0 10px;
  color: #d9d9d9;
}

.user-ip {
  color: #666;
  font-size: 14px;
}

.nav-link {
  text-decoration: none;
  color: inherit;
}

.nav-link:hover {
  color: #1890ff;
}
</style>