<template>
  <div class="stats-container">
    <div class="filters">
      <div class="filter-group">
        <label>기간 선택:</label>
        <select v-model="selectedPeriod">
          <option value="day">일간</option>
          <option value="week">주간</option>
          <option value="month">월간</option>
        </select>
      </div>
      <div class="filter-group">
        <label>로봇 선택:</label>
        <select v-model="selectedRobot">
          <option value="all">전체</option>
          <option v-for="robot in robots" :key="robot.id" :value="robot.id">
            {{ robot.name }}
          </option>
        </select>
      </div>
      <div class="filter-group">
        <label>데이터 유형:</label>
        <select v-model="selectedDataType">
          <option value="operation">운영 시간</option>
          <option value="battery">배터리 사용</option>
          <option value="incidents">특이사항</option>
        </select>
      </div>
    </div>

    <div class="stats-table">
      <table>
        <thead>
          <tr>
            <th>날짜</th>
            <th>로봇 ID</th>
            <th>운영 시간</th>
            <th>배터리 사용량</th>
            <th>특이사항</th>
            <th>상태</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="!tableData.length">
            <td colspan="6" class="no-data">데이터가 없습니다</td>
          </tr>
          <tr v-for="(row, index) in tableData" :key="index">
            <td>{{ row.date }}</td>
            <td>{{ row.robotId }}</td>
            <td>{{ row.operationTime }}</td>
            <td>{{ row.batteryUsage }}</td>
            <td>{{ row.incidents }}</td>
            <td>{{ row.status }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="pagination">
      <button :disabled="currentPage === 1" @click="currentPage--">이전</button>
      <span>{{ currentPage }} / {{ totalPages }}</span>
      <button :disabled="currentPage === totalPages" @click="currentPage++">다음</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const selectedPeriod = ref('day');
const selectedRobot = ref('all');
const selectedDataType = ref('operation');
const currentPage = ref(1);
const totalPages = ref(1);
const tableData = ref([]);

const robots = ref([
  { id: 'ROBOT_001', name: '로봇 1' },
  { id: 'ROBOT_002', name: '로봇 2' },
  { id: 'ROBOT_003', name: '로봇 3' },
]);

// 나중에 실제 데이터를 가져오는 함수로 대체
const fetchData = () => {
  // API 호출 로직 구현 예정
  console.log('데이터 가져오기:', {
    period: selectedPeriod.value,
    robot: selectedRobot.value,
    dataType: selectedDataType.value,
    page: currentPage.value
  });
};

onMounted(() => {
  fetchData();
});
</script>

<style scoped>
.stats-container {
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.filters {
  display: flex;
  gap: 20px;
  padding: 15px;
  background: #f5f5f5;
  border-radius: 8px;
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 10px;
}

.filter-group select {
  padding: 8px;
  border-radius: 4px;
  border: 1px solid #ddd;
}

.stats-table {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
  background: white;
}

th, td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

th {
  background: #f5f5f5;
  font-weight: bold;
}

.no-data {
  text-align: center;
  padding: 40px;
  color: #666;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 15px;
}

.pagination button {
  padding: 8px 16px;
  border: 1px solid #ddd;
  background: white;
  border-radius: 4px;
  cursor: pointer;
}

.pagination button:disabled {
  background: #f5f5f5;
  cursor: not-allowed;
}

.pagination span {
  font-size: 14px;
}
</style> 