<template>
  <div class="settings-container">
    <div class="settings-section">
      <h2>시스템 설정</h2>
      
      <div class="setting-group">
        <h3>일반 설정</h3>
        <div class="setting-item">
          <label>언어</label>
          <select v-model="settings.language">
            <option value="ko">한국어</option>
            <option value="en">English</option>
          </select>
        </div>
        <div class="setting-item">
          <label>시간대</label>
          <select v-model="settings.timezone">
            <option value="Asia/Seoul">서울 (UTC+9)</option>
            <option value="UTC">UTC</option>
          </select>
        </div>
      </div>

      <div class="setting-group">
        <h3>알림 설정</h3>
        <div class="setting-item">
          <label>알림 사용</label>
          <input type="checkbox" v-model="settings.notifications.enabled">
        </div>
        <div class="setting-item" v-if="settings.notifications.enabled">
          <label>알림 유형</label>
          <div class="checkbox-group">
            <label>
              <input type="checkbox" v-model="settings.notifications.types.error">
              오류
            </label>
            <label>
              <input type="checkbox" v-model="settings.notifications.types.warning">
              경고
            </label>
            <label>
              <input type="checkbox" v-model="settings.notifications.types.info">
              정보
            </label>
          </div>
        </div>
      </div>

      <div class="setting-group">
        <h3>로봇 설정</h3>
        <div class="setting-item">
          <label>자동 충전 임계값 (%)</label>
          <input 
            type="number" 
            v-model="settings.robot.autoChargeThreshold"
            min="0"
            max="100"
          >
        </div>
        <div class="setting-item">
          <label>야간 모드</label>
          <input type="checkbox" v-model="settings.robot.nightMode">
        </div>
      </div>

      <div class="setting-group">
        <h3>백업 설정</h3>
        <div class="setting-item">
          <label>자동 백업</label>
          <input type="checkbox" v-model="settings.backup.enabled">
        </div>
        <div class="setting-item" v-if="settings.backup.enabled">
          <label>백업 주기</label>
          <select v-model="settings.backup.interval">
            <option value="daily">매일</option>
            <option value="weekly">매주</option>
            <option value="monthly">매월</option>
          </select>
        </div>
      </div>
    </div>

    <div class="settings-actions">
      <button class="save-btn" @click="saveSettings">저장</button>
      <button class="reset-btn" @click="resetSettings">초기화</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const settings = ref({
  language: 'ko',
  timezone: 'Asia/Seoul',
  notifications: {
    enabled: true,
    types: {
      error: true,
      warning: true,
      info: true
    }
  },
  robot: {
    autoChargeThreshold: 20,
    nightMode: false
  },
  backup: {
    enabled: true,
    interval: 'daily'
  }
});

const saveSettings = () => {
  // API 호출 로직 구현 예정
  console.log('설정 저장:', settings.value);
};

const resetSettings = () => {
  // 기본값으로 초기화
  settings.value = {
    language: 'ko',
    timezone: 'Asia/Seoul',
    notifications: {
      enabled: true,
      types: {
        error: true,
        warning: true,
        info: true
      }
    },
    robot: {
      autoChargeThreshold: 20,
      nightMode: false
    },
    backup: {
      enabled: true,
      interval: 'daily'
    }
  };
};
</script>

<style scoped>
.settings-container {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

.settings-section {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.setting-group {
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid #eee;
}

.setting-group:last-child {
  border-bottom: none;
  margin-bottom: 0;
  padding-bottom: 0;
}

h2 {
  margin-bottom: 20px;
  color: #333;
}

h3 {
  margin-bottom: 15px;
  color: #666;
}

.setting-item {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
}

.setting-item label {
  width: 200px;
  color: #333;
}

.setting-item select,
.setting-item input[type="number"] {
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  width: 200px;
}

.checkbox-group {
  display: flex;
  gap: 20px;
}

.checkbox-group label {
  display: flex;
  align-items: center;
  gap: 5px;
  width: auto;
}

.settings-actions {
  margin-top: 20px;
  display: flex;
  gap: 10px;
  justify-content: flex-end;
}

button {
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  border: none;
  font-weight: 500;
}

.save-btn {
  background-color: #007bff;
  color: white;
}

.reset-btn {
  background-color: #6c757d;
  color: white;
}

button:hover {
  opacity: 0.9;
}
</style> 