<template>
  <div class="relation-view">
    <a-tabs v-model:activeKey="activeTabKey">
      <a-tab-pane key="leader" tab="按负责人查看">
        <div class="relation-cards">
          <a-card 
            v-for="leader in leaderList" 
            :key="leader" 
            :title="leader" 
            class="relation-card"
          >
            <template #extra>
              <a-tag color="blue">项目负责人</a-tag>
            </template>
            <div class="member-list">
              <h4>负责的组员：</h4>
              <div class="member-tags">
                <a-tag 
                  v-for="member in getMembersByLeader(leader)" 
                  :key="member"
                  color="green"
                >
                  {{ member }}
                </a-tag>
                <span v-if="getMembersByLeader(leader).length === 0">
                  无组员
                </span>
              </div>
            </div>
          </a-card>
        </div>
      </a-tab-pane>
      
      <a-tab-pane key="project" tab="按项目查看">
        <div class="relation-cards">
          <a-card 
            v-for="project in projectList" 
            :key="project" 
            :title="project" 
            class="relation-card"
          >
            <div class="role-section">
              <h4>负责人</h4>
              <div class="person-list">
                <a-tag 
                  v-for="leader in getLeadersByProject(project)" 
                  :key="leader"
                  color="blue"
                >
                  {{ leader }}
                </a-tag>
                <span v-if="getLeadersByProject(project).length === 0">
                  无负责人
                </span>
              </div>
            </div>
            <div class="role-section">
              <h4>组员</h4>
              <div class="person-list">
                <a-tag 
                  v-for="member in getMembersByProject(project)" 
                  :key="member"
                  color="green"
                >
                  {{ member }}
                </a-tag>
                <span v-if="getMembersByProject(project).length === 0">
                  无组员
                </span>
              </div>
            </div>
          </a-card>
        </div>
      </a-tab-pane>
    </a-tabs>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRelationStore } from '../../store/relation';

const store = useRelationStore();
const activeTabKey = ref('leader');

const personnelData = computed(() => store.personnelData);
const projectList = computed(() => store.projectList);
const leaderList = computed(() => store.leaderList);

// 根据负责人获取组员
const getMembersByLeader = (leaderName) => {
  return personnelData.value
    .filter(person => 
      person.role === '项目组员' && 
      person.leaderNames.includes(leaderName)
    )
    .map(person => person.memberName);
};

// 根据项目获取负责人
const getLeadersByProject = (project) => {
  return personnelData.value
    .filter(person => 
      person.role === '项目负责人' && 
      person.projects.includes(project)
    )
    .map(person => person.memberName);
};

// 根据项目获取组员
const getMembersByProject = (project) => {
  return personnelData.value
    .filter(person => 
      person.role === '项目组员' && 
      person.projects.includes(project)
    )
    .map(person => person.memberName);
};
</script>

<style scoped>
.relation-view {
  padding: 15px;
  height: 100%;
}

.relation-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 16px;
  margin-top: 16px;
}

.relation-card {
  margin-bottom: 16px;
}

.member-list, .role-section {
  margin-bottom: 12px;
}

.member-tags, .person-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 8px;
}

h4 {
  margin-bottom: 8px;
  color: #1890ff;
}
</style>