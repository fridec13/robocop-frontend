<template>
  <div class="robot-control-test">
    <h2>로봇 제어 테스트</h2>
    
    <div class="connection-panel">
      <input
        v-model="robotId"
        type="text"
        placeholder="로봇 ID 입력"
        :disabled="isConnected"
      />
      <button 
        v-if="!isConnected"
        @click="handleConnect"
      >
        연결
      </button>
      <button 
        v-else
        @click="handleDisconnect"
      >
        연결 해제
      </button>
    </div>

    <div class="status-panel" :class="statusClass">
      <div class="status-indicator">
        상태: {{ isConnected ? '연결됨' : '연결 끊김' }}
      </div>
      <div v-if="error" class="error-message">{{ error }}</div>
    </div>

    <div v-if="isConnected" class="control-info">
      <h3>조작 방법</h3>
      <ul>
        <li>↑: 전진</li>
        <li>↓: 후진</li>
        <li>←: 좌회전</li>
        <li>→: 우회전</li>
        <li>방향키 동시 입력: 대각선 이동</li>
      </ul>
    </div>

    <div v-if="lastCommand" class="command-feedback">
      <h3>현재 명령</h3>
      <div>선속도: {{ lastCommand.linear }} m/s</div>
      <div>각속도: {{ lastCommand.angular }} rad/s</div>
      <div>눌린 키: {{ lastCommand.keys.join(', ') }}</div>
    </div>
  </div>
</template>

<script>
import { RobotControl } from '@/services/websocket/robotControl';

export default {
  name: 'RobotControlTest',
  
  data() {
    return {
      robotId: '',
      isConnected: false,
      controlInstance: null,
      lastCommand: null,
      error: null
    };
  },

  computed: {
    statusClass() {
      return this.isConnected ? 'status-connected' : 'status-disconnected';
    }
  },

  methods: {
    handleConnect() {
      if (!this.robotId) {
        this.error = '로봇 ID를 입력해주세요';
        return;
      }

      const control = new RobotControl(this.robotId, {
        onConnect: () => {
          this.isConnected = true;
          this.error = null;
        },
        onDisconnect: () => {
          this.isConnected = false;
        },
        onError: (error) => {
          this.error = error;
        },
        onFeedback: (data) => {
          this.lastCommand = {
            linear: data.twist.linear.x.toFixed(2),
            angular: data.twist.angular.z.toFixed(2),
            keys: data.pressed_keys
          };
        }
      });

      control.connect();
      this.controlInstance = control;
    },

    handleDisconnect() {
      if (this.controlInstance) {
        this.controlInstance.disconnect();
        this.controlInstance = null;
        this.isConnected = false;
      }
    }
  },

  beforeUnmount() {
    if (this.controlInstance) {
      this.controlInstance.disconnect();
    }
  }
};
</script>

<style scoped>
.robot-control-test {
  max-width: 600px;
  margin: 20px auto;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  background-color: white;
}

.connection-panel {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.connection-panel input {
  flex: 1;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.connection-panel button {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  background-color: #007bff;
  color: white;
  cursor: pointer;
}

.connection-panel button:hover {
  background-color: #0056b3;
}

.status-panel {
  padding: 10px;
  border-radius: 4px;
  margin-bottom: 20px;
}

.status-connected {
  background-color: #d4edda;
  border: 1px solid #c3e6cb;
}

.status-disconnected {
  background-color: #f8d7da;
  border: 1px solid #f5c6cb;
}

.status-indicator {
  font-weight: bold;
}

.error-message {
  color: #dc3545;
  margin-top: 10px;
}

.control-info {
  background-color: #f8f9fa;
  padding: 15px;
  border-radius: 4px;
  margin-bottom: 20px;
}

.control-info ul {
  list-style-type: none;
  padding: 0;
}

.control-info li {
  margin: 5px 0;
  padding: 5px 0;
}

.command-feedback {
  background-color: #e9ecef;
  padding: 15px;
  border-radius: 4px;
}

.command-feedback div {
  margin: 5px 0;
}
</style> 