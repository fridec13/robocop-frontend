<template>
  <div class="task-progress">
    <div class="header">
      <h2>작업 진척도</h2>
      <div class="filters">
        <select v-model="selectedRobot" class="filter-select">
          <option value="">전체 로봇</option>
          <option v-for="robot in robots" :key="robot.id" :value="robot.id">
            {{ robot.name }}
          </option>
        </select>
        <select v-model="selectedPeriod" class="filter-select">
          <option value="day">일간</option>
          <option value="week">주간</option>
          <option value="month">월간</option>
        </select>
      </div>
    </div>

    <!-- 전체 진행률 -->
    <div class="overall-progress">
      <div class="progress-info">
        <h3>전체 진행률</h3>
        <span class="percentage">{{ overallProgress }}%</span>
      </div>
      <div class="progress-bar">
        <div class="progress" :style="{ width: overallProgress + '%' }"></div>
      </div>
      <div class="progress-stats">
        <div class="stat-item">
          <span class="label">완료</span>
          <span class="value">{{ completedTasks }}건</span>
        </div>
        <div class="stat-item">
          <span class="label">진행 중</span>
          <span class="value">{{ inProgressTasks }}건</span>
        </div>
        <div class="stat-item">
          <span class="label">대기</span>
          <span class="value">{{ pendingTasks }}건</span>
        </div>
      </div>
    </div>

    <!-- 작업 목록 -->
    <div class="task-list">
      <div v-for="task in filteredTasks" 
           :key="task.id" 
           class="task-item"
           :class="{ 'high-priority': task.priority === 'high' }">
        <div class="task-header">
          <div class="task-title">
            <span class="task-id">#{{ task.id }}</span>
            {{ task.title }}
          </div>
          <div class="task-meta">
            <span class="robot-name">{{ task.robotName }}</span>
            <span class="task-type" :class="task.type">{{ getTaskTypeLabel(task.type) }}</span>
          </div>
        </div>
        
        <div class="task-progress-bar">
          <div class="progress" :style="{ width: task.progress + '%' }"></div>
          <span class="progress-text">{{ task.progress }}%</span>
        </div>
        
        <div class="task-details">
          <div class="detail-row">
            <span class="label">시작 시간</span>
            <span class="value">{{ formatDateTime(task.startTime) }}</span>
          </div>
          <div class="detail-row">
            <span class="label">예상 종료</span>
            <span class="value">{{ formatDateTime(task.expectedEndTime) }}</span>
          </div>
          <div class="detail-row">
            <span class="label">상태</span>
            <span class="status" :class="task.status">{{ getStatusLabel(task.status) }}</span>
          </div>
        </div>

        <div class="task-actions">
          <button v-if="task.status === 'pending'" 
                  class="action-btn start"
                  @click="startTask(task)">
            시작
          </button>
          <button v-else-if="task.status === 'in_progress'" 
                  class="action-btn complete"
                  @click="completeTask(task)">
            완료
          </button>
          <button v-if="task.status !== 'completed'" 
                  class="action-btn cancel"
                  @click="cancelTask(task)">
            취소
          </button>
        </div>
      </div>
    </div>

    <!-- 작업 없음 표시 -->
    <div v-if="filteredTasks.length === 0" class="no-tasks">
      작업이 없습니다.
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

// 필터 상태
const selectedRobot = ref('')
const selectedPeriod = ref('day')

// 로봇 목록
const robots = ref([
  { id: 'SSAFY-ROBO-1', name: 'Robot 1' },
  { id: 'SSAFY-ROBO-2', name: 'Robot 2' }
])

// 예시 작업 데이터
const tasks = ref([
  {
    id: 1,
    title: '1층 로비 순찰',
    type: 'patrol',
    robotName: 'Robot 1',
    progress: 75,
    priority: 'high',
    status: 'in_progress',
    startTime: new Date('2024-02-20T09:00:00'),
    expectedEndTime: new Date('2024-02-20T10:00:00')
  },
  {
    id: 2,
    title: '주차장 감시',
    type: 'surveillance',
    robotName: 'Robot 2',
    progress: 100,
    priority: 'medium',
    status: 'completed',
    startTime: new Date('2024-02-20T08:00:00'),
    expectedEndTime: new Date('2024-02-20T09:00:00')
  },
  {
    id: 3,
    title: '비상구 점검',
    type: 'inspection',
    robotName: 'Robot 1',
    progress: 0,
    priority: 'low',
    status: 'pending',
    startTime: new Date('2024-02-20T11:00:00'),
    expectedEndTime: new Date('2024-02-20T12:00:00')
  }
])

// 필터링된 작업 목록
const filteredTasks = computed(() => {
  return tasks.value.filter(task => {
    if (selectedRobot.value && task.robotName !== selectedRobot.value) return false
    // 기간 필터링 로직 추가 예정
    return true
  })
})

// 전체 진행률 계산
const overallProgress = computed(() => {
  const total = tasks.value.length
  if (total === 0) return 0
  const completed = tasks.value.reduce((sum, task) => sum + task.progress, 0)
  return Math.round(completed / total)
})

// 작업 상태별 개수
const completedTasks = computed(() => 
  tasks.value.filter(task => task.status === 'completed').length
)
const inProgressTasks = computed(() => 
  tasks.value.filter(task => task.status === 'in_progress').length
)
const pendingTasks = computed(() => 
  tasks.value.filter(task => task.status === 'pending').length
)

// 작업 타입 레이블
const getTaskTypeLabel = (type) => {
  const types = {
    patrol: '순찰',
    surveillance: '감시',
    inspection: '점검'
  }
  return types[type] || type
}

// 상태 레이블
const getStatusLabel = (status) => {
  const statuses = {
    pending: '대기',
    in_progress: '진행 중',
    completed: '완료',
    cancelled: '취소'
  }
  return statuses[status] || status
}

// 날짜 포맷
const formatDateTime = (date) => {
  return date.toLocaleString('ko-KR', {
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 작업 상태 변경
const startTask = (task) => {
  task.status = 'in_progress'
  task.progress = 0
  task.startTime = new Date()
}

const completeTask = (task) => {
  task.status = 'completed'
  task.progress = 100
}

const cancelTask = (task) => {
  if (confirm('작업을 취소하시겠습니까?')) {
    task.status = 'cancelled'
    task.progress = 0
  }
}
</script>

<style scoped>
.task-progress {
  padding: 1.5rem;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.filters {
  display: flex;
  gap: 1rem;
}

.filter-select {
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  min-width: 150px;
}

.overall-progress {
  background-color: white;
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 2rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.progress-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.percentage {
  font-size: 1.5rem;
  font-weight: 500;
  color: #007bff;
}

.progress-bar {
  height: 8px;
  background-color: #e9ecef;
  border-radius: 4px;
  margin-bottom: 1rem;
  overflow: hidden;
}

.progress-bar .progress {
  height: 100%;
  background-color: #007bff;
  transition: width 0.3s ease;
}

.progress-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
  text-align: center;
}

.stat-item {
  display: flex;
  flex-direction: column;
}

.stat-item .label {
  color: #666;
  font-size: 0.875rem;
}

.stat-item .value {
  font-size: 1.25rem;
  font-weight: 500;
  color: #333;
}

.task-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.task-item {
  background-color: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.task-item.high-priority {
  border-left: 4px solid #dc3545;
}

.task-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.task-title {
  font-weight: 500;
}

.task-id {
  color: #666;
  margin-right: 0.5rem;
}

.task-meta {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.robot-name {
  color: #666;
  font-size: 0.875rem;
}

.task-type {
  padding: 0.25rem 0.5rem;
  border-radius: 999px;
  font-size: 0.75rem;
  font-weight: 500;
}

.task-type.patrol {
  background-color: #007bff;
  color: white;
}

.task-type.surveillance {
  background-color: #ffc107;
  color: #000;
}

.task-type.inspection {
  background-color: #28a745;
  color: white;
}

.task-progress-bar {
  height: 4px;
  background-color: #e9ecef;
  border-radius: 2px;
  margin: 1rem 0;
  position: relative;
}

.task-progress-bar .progress {
  height: 100%;
  background-color: #007bff;
  border-radius: 2px;
  transition: width 0.3s ease;
}

.progress-text {
  position: absolute;
  right: 0;
  top: -1.5rem;
  font-size: 0.875rem;
  color: #666;
}

.task-details {
  margin: 1rem 0;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
}

.detail-row .label {
  color: #666;
  font-size: 0.875rem;
}

.status {
  padding: 0.25rem 0.5rem;
  border-radius: 999px;
  font-size: 0.75rem;
  font-weight: 500;
}

.status.pending {
  background-color: #f8f9fa;
  color: #666;
}

.status.in_progress {
  background-color: #007bff;
  color: white;
}

.status.completed {
  background-color: #28a745;
  color: white;
}

.status.cancelled {
  background-color: #dc3545;
  color: white;
}

.task-actions {
  display: flex;
  gap: 0.5rem;
  margin-top: 1rem;
}

.action-btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.875rem;
}

.action-btn.start {
  background-color: #007bff;
  color: white;
}

.action-btn.complete {
  background-color: #28a745;
  color: white;
}

.action-btn.cancel {
  background-color: #dc3545;
  color: white;
}

.no-tasks {
  text-align: center;
  padding: 3rem;
  color: #666;
  background-color: white;
  border-radius: 8px;
}

@media (max-width: 768px) {
  .header {
    flex-direction: column;
    gap: 1rem;
  }
  
  .filters {
    width: 100%;
    flex-direction: column;
  }
  
  .filter-select {
    width: 100%;
  }
  
  .task-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
  
  .task-meta {
    width: 100%;
    justify-content: space-between;
  }
  
  .task-actions {
    flex-direction: column;
  }
  
  .action-btn {
    width: 100%;
  }
}
</style> 