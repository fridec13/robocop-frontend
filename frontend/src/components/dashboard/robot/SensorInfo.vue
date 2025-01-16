<template>
  <div class="sensor-info">
    <div class="header">
      <h2>센서 정보</h2>
      <div class="robot-selector">
        <select v-model="selectedRobot">
          <option value="">로봇 선택</option>
          <option v-for="robot in robots" :key="robot.id" :value="robot.id">
            {{ robot.name }} ({{ robot.id }})
          </option>
        </select>
      </div>
    </div>

    <div v-if="selectedRobot" class="sensor-panel">
      <!-- LiDAR 센서 정보 -->
      <div class="sensor-group">
        <h3>LiDAR 센서</h3>
        <div class="sensor-grid">
          <div class="sensor-item">
            <span class="label">스캔 범위</span>
            <span class="value">360°</span>
          </div>
          <div class="sensor-item">
            <span class="label">스캔 속도</span>
            <span class="value">10Hz</span>
          </div>
          <div class="sensor-item">
            <span class="label">감지 거리</span>
            <span class="value">0.1m ~ 30m</span>
          </div>
          <div class="sensor-item">
            <span class="label">정확도</span>
            <span class="value">±30mm</span>
          </div>
        </div>
        <div class="sensor-visualization">
          <div class="lidar-view">
            <!-- LiDAR 시각화가 들어갈 자리 -->
            <div class="placeholder">LiDAR 시각화</div>
          </div>
        </div>
      </div>

      <!-- 카메라 센서 정보 -->
      <div class="sensor-group">
        <h3>카메라</h3>
        <div class="sensor-grid">
          <div class="sensor-item">
            <span class="label">해상도</span>
            <span class="value">1920 x 1080</span>
          </div>
          <div class="sensor-item">
            <span class="label">FPS</span>
            <span class="value">30</span>
          </div>
          <div class="sensor-item">
            <span class="label">시야각</span>
            <span class="value">120°</span>
          </div>
          <div class="sensor-item">
            <span class="label">야간 모드</span>
            <span class="value">활성화</span>
          </div>
        </div>
      </div>

      <!-- IMU 센서 정보 -->
      <div class="sensor-group">
        <h3>IMU 센서</h3>
        <div class="sensor-grid">
          <div class="sensor-item">
            <span class="label">가속도</span>
            <span class="value">{{ sensorData.acceleration.toFixed(2) }} m/s²</span>
          </div>
          <div class="sensor-item">
            <span class="label">각속도</span>
            <span class="value">{{ sensorData.angularVelocity.toFixed(2) }} rad/s</span>
          </div>
          <div class="sensor-item">
            <span class="label">방향</span>
            <span class="value">{{ sensorData.orientation.toFixed(2) }}°</span>
          </div>
          <div class="sensor-item">
            <span class="label">온도</span>
            <span class="value">{{ sensorData.temperature.toFixed(1) }}°C</span>
          </div>
        </div>
      </div>

      <!-- 기타 센서 정보 -->
      <div class="sensor-group">
        <h3>기타 센서</h3>
        <div class="sensor-grid">
          <div class="sensor-item">
            <span class="label">습도</span>
            <span class="value">{{ sensorData.humidity.toFixed(1) }}%</span>
          </div>
          <div class="sensor-item">
            <span class="label">기압</span>
            <span class="value">{{ sensorData.pressure.toFixed(0) }} hPa</span>
          </div>
          <div class="sensor-item">
            <span class="label">소음 레벨</span>
            <span class="value">{{ sensorData.noiseLevel.toFixed(1) }} dB</span>
          </div>
          <div class="sensor-item">
            <span class="label">CO₂ 농도</span>
            <span class="value">{{ sensorData.co2Level }} ppm</span>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="no-robot-selected">
      로봇을 선택해주세요
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const selectedRobot = ref('')
const robots = ref([
  { id: 'SSAFY-ROBO-1', name: 'Robot 1' },
  { id: 'SSAFY-ROBO-2', name: 'Robot 2' }
])

// 실제로는 실시간으로 업데이트되어야 하는 센서 데이터
const sensorData = ref({
  acceleration: 0.25,
  angularVelocity: 0.15,
  orientation: 45.5,
  temperature: 23.4,
  humidity: 45.5,
  pressure: 1013,
  noiseLevel: 45.2,
  co2Level: 450
})

// 실제 구현 시에는 웹소켓 등을 통해 실시간 데이터 업데이트 필요
</script>

<style scoped>
.sensor-info {
  padding: 1.5rem;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.robot-selector select {
  padding: 0.5rem;
  border-radius: 4px;
  border: 1px solid #ddd;
  width: 200px;
}

.sensor-panel {
  display: grid;
  gap: 1.5rem;
}

.sensor-group {
  background-color: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.sensor-group h3 {
  margin-bottom: 1rem;
  color: #333;
  font-size: 1.1rem;
}

.sensor-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
}

.sensor-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem;
  background-color: #f8f9fa;
  border-radius: 4px;
}

.label {
  color: #666;
  font-size: 0.875rem;
}

.value {
  font-weight: 500;
  color: #333;
}

.sensor-visualization {
  margin-top: 1rem;
}

.lidar-view {
  aspect-ratio: 1;
  background-color: #000;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.placeholder {
  color: #666;
}

.no-robot-selected {
  text-align: center;
  padding: 3rem;
  background-color: white;
  border-radius: 8px;
  color: #666;
}

@media (max-width: 768px) {
  .sensor-grid {
    grid-template-columns: 1fr;
  }
  
  .header {
    flex-direction: column;
    gap: 1rem;
  }
  
  .robot-selector select {
    width: 100%;
  }
}
</style> 