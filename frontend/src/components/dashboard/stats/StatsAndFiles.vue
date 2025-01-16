<template>
  <div class="stats-and-files">
    <!-- 통계 섹션 -->
    <section class="stats-section">
      <h2>운영 통계</h2>
      
      <div class="stats-grid">
        <!-- 로봇 운영 시간 -->
        <div class="stat-card">
          <h3>로봇 운영 시간</h3>
          <StatCharts class="chart-container" chartType="operating-time" />
          <div class="stat-summary">
            <div class="stat-item">
              <span class="label">일일 평균</span>
              <span class="value">{{ dailyAverage }}시간</span>
            </div>
            <div class="stat-item">
              <span class="label">주간 누적</span>
              <span class="value">{{ weeklyTotal }}시간</span>
            </div>
          </div>
        </div>

        <!-- 특이사항 발생 통계 -->
        <div class="stat-card">
          <h3>특이사항 발생</h3>
          <StatCharts class="chart-container" chartType="incident" />
          <div class="stat-summary">
            <div class="stat-item">
              <span class="label">이번 주</span>
              <span class="value">{{ weeklyIncidents }}건</span>
            </div>
            <div class="stat-item">
              <span class="label">전주 대비</span>
              <span class="value" :class="incidentTrend.class">{{ incidentTrend.value }}</span>
            </div>
          </div>
        </div>

        <!-- 배터리 사용 통계 -->
        <div class="stat-card">
          <h3>배터리 사용</h3>
          <StatCharts class="chart-container" chartType="battery" />
          <div class="stat-summary">
            <div class="stat-item">
              <span class="label">평균 사용 시간</span>
              <span class="value">{{ avgBatteryTime }}시간</span>
            </div>
            <div class="stat-item">
              <span class="label">충전 횟수</span>
              <span class="value">{{ chargeCount }}회</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 파일 관리 섹션 -->
    <section class="files-section">
      <div class="files-header">
        <h2>파일 관리</h2>
        <div class="file-actions">
          <button class="action-btn" @click="showUploadModal">
            파일 업로드
          </button>
          <select v-model="selectedFileType" class="file-type-select">
            <option value="">전체 파일</option>
            <option value="image">이미지</option>
            <option value="video">영상</option>
            <option value="report">보고서</option>
          </select>
        </div>
      </div>

      <div class="files-grid">
        <div v-for="file in filteredFiles" 
             :key="file.id" 
             class="file-card"
             @click="showFileDetails(file)">
          <div class="file-icon" :class="file.type">
            <i class="icon-placeholder"></i>
          </div>
          <div class="file-info">
            <div class="file-name">{{ file.name }}</div>
            <div class="file-meta">
              <span>{{ formatFileSize(file.size) }}</span>
              <span>{{ formatDate(file.date) }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 파일 없음 표시 -->
      <div v-if="filteredFiles.length === 0" class="no-files">
        파일이 없습니다.
      </div>
    </section>

    <!-- 파일 업로드 모달 -->
    <div v-if="showingUploadModal" class="modal">
      <div class="modal-content">
        <div class="modal-header">
          <h3>파일 업로드</h3>
          <button class="close-btn" @click="showingUploadModal = false">&times;</button>
        </div>
        
        <div class="modal-body">
          <div class="upload-area"
               @dragover.prevent
               @drop.prevent="handleFileDrop">
            <input type="file" 
                   ref="fileInput" 
                   @change="handleFileSelect" 
                   multiple 
                   class="file-input">
            <div class="upload-message">
              파일을 드래그하거나 클릭하여 업로드
            </div>
          </div>

          <div v-if="uploadQueue.length > 0" class="upload-queue">
            <div v-for="file in uploadQueue" 
                 :key="file.name" 
                 class="upload-item">
              <div class="file-info">
                <span class="file-name">{{ file.name }}</span>
                <span class="file-size">{{ formatFileSize(file.size) }}</span>
              </div>
              <div class="upload-progress">
                <div class="progress-bar" 
                     :style="{ width: file.progress + '%' }">
                </div>
              </div>
            </div>
          </div>

          <div class="upload-actions">
            <button class="action-btn" 
                    @click="startUpload"
                    :disabled="uploadQueue.length === 0">
              업로드 시작
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 파일 상세 모달 -->
    <div v-if="selectedFile" class="modal">
      <div class="modal-content">
        <div class="modal-header">
          <h3>파일 상세</h3>
          <button class="close-btn" @click="selectedFile = null">&times;</button>
        </div>
        
        <div class="modal-body">
          <div class="file-preview">
            <img v-if="selectedFile.type === 'image'"
                 :src="selectedFile.url"
                 :alt="selectedFile.name">
            <video v-else-if="selectedFile.type === 'video'"
                   :src="selectedFile.url"
                   controls></video>
            <div v-else class="document-preview">
              <i class="icon-placeholder"></i>
            </div>
          </div>

          <div class="file-details">
            <div class="detail-item">
              <span class="label">파일명</span>
              <span class="value">{{ selectedFile.name }}</span>
            </div>
            <div class="detail-item">
              <span class="label">유형</span>
              <span class="value">{{ getFileTypeLabel(selectedFile.type) }}</span>
            </div>
            <div class="detail-item">
              <span class="label">크기</span>
              <span class="value">{{ formatFileSize(selectedFile.size) }}</span>
            </div>
            <div class="detail-item">
              <span class="label">업로드 일시</span>
              <span class="value">{{ formatDateTime(selectedFile.date) }}</span>
            </div>
          </div>

          <div class="file-actions">
            <button class="action-btn" @click="downloadFile(selectedFile)">
              다운로드
            </button>
            <button class="action-btn delete" @click="deleteFile(selectedFile)">
              삭제
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import StatCharts from './StatCharts.vue'

// 통계 데이터
const dailyAverage = ref(8.5)
const weeklyTotal = ref(59.5)
const weeklyIncidents = ref(12)
const incidentTrend = computed(() => ({
  value: '-15%',
  class: 'trend-down'
}))
const avgBatteryTime = ref(4.2)
const chargeCount = ref(28)

// 파일 관리
const selectedFileType = ref('')
const showingUploadModal = ref(false)
const selectedFile = ref(null)
const uploadQueue = ref([])

// 예시 파일 데이터
const files = ref([
  {
    id: 1,
    name: '순찰_보고서_20240220.pdf',
    type: 'report',
    size: 2500000,
    date: new Date('2024-02-20T15:30:00'),
    url: '/files/report1.pdf'
  },
  {
    id: 2,
    name: '특이사항_영상_01.mp4',
    type: 'video',
    size: 15000000,
    date: new Date('2024-02-20T10:15:00'),
    url: '/files/video1.mp4'
  },
  {
    id: 3,
    name: '현장사진_20240220_01.jpg',
    type: 'image',
    size: 3500000,
    date: new Date('2024-02-20T09:45:00'),
    url: '/files/image1.jpg'
  }
])

// 필터링된 파일 목록
const filteredFiles = computed(() => {
  if (!selectedFileType.value) return files.value
  return files.value.filter(file => file.type === selectedFileType.value)
})

// 파일 크기 포맷
const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i]
}

// 날짜 포맷
const formatDate = (date) => {
  return date.toLocaleDateString('ko-KR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const formatDateTime = (date) => {
  return date.toLocaleString('ko-KR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 파일 타입 레이블
const getFileTypeLabel = (type) => {
  const types = {
    image: '이미지',
    video: '영상',
    report: '보고서'
  }
  return types[type] || type
}

// 파일 업로드 모달
const showUploadModal = () => {
  showingUploadModal.value = true
  uploadQueue.value = []
}

// 파일 선택 처리
const handleFileSelect = (event) => {
  const files = Array.from(event.target.files)
  addFilesToQueue(files)
}

// 파일 드롭 처리
const handleFileDrop = (event) => {
  const files = Array.from(event.dataTransfer.files)
  addFilesToQueue(files)
}

// 업로드 큐에 파일 추가
const addFilesToQueue = (newFiles) => {
  const queueFiles = newFiles.map(file => ({
    name: file.name,
    size: file.size,
    progress: 0,
    file: file
  }))
  uploadQueue.value.push(...queueFiles)
}

// 업로드 시작
const startUpload = () => {
  uploadQueue.value.forEach(queueFile => {
    // 실제 파일 업로드 로직 구현
    console.log('파일 업로드:', queueFile.name)
    
    // 프로그레스 시뮬레이션
    let progress = 0
    const interval = setInterval(() => {
      progress += 10
      queueFile.progress = progress
      if (progress >= 100) {
        clearInterval(interval)
      }
    }, 500)
  })
}

// 파일 상세 보기
const showFileDetails = (file) => {
  selectedFile.value = file
}

// 파일 다운로드
const downloadFile = (file) => {
  // 실제 다운로드 로직 구현
  console.log('파일 다운로드:', file.name)
}

// 파일 삭제
const deleteFile = (file) => {
  if (confirm('파일을 삭제하시겠습니까?')) {
    // 실제 삭제 로직 구현
    console.log('파일 삭제:', file.name)
    files.value = files.value.filter(f => f.id !== file.id)
    selectedFile.value = null
  }
}
</script>

<style scoped>
.stats-and-files {
  padding: 1.5rem;
}

.stats-section,
.files-section {
  margin-bottom: 2rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-top: 1.5rem;
}

.stat-card {
  background-color: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.chart-container {
  margin: 1rem 0;
  height: 200px;
  background-color: #f8f9fa;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-summary {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
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

.trend-up {
  color: #28a745;
}

.trend-down {
  color: #dc3545;
}

.files-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.file-actions {
  display: flex;
  gap: 1rem;
}

.action-btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  background-color: #007bff;
  color: white;
  cursor: pointer;
}

.action-btn.delete {
  background-color: #dc3545;
}

.file-type-select {
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  min-width: 150px;
}

.files-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1rem;
}

.file-card {
  background-color: white;
  border-radius: 8px;
  padding: 1rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 1rem;
}

.file-icon {
  width: 40px;
  height: 40px;
  background-color: #f8f9fa;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.file-icon.image {
  background-color: #28a745;
}

.file-icon.video {
  background-color: #007bff;
}

.file-icon.report {
  background-color: #6c757d;
}

.file-info {
  flex: 1;
}

.file-name {
  font-weight: 500;
  margin-bottom: 0.25rem;
}

.file-meta {
  display: flex;
  gap: 1rem;
  color: #666;
  font-size: 0.875rem;
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

.upload-area {
  border: 2px dashed #ddd;
  border-radius: 8px;
  padding: 2rem;
  text-align: center;
  cursor: pointer;
  position: relative;
}

.file-input {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  opacity: 0;
  cursor: pointer;
}

.upload-message {
  color: #666;
}

.upload-queue {
  margin-top: 1.5rem;
}

.upload-item {
  background-color: #f8f9fa;
  border-radius: 4px;
  padding: 1rem;
  margin-bottom: 0.5rem;
}

.upload-progress {
  height: 4px;
  background-color: #ddd;
  border-radius: 2px;
  margin-top: 0.5rem;
}

.progress-bar {
  height: 100%;
  background-color: #007bff;
  border-radius: 2px;
  transition: width 0.3s ease;
}

.file-preview {
  margin-bottom: 1.5rem;
  text-align: center;
}

.file-preview img,
.file-preview video {
  max-width: 100%;
  border-radius: 4px;
}

.document-preview {
  background-color: #f8f9fa;
  border-radius: 4px;
  padding: 2rem;
  text-align: center;
}

.file-details {
  margin-bottom: 1.5rem;
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

.file-actions {
  display: flex;
  gap: 1rem;
}

.no-files {
  text-align: center;
  padding: 3rem;
  color: #666;
  background-color: white;
  border-radius: 8px;
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .files-header {
    flex-direction: column;
    gap: 1rem;
  }
  
  .file-actions {
    width: 100%;
    flex-direction: column;
  }
  
  .file-type-select {
    width: 100%;
  }
  
  .files-grid {
    grid-template-columns: 1fr;
  }
  
  .file-actions {
    flex-direction: column;
  }
  
  .action-btn {
    width: 100%;
  }
}
</style> 