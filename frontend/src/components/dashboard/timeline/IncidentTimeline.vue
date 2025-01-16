<template>
  <div class="incident-timeline">
    <div class="header">
      <h2>특이사항 타임라인</h2>
      <div class="filters">
        <select v-model="selectedType" class="filter-select">
          <option value="">전체 유형</option>
          <option v-for="type in incidentTypes" :key="type.value" :value="type.value">
            {{ type.label }}
          </option>
        </select>
        <select v-model="selectedRobot" class="filter-select">
          <option value="">전체 로봇</option>
          <option v-for="robot in robots" :key="robot.id" :value="robot.id">
            {{ robot.name }}
          </option>
        </select>
      </div>
    </div>

    <div class="timeline-container">
      <div v-for="(group, date) in groupedIncidents" :key="date" class="timeline-group">
        <div class="timeline-date">{{ formatDate(date) }}</div>
        
        <div class="timeline-items">
          <div v-for="incident in group" :key="incident.id" 
               class="timeline-item"
               :class="{ 'high-priority': incident.priority === 'high' }">
            <div class="time">{{ formatTime(incident.timestamp) }}</div>
            
            <div class="incident-content">
              <div class="incident-header">
                <span class="type-badge" :class="incident.type">
                  {{ getIncidentTypeLabel(incident.type) }}
                </span>
                <span class="robot-name">{{ incident.robotName }}</span>
              </div>
              
              <div class="incident-details">
                <p class="description">{{ incident.description }}</p>
                <div class="location">위치: {{ incident.location }}</div>
              </div>

              <div class="incident-media" v-if="incident.media">
                <img v-if="incident.media.type === 'image'" 
                     :src="incident.media.url" 
                     :alt="incident.description"
                     @click="openMedia(incident.media)">
                <video v-else-if="incident.media.type === 'video'"
                       :src="incident.media.url"
                       controls></video>
              </div>

              <div class="incident-actions">
                <button class="action-btn" @click="handleIncident(incident.id)">
                  {{ incident.handled ? '처리 완료' : '처리하기' }}
                </button>
                <button class="action-btn" @click="showDetails(incident)">
                  상세 보기
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-if="Object.keys(groupedIncidents).length === 0" class="no-incidents">
        특이사항이 없습니다.
      </div>
    </div>

    <!-- 상세 보기 모달 -->
    <div v-if="selectedIncident" class="modal">
      <div class="modal-content">
        <div class="modal-header">
          <h3>특이사항 상세</h3>
          <button class="close-btn" @click="selectedIncident = null">&times;</button>
        </div>
        
        <div class="modal-body">
          <div class="detail-item">
            <span class="label">발생 시각</span>
            <span class="value">{{ formatDateTime(selectedIncident.timestamp) }}</span>
          </div>
          <div class="detail-item">
            <span class="label">유형</span>
            <span class="value">{{ getIncidentTypeLabel(selectedIncident.type) }}</span>
          </div>
          <div class="detail-item">
            <span class="label">로봇</span>
            <span class="value">{{ selectedIncident.robotName }}</span>
          </div>
          <div class="detail-item">
            <span class="label">위치</span>
            <span class="value">{{ selectedIncident.location }}</span>
          </div>
          <div class="detail-item">
            <span class="label">설명</span>
            <p class="value description">{{ selectedIncident.description }}</p>
          </div>
          
          <div class="detail-media" v-if="selectedIncident.media">
            <img v-if="selectedIncident.media.type === 'image'" 
                 :src="selectedIncident.media.url" 
                 :alt="selectedIncident.description">
            <video v-else-if="selectedIncident.media.type === 'video'"
                   :src="selectedIncident.media.url"
                   controls></video>
          </div>

          <div class="detail-actions">
            <button class="action-btn" 
                    @click="handleIncident(selectedIncident.id)"
                    :class="{ handled: selectedIncident.handled }">
              {{ selectedIncident.handled ? '처리 완료' : '처리하기' }}
            </button>
            <button class="action-btn" @click="exportIncident(selectedIncident)">
              내보내기
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const selectedType = ref('')
const selectedRobot = ref('')
const selectedIncident = ref(null)

const incidentTypes = [
  { value: 'unauthorized', label: '신원확인 불가' },
  { value: 'suspicious', label: '거동 수상자' },
  { value: 'emergency', label: '비상 상황' },
  { value: 'malfunction', label: '로봇 오작동' }
]

const robots = ref([
  { id: 'SSAFY-ROBO-1', name: 'Robot 1' },
  { id: 'SSAFY-ROBO-2', name: 'Robot 2' }
])

// 예시 데이터
const incidents = ref([
  {
    id: 1,
    type: 'unauthorized',
    timestamp: new Date('2024-02-20T10:30:00'),
    robotName: 'Robot 1',
    location: '1층 로비',
    description: '신원 미확인 인원 발견',
    priority: 'high',
    handled: false,
    media: {
      type: 'image',
      url: '/images/incident1.jpg'
    }
  },
  {
    id: 2,
    type: 'suspicious',
    timestamp: new Date('2024-02-20T15:45:00'),
    robotName: 'Robot 2',
    location: '주차장 입구',
    description: '수상한 행동 포착',
    priority: 'medium',
    handled: true,
    media: {
      type: 'video',
      url: '/videos/incident2.mp4'
    }
  }
])

// 필터링된 특이사항
const filteredIncidents = computed(() => {
  return incidents.value.filter(incident => {
    if (selectedType.value && incident.type !== selectedType.value) return false
    if (selectedRobot.value && incident.robotName !== selectedRobot.value) return false
    return true
  })
})

// 날짜별로 그룹화
const groupedIncidents = computed(() => {
  const groups = {}
  filteredIncidents.value.forEach(incident => {
    const date = incident.timestamp.toISOString().split('T')[0]
    if (!groups[date]) groups[date] = []
    groups[date].push(incident)
  })
  return groups
})

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('ko-KR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    weekday: 'long'
  })
}

const formatTime = (date) => {
  return date.toLocaleTimeString('ko-KR', {
    hour: '2-digit',
    minute: '2-digit'
  })
}

const formatDateTime = (date) => {
  return date.toLocaleString('ko-KR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    weekday: 'long',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const getIncidentTypeLabel = (type) => {
  const found = incidentTypes.find(t => t.value === type)
  return found ? found.label : type
}

const handleIncident = (id) => {
  const incident = incidents.value.find(inc => inc.id === id)
  if (incident) {
    incident.handled = !incident.handled
  }
}

const showDetails = (incident) => {
  selectedIncident.value = incident
}

const openMedia = (media) => {
  // 미디어 뷰어 구현
  console.log('미디어 열기:', media)
}

const exportIncident = (incident) => {
  // 특이사항 내보내기 구현
  console.log('특이사항 내보내기:', incident)
}
</script>

<style scoped>
.incident-timeline {
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

.timeline-container {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.timeline-group {
  background-color: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.timeline-date {
  font-weight: bold;
  color: #333;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid #f0f0f0;
}

.timeline-items {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.timeline-item {
  display: flex;
  gap: 1rem;
  padding: 1rem;
  background-color: #f8f9fa;
  border-radius: 4px;
  border-left: 4px solid #ddd;
}

.timeline-item.high-priority {
  border-left-color: #dc3545;
}

.time {
  color: #666;
  font-size: 0.875rem;
  white-space: nowrap;
}

.incident-content {
  flex: 1;
}

.incident-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 0.5rem;
}

.type-badge {
  padding: 0.25rem 0.5rem;
  border-radius: 999px;
  font-size: 0.75rem;
  font-weight: 500;
}

.type-badge.unauthorized {
  background-color: #dc3545;
  color: white;
}

.type-badge.suspicious {
  background-color: #ffc107;
  color: #000;
}

.type-badge.emergency {
  background-color: #dc3545;
  color: white;
}

.type-badge.malfunction {
  background-color: #6c757d;
  color: white;
}

.robot-name {
  color: #666;
  font-size: 0.875rem;
}

.incident-details {
  margin-bottom: 1rem;
}

.description {
  margin-bottom: 0.5rem;
}

.location {
  color: #666;
  font-size: 0.875rem;
}

.incident-media {
  margin: 1rem 0;
}

.incident-media img,
.incident-media video {
  max-width: 100%;
  border-radius: 4px;
}

.incident-actions {
  display: flex;
  gap: 0.5rem;
}

.action-btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  background-color: #007bff;
  color: white;
  cursor: pointer;
}

.action-btn.handled {
  background-color: #28a745;
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
  border-radius: 8px;
  width: 90%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #ddd;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
}

.modal-body {
  padding: 1.5rem;
}

.detail-item {
  margin-bottom: 1rem;
}

.detail-item .label {
  display: block;
  color: #666;
  font-size: 0.875rem;
  margin-bottom: 0.25rem;
}

.detail-item .value {
  color: #333;
}

.detail-item .value.description {
  white-space: pre-line;
}

.detail-media {
  margin: 1rem 0;
}

.detail-media img,
.detail-media video {
  max-width: 100%;
  border-radius: 4px;
}

.detail-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1.5rem;
}

.no-incidents {
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
  
  .timeline-item {
    flex-direction: column;
  }
  
  .incident-actions {
    flex-direction: column;
  }
  
  .action-btn {
    width: 100%;
  }
}
</style> 