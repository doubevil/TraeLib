// 接收员工数据并计算统计信息
self.onmessage = function(e) {
  const employees = e.data;
  
  const stats = {
    'below40': [],
    '40to50': [],
    '50to60': [],
    '60to70': [],
    '70to80': [],
    '80to90': [],
    'above90': []
  };
  
  employees.forEach(emp => {
    if (emp.totalScore < 40) stats.below40.push(emp.id);
    else if (emp.totalScore < 50) stats['40to50'].push(emp.id);
    else if (emp.totalScore < 60) stats['50to60'].push(emp.id);
    else if (emp.totalScore < 70) stats['60to70'].push(emp.id);
    else if (emp.totalScore < 80) stats['70to80'].push(emp.id);
    else if (emp.totalScore < 90) stats['80to90'].push(emp.id);
    else stats.above90.push(emp.id);
  });
  
  self.postMessage(stats);
};