<template>
  <div class="score-detail">
    <div class="score-items-container">
      <div class="score-items">
        <!-- 左侧列：显示较小序号的项点 -->
        <div class="score-column left-column">
          <div v-for="category in leftCategories" :key="category.category" class="score-category">
            <h3>{{ category.category }}</h3>
            <div class="score-item-list">
              <div 
                v-for="item in category.items" 
                :key="item.id" 
                class="score-item"
                :class="{
                  'negative': category.category.includes('减分项'),
                  'positive': category.category.includes('加分项'),
                  'normal': !category.category.includes('减分项') && !category.category.includes('加分项')
                }"
              >
                <div class="item-number">{{ item.id }}</div>
                <div class="item-name" @mouseenter="showTooltip(item)" @mouseleave="hideTooltip">
                  {{ item.name }}
                  <a-tooltip v-if="activeTooltip === item.id" :title="item.description" placement="right">
                    <info-circle-outlined />
                  </a-tooltip>
                </div>
                <div class="item-score">
                  <a-input-number 
                    v-model:value="employeeScores[item.id]" 
                    :min="item.min" 
                    :max="item.max"
                    :placeholder="item.score"
                    @change="updateScore(item.id, $event)"
                    size="small"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 右侧列：显示较大序号的项点 -->
        <div class="score-column right-column">
          <div v-for="category in rightCategories" :key="category.category" class="score-category">
            <h3>{{ category.category }}</h3>
            <div class="score-item-list">
              <div 
                v-for="item in category.items" 
                :key="item.id" 
                class="score-item"
                :class="{
                  'negative': category.category.includes('减分项'),
                  'positive': category.category.includes('加分项'),
                  'normal': !category.category.includes('减分项') && !category.category.includes('加分项')
                }"
              >
                <div class="item-number">{{ item.id }}</div>
                <div class="item-name" @mouseenter="showTooltip(item)" @mouseleave="hideTooltip">
                  {{ item.name }}
                  <a-tooltip v-if="activeTooltip === item.id" :title="item.description" placement="right">
                    <info-circle-outlined />
                  </a-tooltip>
                </div>
                <div class="item-score">
                  <a-input-number 
                    v-model:value="employeeScores[item.id]" 
                    :min="item.min" 
                    :max="item.max"
                    :placeholder="item.score"
                    @change="updateScore(item.id, $event)"
                    size="small"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 保留评价部分和按钮不变 -->
    <div class="comment-section">
      <h3>评价</h3>
      <a-textarea 
        v-model:value="comment" 
        :rows="4" 
        placeholder="请输入评价内容（不超过200字）" 
        :maxlength="200"
        show-count
        @change="updateComment"
      />
    </div>
    
    <div class="action-buttons">
      <a-button 
        type="primary" 
        @click="previousEmployee" 
        :disabled="!hasPrevious"
      >
        ← 上一个员工
      </a-button>
      <a-button 
        type="primary" 
        @click="saveScore"
        :disabled="!isCommentValid"
      >
        保存评分
      </a-button>
      <a-button 
        type="primary" 
        @click="nextEmployee" 
        :disabled="!hasNext"
      >
        下一个员工 →
      </a-button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue';
import { useScoreStore } from '../store/score';
import { InfoCircleOutlined } from '@ant-design/icons-vue';
import { message } from 'ant-design-vue';

const store = useScoreStore();
const activeTooltip = ref(null);
const employeeScores = ref({});
const comment = ref('');

const scoreItems = computed(() => store.scoreItems);
const currentEmployee = computed(() => store.currentEmployee);

// 将项点分为左右两列，左侧小序号，右侧大序号
const leftCategories = computed(() => {
  const allCategories = [...scoreItems.value];
  const midPoint = Math.ceil(getTotalItemsCount(allCategories) / 2);
  
  let count = 0;
  const leftCats = [];
  
  for (const category of allCategories) {
    const itemsCount = category.items.length;
    if (count + itemsCount <= midPoint) {
      leftCats.push(category);
      count += itemsCount;
    } else {
      // 需要拆分这个分类
      const leftItems = [];
      const rightItems = [];
      
      for (let i = 0; i < category.items.length; i++) {
        if (count < midPoint) {
          leftItems.push(category.items[i]);
          count++;
        } else {
          rightItems.push(category.items[i]);
        }
      }
      
      if (leftItems.length > 0) {
        leftCats.push({
          ...category,
          items: leftItems
        });
      }
      
      break;
    }
  }
  
  return leftCats;
});

const rightCategories = computed(() => {
  const allCategories = [...scoreItems.value];
  const midPoint = Math.ceil(getTotalItemsCount(allCategories) / 2);
  
  let count = 0;
  const rightCats = [];
  let startAdding = false;
  
  for (const category of allCategories) {
    const itemsCount = category.items.length;
    
    if (startAdding) {
      rightCats.push(category);
      continue;
    }
    
    if (count + itemsCount <= midPoint) {
      count += itemsCount;
    } else {
      // 需要拆分这个分类
      const leftItems = [];
      const rightItems = [];
      
      for (let i = 0; i < category.items.length; i++) {
        if (count < midPoint) {
          leftItems.push(category.items[i]);
          count++;
        } else {
          rightItems.push(category.items[i]);
        }
      }
      
      if (rightItems.length > 0) {
        rightCats.push({
          ...category,
          items: rightItems
        });
      }
      
      startAdding = true;
    }
  }
  
  return rightCats;
});

function getTotalItemsCount(categories) {
  return categories.reduce((sum, category) => sum + category.items.length, 0);
}

// 初始化员工分数，使用基础分作为默认值
function initEmployeeScores() {
  const scores = {};
  scoreItems.value.forEach(category => {
    category.items.forEach(item => {
      if (!employeeScores.value[item.id]) {
        scores[item.id] = item.score;
      } else {
        scores[item.id] = employeeScores.value[item.id];
      }
    });
  });
  employeeScores.value = scores;
}

const hasPrevious = computed(() => {
  const currentIndex = store.employees.findIndex(emp => emp.id === store.currentEmployeeId);
  return currentIndex > 0;
});

const hasNext = computed(() => {
  const currentIndex = store.employees.findIndex(emp => emp.id === store.currentEmployeeId);
  return currentIndex < store.employees.length - 1;
});

const isCommentValid = computed(() => {
  return comment.value.length > 0 && comment.value.length <= 200;
});

watch(currentEmployee, (newEmployee) => {
  // 当选中的员工变化时，更新分数和评论
  employeeScores.value = { ...newEmployee.scores };
  comment.value = newEmployee.comment || '';
  // 初始化未设置的分数为基础分
  initEmployeeScores();
}, { immediate: true });

function showTooltip(item) {
  activeTooltip.value = item.id;
}

function hideTooltip() {
  activeTooltip.value = null;
}

function updateScore(itemId, value) {
  employeeScores.value[itemId] = value;
  store.updateEmployeeScore(currentEmployee.value.id, itemId, value);
}

function updateComment() {
  store.updateEmployeeComment(currentEmployee.value.id, comment.value);
}

function saveScore() {
  if (!isCommentValid.value) {
    message.error('评价内容不能为空且不能超过200字');
    return;
  }
  
  // 保存当前评分
  for (const itemId in employeeScores.value) {
    store.updateEmployeeScore(currentEmployee.value.id, itemId, employeeScores.value[itemId]);
  }
  store.updateEmployeeComment(currentEmployee.value.id, comment.value);
  
  message.success('评分保存成功');
}

function previousEmployee() {
  store.previousEmployee();
}

function nextEmployee() {
  store.nextEmployee();
}
</script>

<style scoped>
.score-detail {
  padding: 15px;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.score-items-container {
  flex: 1;
  margin-bottom: 15px;
}

.score-items {
  display: flex;
  height: 100%;
}

.score-column {
  flex: 1;
  padding: 0 5px;
}

.left-column {
  border-right: 1px dashed #e8e8e8;
}

.score-category {
  margin-bottom: 15px;
}

.score-category h3 {
  margin-bottom: 8px;
  padding-bottom: 5px;
  border-bottom: 1px solid #e8e8e8;
  font-size: 14px;
}

.score-item-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.score-item {
  display: flex;
  align-items: center;
  padding: 6px;
  border-radius: 4px;
  transition: all 0.3s ease;
  font-size: 12px;
}

/* 颜色区分 */
.score-item.normal {
  background-color: #f9f9f9;
  border-left: 3px solid #1890ff;
}

.score-item.negative {
  background-color: #fff1f0;
  border-left: 3px solid #ff4d4f;
}

.score-item.positive {
  background-color: #f6ffed;
  border-left: 3px solid #52c41a;
}

.item-number {
  width: 24px;
  text-align: center;
  font-weight: bold;
  flex-shrink: 0;
}

.item-name {
  flex: 1;
  margin: 0 5px;
  display: flex;
  align-items: center;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.item-score {
  width: 60px;
  flex-shrink: 0;
}

/* 减小 a-input-number 组件的宽度 */
:deep(.ant-input-number) {
  width: 55px !important;
}

.comment-section {
  margin: 10px 0;
  max-height: 150px;
}

.action-buttons {
  display: flex;
  justify-content: space-between;
  margin-top: 10px;
}

/* 响应式布局 */
@media (max-width: 768px) {
  .score-items {
    flex-direction: column;
  }
  
  .left-column {
    border-right: none;
    border-bottom: 1px dashed #e8e8e8;
    margin-bottom: 10px;
  }
}
</style>