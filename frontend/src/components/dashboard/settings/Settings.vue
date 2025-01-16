<template>
  <div class="settings">
    <h2>설정</h2>

    <!-- 일반 설정 -->
    <section class="settings-section">
      <h3>일반 설정</h3>
      
      <div class="setting-group">
        <div class="setting-item">
          <label>시스템 언어</label>
          <select v-model="settings.language" class="setting-input">
            <option value="ko">한국어</option>
            <option value="en">English</option>
          </select>
        </div>

        <div class="setting-item">
          <label>시간대</label>
          <select v-model="settings.timezone" class="setting-input">
            <option value="Asia/Seoul">서울 (UTC+9)</option>
            <option value="UTC">UTC</option>
          </select>
        </div>

        <div class="setting-item">
          <label>날짜 형식</label>
          <select v-model="settings.dateFormat" class="setting-input">
            <option value="YYYY-MM-DD">YYYY-MM-DD</option>
            <option value="DD/MM/YYYY">DD/MM/YYYY</option>
            <option value="MM/DD/YYYY">MM/DD/YYYY</option>
          </select>
        </div>
      </div>
    </section>

    <!-- 알림 설정 -->
    <section class="settings-section">
      <h3>알림 설정</h3>
      
      <div class="setting-group">
        <div class="setting-item">
          <label>알림 사용</label>
          <div class="toggle-switch">
            <input type="checkbox" 
                   v-model="settings.notifications.enabled"
                   id="notifications-toggle">
            <label for="notifications-toggle"></label>
          </div>
        </div>

        <div class="setting-item" v-if="settings.notifications.enabled">
          <label>알림 유형</label>
          <div class="checkbox-group">
            <label class="checkbox-item">
              <input type="checkbox" 
                     v-model="settings.notifications.types.security">
              보안 알림
            </label>
            <label class="checkbox-item">
              <input type="checkbox" 
                     v-model="settings.notifications.types.system">
              시스템 알림
            </label>
            <label class="checkbox-item">
              <input type="checkbox" 
                     v-model="settings.notifications.types.task">
              작업 알림
            </label>
          </div>
        </div>

        <div class="setting-item" v-if="settings.notifications.enabled">
          <label>알림 방법</label>
          <div class="checkbox-group">
            <label class="checkbox-item">
              <input type="checkbox" 
                     v-model="settings.notifications.methods.email">
              이메일
            </label>
            <label class="checkbox-item">
              <input type="checkbox" 
                     v-model="settings.notifications.methods.sms">
              SMS
            </label>
            <label class="checkbox-item">
              <input type="checkbox" 
                     v-model="settings.notifications.methods.push">
              푸시 알림
            </label>
          </div>
        </div>
      </div>
    </section>

    <!-- 로봇 설정 -->
    <section class="settings-section">
      <h3>로봇 설정</h3>
      
      <div class="setting-group">
        <div class="setting-item">
          <label>자동 충전 임계값</label>
          <div class="range-input">
            <input type="range" 
                   v-model="settings.robot.autoChargeThreshold"
                   min="10" 
                   max="50"
                   step="5">
            <span class="range-value">{{ settings.robot.autoChargeThreshold }}%</span>
          </div>
        </div>

        <div class="setting-item">
          <label>순찰 속도</label>
          <div class="range-input">
            <input type="range" 
                   v-model="settings.robot.patrolSpeed"
                   min="1" 
                   max="5"
                   step="1">
            <span class="range-value">레벨 {{ settings.robot.patrolSpeed }}</span>
          </div>
        </div>

        <div class="setting-item">
          <label>야간 모드</label>
          <div class="toggle-switch">
            <input type="checkbox" 
                   v-model="settings.robot.nightMode"
                   id="night-mode-toggle">
            <label for="night-mode-toggle"></label>
          </div>
        </div>
      </div>
    </section>

    <!-- 백업 설정 -->
    <section class="settings-section">
      <h3>백업 설정</h3>
      
      <div class="setting-group">
        <div class="setting-item">
          <label>자동 백업</label>
          <div class="toggle-switch">
            <input type="checkbox" 
                   v-model="settings.backup.enabled"
                   id="backup-toggle">
            <label for="backup-toggle"></label>
          </div>
        </div>

        <div class="setting-item" v-if="settings.backup.enabled">
          <label>백업 주기</label>
          <select v-model="settings.backup.interval" class="setting-input">
            <option value="daily">매일</option>
            <option value="weekly">매주</option>
            <option value="monthly">매월</option>
          </select>
        </div>

        <div class="setting-item" v-if="settings.backup.enabled">
          <label>보관 기간</label>
          <select v-model="settings.backup.retention" class="setting-input">
            <option value="30">30일</option>
            <option value="60">60일</option>
            <option value="90">90일</option>
          </select>
        </div>
      </div>
    </section>

    <!-- 저장 버튼 -->
    <div class="settings-actions">
      <button class="action-btn save" @click="saveSettings">
        설정 저장
      </button>
      <button class="action-btn reset" @click="resetSettings">
        초기화
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

// 설정 상태
const settings = ref({
  language: 'ko',
  timezone: 'Asia/Seoul',
  dateFormat: 'YYYY-MM-DD',
  notifications: {
    enabled: true,
    types: {
      security: true,
      system: true,
      task: true
    },
    methods: {
      email: true,
      sms: false,
      push: true
    }
  },
  robot: {
    autoChargeThreshold: 20,
    patrolSpeed: 3,
    nightMode: false
  },
  backup: {
    enabled: true,
    interval: 'daily',
    retention: '30'
  }
})

// 초기 설정 저장
const initialSettings = JSON.parse(JSON.stringify(settings.value))

// 설정 저장
const saveSettings = async () => {
  try {
    // API 호출 및 설정 저장 로직
    // await fetch('/api/settings', {
    //   method: 'POST',
    //   body: JSON.stringify(settings.value)
    // })
    alert('설정이 저장되었습니다.')
  } catch (error) {
    console.error('설정 저장 실패:', error)
    alert('설정 저장에 실패했습니다.')
  }
}

// 설정 초기화
const resetSettings = () => {
  if (confirm('설정을 초기화하시겠습니까?')) {
    settings.value = JSON.parse(JSON.stringify(initialSettings))
  }
}
</script>

<style scoped>
.settings {
  padding: 1.5rem;
}

.settings-section {
  background-color: white;
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.settings-section h3 {
  margin-bottom: 1.5rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid #f0f0f0;
}

.setting-group {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.setting-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.setting-item label {
  font-weight: 500;
  color: #333;
}

.setting-input {
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  min-width: 200px;
}

/* 토글 스위치 스타일 */
.toggle-switch {
  position: relative;
  width: 50px;
  height: 24px;
}

.toggle-switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.toggle-switch label {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  transition: 0.4s;
  border-radius: 24px;
}

.toggle-switch label:before {
  position: absolute;
  content: "";
  height: 16px;
  width: 16px;
  left: 4px;
  bottom: 4px;
  background-color: white;
  transition: 0.4s;
  border-radius: 50%;
}

.toggle-switch input:checked + label {
  background-color: #007bff;
}

.toggle-switch input:checked + label:before {
  transform: translateX(26px);
}

/* 체크박스 그룹 스타일 */
.checkbox-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.checkbox-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
}

/* 범위 입력 스타일 */
.range-input {
  display: flex;
  align-items: center;
  gap: 1rem;
  min-width: 200px;
}

.range-input input[type="range"] {
  flex: 1;
}

.range-value {
  min-width: 4rem;
  text-align: right;
}

/* 저장 버튼 스타일 */
.settings-actions {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
}

.action-btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
}

.action-btn.save {
  background-color: #007bff;
  color: white;
}

.action-btn.reset {
  background-color: #6c757d;
  color: white;
}

@media (max-width: 768px) {
  .setting-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
  
  .setting-input,
  .range-input {
    width: 100%;
  }
  
  .settings-actions {
    flex-direction: column;
  }
  
  .action-btn {
    width: 100%;
  }
}
</style> 