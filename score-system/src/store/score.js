// 只需修改以下部分
import { defineStore } from 'pinia'
import { scoreCategories } from '../scoreCategories'

export const useScoreStore = defineStore('score', {
  state: () => ({
    currentMonth: new Date().getMonth(),
    previousMonth: new Date().getMonth() === 0 ? 11 : new Date().getMonth() - 1,
    currentYear: new Date().getFullYear(),
    previousYear: new Date().getMonth() === 0 ? new Date().getFullYear() - 1 : new Date().getFullYear(),
    userName: '管理员',
    userIP: '192.168.1.1',
    employees: [
      { id: 1, name: '张三', totalScore: 85, comment: '', scores: {} },
      { id: 2, name: '李四', totalScore: 76, comment: '', scores: {} },
      { id: 3, name: '王五', totalScore: 92, comment: '', scores: {} },
      { id: 4, name: '赵六', totalScore: 65, comment: '', scores: {} },
      { id: 5, name: '钱七', totalScore: 78, comment: '', scores: {} },
    ],
    currentEmployeeId: 1,
    // 使用 scoreCategories 数据
    scoreItems: processScoreCategories(scoreCategories),
    showStatistics: false
  }),
  getters: {
    currentEmployee: (state) => {
      return state.employees.find(emp => emp.id === state.currentEmployeeId) || state.employees[0];
    },
    scoreStatistics: (state) => {
      const stats = {
        'below40': [],
        '40to50': [],
        '50to60': [],
        '60to70': [],
        '70to80': [],
        '80to90': [],
        'above90': []
      };
      
      state.employees.forEach(emp => {
        if (emp.totalScore < 40) stats.below40.push(emp);
        else if (emp.totalScore < 50) stats['40to50'].push(emp);
        else if (emp.totalScore < 60) stats['50to60'].push(emp);
        else if (emp.totalScore < 70) stats['60to70'].push(emp);
        else if (emp.totalScore < 80) stats['70to80'].push(emp);
        else if (emp.totalScore < 90) stats['80to90'].push(emp);
        else stats.above90.push(emp);
      });
      
      return stats;
    }
  },
  actions: {
    setCurrentEmployee(id) {
      this.currentEmployeeId = id;
    },
    // 修改 updateEmployeeScore 方法，确保在初始化时使用基础分
    updateEmployeeScore(employeeId, itemId, score) {
      const employee = this.employees.find(emp => emp.id === employeeId);
      if (employee) {
        if (!employee.scores) {
          employee.scores = {};
        }
        employee.scores[itemId] = score;
        this.recalculateTotalScore(employeeId);
      }
    },
    updateEmployeeComment(employeeId, comment) {
      const employee = this.employees.find(emp => emp.id === employeeId);
      if (employee) {
        employee.comment = comment;
      }
    },
    recalculateTotalScore(employeeId) {
      const employee = this.employees.find(emp => emp.id === employeeId);
      if (employee) {
        let total = 0;
        for (const itemId in employee.scores) {
          total += employee.scores[itemId];
        }
        employee.totalScore = Math.max(0, Math.min(100, total));
      }
    },
    toggleStatistics() {
      this.showStatistics = !this.showStatistics;
    },
    nextEmployee() {
      const currentIndex = this.employees.findIndex(emp => emp.id === this.currentEmployeeId);
      if (currentIndex < this.employees.length - 1) {
        this.currentEmployeeId = this.employees[currentIndex + 1].id;
      }
    },
    previousEmployee() {
      const currentIndex = this.employees.findIndex(emp => emp.id === this.currentEmployeeId);
      if (currentIndex > 0) {
        this.currentEmployeeId = this.employees[currentIndex - 1].id;
      }
    },
    reorderEmployees(newOrder) {
      this.employees = newOrder;
    }
  }
})

// 处理 scoreCategories 数据，转换为组件需要的格式
// 只修改 processScoreCategories 函数部分
function processScoreCategories(categories) {
  // 按 title 分组
  const groupedByTitle = categories.reduce((acc, item) => {
    if (!acc[item.title]) {
      acc[item.title] = [];
    }
    acc[item.title].push(item);
    return acc;
  }, {});

  // 转换为组件需要的格式
  return Object.keys(groupedByTitle).map(title => {
    return {
      category: title,
      items: groupedByTitle[title].map(item => ({
        id: item.id,
        name: item.cot,
        description: item.cotdtl,
        score: item.deft, // 基础分
        type: title.includes('减分项') ? 'negative' : (title.includes('加分项') ? 'positive' : 'normal'),
        max: item.max,
        min: item.min
      }))
    };
  });
}