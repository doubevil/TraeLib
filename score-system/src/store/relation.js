import { defineStore } from 'pinia'

// 模拟从外部系统导入的数据
const mockImportData = {
  '202303': [
    {
      date: '202303',
      memberName: '张三',
      leaderNames: ['李四', '王五'],
      leaderCount: 2,
      projects: ['项目1', '项目2', '项目3', '项目4'],
      role: '项目组员',
      attributes: ['技术开发', '项目管理', '测试', '设计']
    },
    {
      date: '202303',
      memberName: '李四',
      leaderNames: ['李四'],
      leaderCount: 1,
      projects: ['项目1'],
      role: '项目负责人',
      attributes: ['技术开发', '项目管理', '测试', '设计']
    },
    {
      date: '202303',
      memberName: '王五',
      leaderNames: ['王五'],
      leaderCount: 1,
      projects: ['项目2'],
      role: '项目负责人',
      attributes: ['项目管理', '测试']
    },
    {
      date: '202303',
      memberName: '赵六',
      leaderNames: ['李四', '王五'],
      leaderCount: 2,
      projects: ['项目1', '项目2'],
      role: '项目组员',
      attributes: ['技术开发', '测试']
    },
    {
      date: '202303',
      memberName: '钱七',
      leaderNames: [],
      leaderCount: 0,
      projects: [],
      role: '自由人',
      attributes: ['设计', '市场']
    }
  ],
  '202302': [
    {
      date: '202302',
      memberName: '张三',
      leaderNames: ['李四'],
      leaderCount: 1,
      projects: ['项目1', '项目2'],
      role: '项目组员',
      attributes: ['技术开发', '测试']
    },
    {
      date: '202302',
      memberName: '李四',
      leaderNames: ['李四'],
      leaderCount: 1,
      projects: ['项目1'],
      role: '项目负责人',
      attributes: ['技术开发', '项目管理']
    },
    {
      date: '202302',
      memberName: '王五',
      leaderNames: ['王五'],
      leaderCount: 1,
      projects: ['项目2'],
      role: '项目负责人',
      attributes: ['项目管理', '测试']
    }
  ]
}

export const useRelationStore = defineStore('relation', {
  state: () => ({
    personnelData: [],
    availableDates: Object.keys(mockImportData).sort().reverse(),
    currentDate: '',
    userName: '管理员',
    userIP: '192.168.1.1',
    isDataImported: false,
    roleOptions: ['项目组员', '项目负责人', '自由人'],
    attributeOptions: ['技术开发', '项目管理', '测试', '设计', '运营', '市场', '其他'],
    roleRanking: {
      '项目负责人': 2,
      '项目组员': 1,
      '自由人': 0
    }
  }),
  getters: {
    projectLeaderCount: (state) => {
      return state.personnelData.filter(person => person.role === '项目负责人').length
    },
    projectMemberCount: (state) => {
      return state.personnelData.filter(person => person.role === '项目组员').length
    },
    freePersonCount: (state) => {
      return state.personnelData.filter(person => person.role === '自由人').length
    },
    projectList: (state) => {
      const projects = new Set()
      state.personnelData.forEach(person => {
        person.projects.forEach(project => projects.add(project))
      })
      return Array.from(projects)
    },
    leaderList: (state) => {
      const leaders = new Set()
      state.personnelData.forEach(person => {
        if (person.role === '项目负责人') {
          leaders.add(person.memberName)
        }
      })
      return Array.from(leaders)
    }
  },
  actions: {
    importData(date = '') {
      // 如果没有指定日期，使用最新的日期
      const targetDate = date || this.availableDates[0]
      
      if (mockImportData[targetDate]) {
        this.personnelData = JSON.parse(JSON.stringify(mockImportData[targetDate]))
        this.currentDate = targetDate
        this.isDataImported = true
        return Promise.resolve(true)
      } else {
        return Promise.reject(new Error(`没有找到 ${targetDate} 的数据`))
      }
    },
    updatePersonRole(personName, newRole) {
      const person = this.personnelData.find(p => p.memberName === personName)
      if (!person) return
      
      const oldRole = person.role
      
      // 检查角色变更是否符合规则（只能由高向低变更）
      if (this.roleRanking[oldRole] < this.roleRanking[newRole]) {
        return Promise.reject(new Error('角色只能由高向低变更'))
      }
      
      // 如果角色没有变化，直接返回
      if (oldRole === newRole) return Promise.resolve()
      
      // 处理从项目负责人变为项目组员的情况
      if (oldRole === '项目负责人' && newRole === '项目组员') {
        // 1. 从本人的领导列表中移除自己
        const selfIndex = person.leaderNames.indexOf(personName)
        if (selfIndex !== -1) {
          person.leaderNames.splice(selfIndex, 1)
        }
        
        // 2. 如果没有其他领导，则设置为自由人
        if (person.leaderNames.length === 0) {
          person.role = '自由人'
          person.leaderCount = 0
        } else {
          person.role = newRole
          person.leaderCount = person.leaderNames.length
        }
        
        // 3. 从其他人的领导列表中移除此人
        this.personnelData.forEach(p => {
          if (p.memberName !== personName) {
            const leaderIndex = p.leaderNames.indexOf(personName)
            if (leaderIndex !== -1) {
              p.leaderNames.splice(leaderIndex, 1)
              p.leaderCount = p.leaderNames.length
              
              // 如果没有其他领导，则设置为自由人
              if (p.leaderNames.length === 0 && p.role === '项目组员') {
                p.role = '自由人'
              }
            }
          }
        })
      }
      
      // 处理从项目负责人变为自由人的情况
      else if (oldRole === '项目负责人' && newRole === '自由人') {
        // 1. 设置角色为自由人
        person.role = newRole
        
        // 2. 从其他人的领导列表中移除此人
        this.personnelData.forEach(p => {
          if (p.memberName !== personName) {
            const leaderIndex = p.leaderNames.indexOf(personName)
            if (leaderIndex !== -1) {
              p.leaderNames.splice(leaderIndex, 1)
              p.leaderCount = p.leaderNames.length
              
              // 如果没有其他领导，则设置为自由人
              if (p.leaderNames.length === 0 && p.role === '项目组员') {
                p.role = '自由人'
              }
            }
          }
        })
      }
      
      // 处理从项目组员变为自由人的情况
      else if (oldRole === '项目组员' && newRole === '自由人') {
        // 简单地更新角色
        person.role = newRole
      }
      
      return Promise.resolve()
    },
    updatePersonAttributes(personName, attributes) {
      const person = this.personnelData.find(p => p.memberName === personName)
      if (person) {
        person.attributes = [...attributes]
        return Promise.resolve()
      }
      return Promise.reject(new Error(`未找到人员: ${personName}`))
    },
    saveChanges() {
      // 在实际应用中，这里会发送请求到后端保存数据
      console.log('保存数据', this.personnelData)
      return Promise.resolve()
    }
  }
})