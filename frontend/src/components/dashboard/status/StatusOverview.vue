<template>
  <div class="status-overview">
    <h2>전체 현황</h2>
    <div class="status-grid">
      <div class="status-card">
        <h3>로봇 상태</h3>
        <div class="robot-status">
          <div class="status-item">
            <span class="label">활성 로봇</span>
            <span class="value">2/3</span>
          </div>
          <div class="status-item">
            <span class="label">평균 배터리</span>
            <span class="value">75%</span>
          </div>
        </div>
      </div>
      
      <div class="status-card">
        <h3>작업 현황</h3>
        <div class="task-status">
          <div class="status-item">
            <span class="label">진행중</span>
            <span class="value">2</span>
          </div>
          <div class="status-item">
            <span class="label">완료</span>
            <span class="value">12</span>
          </div>
        </div>
      </div>

      <div class="status-card">
        <h3>특이사항</h3>
        <div class="incident-status">
          <div class="status-item">
            <span class="label">오늘</span>
            <span class="value">3건</span>
          </div>
          <div class="status-item">
            <span class="label">미처리</span>
            <span class="value">1건</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// 필요한 데이터와 메서드들은 추후 추가
</script>

<style scoped>
.status-overview {
  padding: 1rem;
}

.status-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-top: 1rem;
}

.status-card {
  background-color: #fff;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.status-card h3 {
  margin-bottom: 1rem;
  color: #333;
  font-size: 1.1rem;
}

.status-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.8rem;
}

.label {
  color: #666;
}

.value {
  font-weight: bold;
  color: #333;
}
</style> 