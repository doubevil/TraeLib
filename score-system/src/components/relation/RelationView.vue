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
      
      <a-tab-pane key="chart" tab="关系图表">
        <div class="relation-chart" ref="chartContainer"></div>
      </a-tab-pane>
    </a-tabs>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useRelationStore } from '../../store/relation';
import * as echarts from 'echarts';

const store = useRelationStore();
const activeTabKey = ref('leader');
const chartContainer = ref(null);
const chart = ref(null);

const personnelData = computed(() => store.personnelData);
const projectList = computed(() => store.projectList);
const leaderList = computed(() => store.leaderList);
const relations = computed(() => store.relations);

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

// 初始化图表
const initChart = () => {
  if (!chartContainer.value) return;
  
  chart.value = echarts.init(chartContainer.value);
  updateChart();
  
  // 监听窗口大小变化
  window.addEventListener('resize', () => {
    chart.value && chart.value.resize();
  });
};

// 更新图表数据
const updateChart = () => {
  if (!chart.value) return;
  
  // 处理数据
  const nodes = [];
  const links = [];
  const nodeMap = new Map();
  
  // 添加员工节点
  relations.value.forEach(relation => {
    // 添加组员节点
    if (!nodeMap.has(relation.employee_name)) {
      const category = getCategoryByRole(relation.role);
      nodes.push({
        id: relation.employee_name,
        name: relation.employee_name,
        symbolSize: 30,
        category: category,
        value: relation.project_names.length
      });
      nodeMap.set(relation.employee_name, true);
    }
    
    // 添加项目负责人节点和连接
    relation.leaders_info.forEach(leader => {
      if (!nodeMap.has(leader.name)) {
        nodes.push({
          id: leader.name,
          name: leader.name,
          symbolSize: 40,
          category: 0, // 项目负责人
          value: 1
        });
        nodeMap.set(leader.name, true);
      }
      
      // 添加连接
      links.push({
        source: leader.name,
        target: relation.employee_name,
        value: 1
      });
    });
  });
  
  // 设置图表选项
  const option = {
    title: {
      text: '人员关系图',
      subtext: '项目负责人与组员关系',
      top: 'top',
      left: 'center'
    },
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c}'
    },
    legend: {
      data: ['项目负责人', '项目组员', '自由人'],
      bottom: 10
    },
    series: [
      {
        type: 'graph',
        layout: 'force',
        data: nodes,
        links: links,
        categories: [
          { name: '项目负责人' },
          { name: '项目组员' },
          { name: '自由人' }
        ],
        roam: true,
        label: {
          show: true,
          position: 'right'
        },
        force: {
          repulsion: 100,
          edgeLength: 80
        },
        emphasis: {
          focus: 'adjacency',
          lineStyle: {
            width: 4
          }
        }
      }
    ]
  };
  
  chart.value.setOption(option);
};

// 根据角色获取分类
const getCategoryByRole = (role) => {
  switch (role) {
    case 'project_leader':
      return 0;
    case 'project_member':
      return 1;
    case 'free_person':
      return 2;
    default:
      return 1;
  }
};

// 监听数据变化
watch(() => relations.value, () => {
  updateChart();
}, { deep: true });

// 监听标签页变化，当切换到图表标签页时初始化图表
watch(() => activeTabKey.value, (newValue) => {
  if (newValue === 'chart') {
    setTimeout(() => {
      initChart();
    }, 100);
  }
});

// 组件挂载后初始化图表
onMounted(() => {
  if (activeTabKey.value === 'chart') {
    initChart();
  }
});
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

.relation-chart {
  width: 100%;
  height: 100%;
  min-height: 500px;
}
</style>