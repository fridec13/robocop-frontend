<template>
  <div class="battery-status">
    <h2>배터리 상태</h2>
    
    <div class="battery-list">
      <div v-for="robot in robots" :key="robot.id" class="battery-card">
        <div class="battery-header">
          <h3>{{ robot.name }}</h3>
          <div class="robot-id">{{ robot.id }}</div>
        </div>

        <div class="battery-info">
          <div class="battery-gauge">
            <div class="battery-level" :style="{ width: robot.battery + '%', backgroundColor: getBatteryColor(robot.battery) }"></div>
          </div>
          <div class="battery-percentage">{{ robot.battery }}%</div>
        </div>

        <div class="battery-details">
          <div class="detail-item">
            <span class="label">예상 작동 시간</span>
            <span class="value">{{ calculateRemainingTime(robot.battery) }}</span>
          </div>
          <div class="detail-item">
            <span class="label">배터리 상태</span>
            <span class="value" :class="getBatteryHealthClass(robot.batteryHealth)">
              {{ getBatteryHealthStatus(robot.batteryHealth) }}
            </span>
          </div>
          <div class="detail-item">
            <span class="label">충전 필요</span>
            <span class="value" :class="{ warning: robot.battery < 20 }">
              {{ robot.battery < 20 ? '예' : '아니오' }}
            </span>
          </div>
        </div>

        <div class="battery-actions">
          <button class="action-btn" @click="sendToCharge(robot.id)" :disabled="robot.battery >= 90">
            충전소로 이동
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const robots = ref([
  {
    id: 'SSAFY-ROBO-1',
    name: 'Robot 1',
    battery: 85,
    batteryHealth: 'good',
    isCharging: false
  },
  {
    id: 'SSAFY-ROBO-2',
    name: 'Robot 2',
    battery: 15,
    batteryHealth: 'warning',
    isCharging: false
  }
])

const getBatteryColor = (percentage) => {
  if (percentage > 60) return '#4caf50'
  if (percentage > 20) return '#ff9800'
  return '#f44336'
}

const calculateRemainingTime = (battery) => {
  // 예시: 100% = 8시간 기준
  const remainingHours = (battery / 100) * 8
  const hours = Math.floor(remainingHours)
  const minutes = Math.floor((remainingHours - hours) * 60)
  return hours + '시간 ' + minutes + '분'
}

const getBatteryHealthStatus = (health) => {
  const statusMap = {
    good: '양호',
    warning: '주의',
    bad: '교체 필요'
  }
  return statusMap[health]
}

const getBatteryHealthClass = (health) => {
  return {
    'health-good': health === 'good',
    'health-warning': health === 'warning',
    'health-bad': health === 'bad'
  }
}

const sendToCharge = (robotId) => {
  // 충전소로 이동 명령 구현
  console.log('로봇 ' + robotId + '를 충전소로 이동합니다.')
}
</script>

<style scoped>
.battery-status {
  padding: 1.5rem;
}

.battery-list {
  display: grid;
  gap: 1.5rem;
}

.battery-card {
  background-color: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.battery-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.robot-id {
  color: #666;
  font-size: 0.875rem;
}

.battery-info {
  margin-bottom: 1.5rem;
}

.battery-gauge {
  height: 24px;
  background-color: #f5f5f5;
  border-radius: 12px;
  overflow: hidden;
  margin-bottom: 0.5rem;
}

.battery-level {
  height: 100%;
  transition: width 0.3s ease;
}

.battery-percentage {
  text-align: right;
  font-weight: bold;
  color: #333;
}

.battery-details {
  display: grid;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.label {
  color: #666;
}

.value {
  font-weight: 500;
}

.value.warning {
  color: #f44336;
}

.health-good {
  color: #4caf50;
}

.health-warning {
  color: #ff9800;
}

.health-bad {
  color: #f44336;
}

.battery-actions {
  display: flex;
  justify-content: flex-end;
}

.action-btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  background-color: #007bff;
  color: white;
  cursor: pointer;
}

.action-btn:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

@media (max-width: 768px) {
  .battery-card {
    padding: 1rem;
  }
  
  .battery-details {
    grid-template-columns: 1fr;
  }
}
</style> 