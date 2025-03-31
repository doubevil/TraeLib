import axios from 'axios';

// 设置API基础URL
const API_URL = 'http://localhost:8000/api';

export const relationApi = {
  // 获取指定日期的人员关系数据
  getRelationsByDate(date) {
    return axios.get(`${API_URL}/relations/`, {
      params: { date }
    });
  },
  
  // 导入人员关系数据
  importRelations(data) {
    return axios.post(`${API_URL}/relations/import/`, data);
  },
  
  // 修改人员角色和属性
  updateRelation(id, data) {
    return axios.patch(`${API_URL}/relations/${id}/`, data);
  },
  
  // 获取统计数据
  getStatistics(date) {
    return axios.get(`${API_URL}/relations/statistics/`, {
      params: { date }
    });
  },
  
  // 保存关系数据
  saveRelations(date, relations) {
    return axios.post(`${API_URL}/relations/save/`, {
      date,
      relations
    });
  }
};

// 假设这是 api/relation.js 文件的部分内容

// 获取关系数据
export const getRelations = async (date) => {
  try {
    const response = await axios.get(`/api/relations/?date=${date}`);
    return response.data;
  } catch (error) {
    console.error('获取关系数据失败:', error);
    throw error;
  }
};