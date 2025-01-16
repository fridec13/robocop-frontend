<template>
  <div class="robot-settings">
    <div class="header">
      <h2>로봇 설정</h2>
      <button class="add-robot-btn" @click="showAddRobotModal = true">
        <span>+</span> 로봇 추가
      </button>
    </div>

    <div class="robot-list">
      <div v-for="robot in robots" :key="robot.id" class="robot-card">
        <div class="robot-header">
          <div class="robot-status" :class="{ active: robot.isActive }">
            {{ robot.isActive ? '활성' : '비활성' }}
          </div>
          <h3>{{ robot.name }}</h3>
        </div>

        <div class="robot-info">
          <div class="info-item">
            <span class="label">ID</span>
            <span class="value">{{ robot.id }}</span>
          </div>
          <div class="info-item">
            <span class="label">상태</span>
            <span class="value">{{ robot.status }}</span>
          </div>
          <div class="info-item">
            <span class="label">현재 위치</span>
            <span class="value">{{ robot.location }}</span>
          </div>
          <div class="info-item">
            <span class="label">배터리</span>
            <span class="value">{{ robot.battery }}%</span>
          </div>
        </div>

        <div class="robot-controls">
          <button class="control-btn" @click="toggleRobotStatus(robot.id)">
            {{ robot.isActive ? '비활성화' : '활성화' }}
          </button>
          <button class="control-btn" @click="openManualControl(robot.id)">
            수동 제어
          </button>
          <button class="control-btn settings" @click="openSettings(robot.id)">
            설정
          </button>
        </div>
      </div>
    </div>

    <!-- 로봇 추가 모달 -->
    <div v-if="showAddRobotModal" class="modal">
      <div class="modal-content">
        <h3>새 로봇 추가</h3>
        <form @submit.prevent="addNewRobot">
          <div class="form-group">
            <label>로봇 이름</label>
            <input v-model="newRobot.name" type="text" required>
          </div>
          <div class="form-group">
            <label>로봇 ID</label>
            <input v-model="newRobot.id" type="text" required>
          </div>
          <div class="modal-buttons">
            <button type="button" @click="showAddRobotModal = false">취소</button>
            <button type="submit">추가</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const showAddRobotModal = ref(false)
const robots = ref([
  {
    id: 'SSAFY-ROBO-1',
    name: 'Robot 1',
    isActive: true,
    status: '순찰 중',
    location: '1층 사무실',
    battery: 85
  },
  {
    id: 'SSAFY-ROBO-2',
    name: 'Robot 2',
    isActive: false,
    status: '대기 중',
    location: '충전소',
    battery: 30
  }
])

const newRobot = ref({
  name: '',
  id: ''
})

const toggleRobotStatus = (robotId) => {
  const robot = robots.value.find(r => r.id === robotId)
  if (robot) {
    robot.isActive = !robot.isActive
  }
}

const openManualControl = (robotId) => {
  // 수동 제어 페이지로 이동 또는 모달 표시
  console.log('수동 제어:', robotId)
}

const openSettings = (robotId) => {
  // 설정 페이지로 이동 또는 모달 표시
  console.log('설정:', robotId)
}

const addNewRobot = () => {
  robots.value.push({
    ...newRobot.value,
    isActive: false,
    status: '대기 중',
    location: '미지정',
    battery: 100
  })
  showAddRobotModal.value = false
  newRobot.value = { name: '', id: '' }
}
</script>

<style scoped>
.robot-settings {
  padding: 1.5rem;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.add-robot-btn {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.robot-list {
  display: grid;
  gap: 1.5rem;
}

.robot-card {
  background-color: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.robot-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
}

.robot-status {
  padding: 0.25rem 0.75rem;
  border-radius: 999px;
  font-size: 0.875rem;
  background-color: #dc3545;
  color: white;
}

.robot-status.active {
  background-color: #28a745;
}

.robot-info {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.label {
  color: #666;
  font-size: 0.875rem;
}

.value {
  font-weight: 500;
}

.robot-controls {
  display: flex;
  gap: 0.5rem;
}

.control-btn {
  flex: 1;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: white;
  cursor: pointer;
  transition: all 0.2s;
}

.control-btn:hover {
  background-color: #f8f9fa;
}

.control-btn.settings {
  background-color: #6c757d;
  color: white;
  border: none;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  padding: 2rem;
  border-radius: 8px;
  width: 100%;
  max-width: 500px;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #333;
}

.form-group input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.modal-buttons {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1.5rem;
}

.modal-buttons button {
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
}

.modal-buttons button[type="button"] {
  background-color: #6c757d;
  color: white;
  border: none;
}

.modal-buttons button[type="submit"] {
  background-color: #007bff;
  color: white;
  border: none;
}

@media (max-width: 768px) {
  .robot-info {
    grid-template-columns: 1fr;
  }
  
  .robot-controls {
    flex-direction: column;
  }
  
  .control-btn {
    width: 100%;
  }
}
</style> 