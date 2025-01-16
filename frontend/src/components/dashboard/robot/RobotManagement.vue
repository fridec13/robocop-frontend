<template>
  <div class="robot-management">
    <div class="header">
      <h2>로봇 관리</h2>
      <button class="add-robot-btn" @click="showAddRobotModal = true">로봇 추가</button>
    </div>

    <div class="robot-list">
      <div v-for="robot in robots" :key="robot.id" class="robot-card">
        <div class="robot-header">
          <h3>{{ robot.name }}</h3>
          <span :class="['status-badge', robot.status]">{{ robot.status }}</span>
        </div>
        <div class="robot-info">
          <div class="info-item">
            <span class="label">ID:</span>
            <span>{{ robot.id }}</span>
          </div>
          <div class="info-item">
            <span class="label">배터리:</span>
            <div class="battery-indicator">
              <div class="battery-level" :style="{ width: `${robot.battery}%` }"></div>
              <span>{{ robot.battery }}%</span>
            </div>
          </div>
          <div class="info-item">
            <span class="label">현재 작업:</span>
            <span>{{ robot.current_task || '없음' }}</span>
          </div>
          <div class="info-item">
            <span class="label">마지막 업데이트:</span>
            <span>{{ formatDate(robot.last_updated) }}</span>
          </div>
        </div>
        <div class="robot-actions">
          <button @click="toggleRobotStatus(robot)">
            {{ robot.status === 'active' ? '비활성화' : '활성화' }}
          </button>
          <button @click="navigateToControl(robot)">수동 제어</button>
          <button @click="openSettings(robot)">설정</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const robots = ref([]);
const showAddRobotModal = ref(false);
let ws = null;

const connectWebSocket = () => {
  // 실제 WebSocket 연결은 특정 로봇에 대해서만 수행
  const robotId = 'ROBOT_001'; // 예시로 하나의 로봇만 연결
  ws = new WebSocket(`ws://localhost:8080/ws/monitoring/${robotId}`);
  
  ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    updateRobotData(data);
  };
  
  ws.onerror = (error) => {
    console.error('WebSocket 에러:', error);
  };
  
  ws.onclose = () => {
    console.log('WebSocket 연결 종료');
    setTimeout(connectWebSocket, 1000); // 재연결 시도
  };
};

const updateRobotData = (data) => {
  const index = robots.value.findIndex(r => r.id === data.id);
  if (index !== -1) {
    robots.value[index] = { ...robots.value[index], ...data };
  } else {
    robots.value.push(data);
  }
};

const formatDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleString();
};

const toggleRobotStatus = (robot) => {
  // API 호출 로직 구현 예정
  console.log('로봇 상태 변경:', robot.id);
};

const navigateToControl = (robot) => {
  router.push({ name: 'point-cloud', params: { robotId: robot.id } });
};

const openSettings = (robot) => {
  // 설정 모달 표시 로직 구현 예정
  console.log('로봇 설정 열기:', robot.id);
};

onMounted(() => {
  // 초기 로봇 데이터 로드
  fetch('http://localhost:8080/api/robots')
    .then(response => response.json())
    .then(data => {
      robots.value = data;
    })
    .catch(error => {
      console.error('로봇 데이터 로드 실패:', error);
    });

  connectWebSocket();
});

onUnmounted(() => {
  if (ws) {
    ws.close();
  }
});
</script>

<style scoped>
.robot-management {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.add-robot-btn {
  padding: 8px 16px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.robot-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.robot-card {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.robot-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.status-badge {
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 0.9em;
}

.status-badge.active {
  background-color: #28a745;
  color: white;
}

.status-badge.charging {
  background-color: #ffc107;
  color: black;
}

.status-badge.idle {
  background-color: #6c757d;
  color: white;
}

.status-badge.error {
  background-color: #dc3545;
  color: white;
}

.robot-info {
  margin-bottom: 15px;
}

.info-item {
  display: flex;
  margin-bottom: 8px;
}

.label {
  width: 120px;
  color: #666;
}

.battery-indicator {
  position: relative;
  width: 100px;
  height: 20px;
  background: #f0f0f0;
  border-radius: 10px;
  overflow: hidden;
}

.battery-level {
  position: absolute;
  left: 0;
  top: 0;
  height: 100%;
  background: #28a745;
  transition: width 0.3s ease;
}

.robot-actions {
  display: flex;
  gap: 10px;
}

.robot-actions button {
  flex: 1;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background: white;
  cursor: pointer;
  transition: background-color 0.3s;
}

.robot-actions button:hover {
  background-color: #f8f9fa;
}
</style> 