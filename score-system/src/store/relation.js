import { defineStore } from 'pinia';
import { relationApi } from '../api/relation';
import { message } from 'ant-design-vue';

export const useRelationStore = defineStore('relation', {
  state: () => ({
    relations: [],
    currentDate: '',
    isDataImported: false,
    loading: false,
    projectLeaderCount: 0,
    projectMemberCount: 0,
    freePersonCount: 0
  }),
  
  actions: {
    // 获取指定日期的人员关系数据
    async fetchRelationsByDate(date) {
      this.loading = true;
      try {
        const response = await relationApi.getRelationsByDate(date);
        console.log('获取到的数据:', response.data);
        
        // 修改这里：检查 response.data 是否有 results 字段
        const relationData = response.data.results || response.data;
        
        // 确保数据是数组
        this.relations = Array.isArray(relationData) ? relationData : [];
        this.currentDate = date;
        this.isDataImported = this.relations.length > 0;
        
        // 更新统计数据
        this.fetchStatistics(date);
        
        // 如果没有数据，显示提示
        if (this.relations.length === 0) {
          message.info(`${date}没有人员关系数据`);
        }
        
        return this.relations;
      } catch (error) {
        console.error('获取人员关系数据失败:', error);
        message.error('获取人员关系数据失败');
        return [];
      } finally {
        this.loading = false;
      }
    },
  
    // 获取统计数据
    async fetchStatistics(date) {
      try {
        const response = await relationApi.getStatistics(date);
        console.log('获取到的统计数据:', response.data);
        this.projectLeaderCount = response.data.project_leader_count;
        this.projectMemberCount = response.data.project_member_count;
        this.freePersonCount = response.data.free_person_count;
        return response.data;
      } catch (error) {
        console.error('获取统计数据失败:', error);
        return null;
      }
    },
  }
});

// 处理关系数据的辅助函数
export const processRelationData = (data) => {
  return data.map(item => ({
    employee_name: item.employee_name,
    leaders: item.leaders || '',
    project_names: item.project_names || [],
    role: item.role,
    // ...其他字段
  }));
};

// 获取角色的显示名称
export const getRoleDisplayName = (role) => {
  const roleMap = {
    'project_leader': '项目负责人',
    'project_member': '项目组员',
    'free_person': '自由人',
  };
  return roleMap[role] || role;
};
