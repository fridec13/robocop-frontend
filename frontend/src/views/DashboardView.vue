<template>
  <div class="dashboard-container">
    <!-- 왼쪽 메뉴 -->
    <div class="left-sidebar">
      <div class="logo-area" @click="refreshPage" style="cursor: pointer;">
        <img src="@/assets/logo.png" alt="로고" class="logo">
      </div>
      <nav class="main-menu">
        <div
          v-for="item in menuItems"
          :key="item.id"
          class="menu-group"
        >
          <div 
            class="menu-item"
            :class="{ active: activeMenu === item.id }"
            @click="handleMenuClick(item)"
          >
            {{ item.name }}
          </div>
          <div 
            class="submenu-items"
            :class="{ expanded: activeMenu === item.id }"
          >
            <router-link
              v-for="subMenu in item.subMenus"
              :key="subMenu.id"
              :to="{ name: subMenu.id }"
              class="submenu-item"
              :class="{ active: $route.name === subMenu.id }"
            >
              {{ subMenu.name }}
            </router-link>
          </div>
        </div>
      </nav>
    </div>

    <!-- 메인 컨텐츠 영역 -->
    <div class="main-content">
      <router-view></router-view>
    </div>

    <!-- 오른쪽 실시간 모니터링 사이드바 -->
    <div class="right-sidebar">
      <!-- 실시간 알림 섹션 추가 -->
      <div class="alert-section">
        <h3>실시간 알림</h3>
        <div class="alert-list">
          <div class="alert-item warning">
            <span class="time">오후 04:27</span>
            <span class="message">Robot 2의 배터리가 부족합니다. (25%)</span>
          </div>
          <div class="alert-item info">
            <span class="time">오후 04:22</span>
            <span class="message">Robot 1이 순찰을 시작했습니다.</span>
          </div>
        </div>
      </div>

      <div class="divider"></div>

      <div class="monitoring-header">
        <h3>실시간 모니터링</h3>
      </div>
      <div class="video-container">
        <div class="camera-section">
          <h3>카메라 1</h3>
          <CameraView />
        </div>
        <div class="camera-section">
          <h3>카메라 2</h3>
          <CameraView />
        </div>
      </div>
      <div class="monitoring-info">
        <div class="info-item">
          <span class="label">현재 상태:</span>
          <span class="value">정상 운영 중</span>
        </div>
        <div class="info-item">
          <span class="label">배터리:</span>
          <span class="value">85%</span>
        </div>
        <div class="info-item">
          <span class="label">현재 위치:</span>
          <span class="value">1층 로비</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import CameraView from '@/components/dashboard/monitoring/CameraView.vue'

const router = useRouter()
const activeMenu = ref('')

const menuItems = [
  {
    id: 'monitoring',
    name: '현황',
    subMenus: [
      { id: 'monitoring', name: '실시간 모니터링' },
      { id: 'point-cloud', name: '라이다 정보' }
    ]
  },
  {
    id: 'robot',
    name: '로봇 관리',
    subMenus: [
      { id: 'robot-management', name: '로봇 관리' }
    ]
  },
  {
    id: 'stats',
    name: '통계',
    subMenus: [
      { id: 'stats', name: '통계 및 파일관리' }
    ]
  },
  {
    id: 'settings',
    name: '설정',
    subMenus: [
      { id: 'settings', name: '시스템 설정' }
    ]
  }
]

const getActiveMenuItem = computed(() => {
  return menuItems.find(item => item.id === activeMenu.value)
})

const handleMenuClick = (item) => {
  activeMenu.value = item.id
  // 해당 메뉴의 첫 번째 서브메뉴로 이동
  if (item.subMenus && item.subMenus.length > 0) {
    router.push({ name: item.subMenus[0].id })
  }
}

const refreshPage = () => {
  window.location.reload()
}

// 초기 메뉴 설정
router.isReady().then(() => {
  const currentRoute = router.currentRoute.value
  const currentMenuItem = menuItems.find(item => 
    item.subMenus.some(subMenu => subMenu.id === currentRoute.name)
  )
  if (currentMenuItem) {
    activeMenu.value = currentMenuItem.id
  } else {
    // 기본 페이지로 리다이렉트
    router.push({ name: 'monitoring' })
  }
})
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.dashboard-container {
  display: flex;
  height: 100vh;
  width: 100%;
  overflow: hidden;
  background-color: #f5f5f5;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
}

.left-sidebar {
  width: 280px;
  background: #1a1a1a;
  color: white;
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
  overflow-y: auto;
}

.logo-area {
  padding: 20px;
  text-align: center;
  background: white;
}

.logo {
  height: 40px;
  width: auto;
}

.main-menu {
  padding: 10px 0;
}

.menu-group {
  margin-bottom: 2px;
}

.menu-item {
  padding: 12px 20px;
  cursor: pointer;
  transition: all 0.3s;
  background: #1a1a1a;
}

.menu-item:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.menu-item.active {
  background-color: #007bff;
}

.submenu-items {
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.3s ease-out;
  background: #2a2a2a;
}

.submenu-items.expanded {
  max-height: 200px; /* 서브메뉴 최대 높이 */
}

.submenu-item {
  display: block;
  padding: 10px 20px 10px 40px;
  color: #fff;
  text-decoration: none;
  transition: background-color 0.3s;
  font-size: 0.95em;
}

.submenu-item:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.submenu-item.active {
  background-color: rgba(0, 123, 255, 0.2);
  color: #fff;
}

.main-content {
  flex: 1;
  overflow: auto;
  padding: 20px;
  background: white;
  min-width: 0;
  display: flex;
  flex-direction: column;
}

.right-sidebar {
  width: 400px;
  background: white;
  border-left: 1px solid #ddd;
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
  overflow-y: auto;
}

.monitoring-header {
  padding: 20px;
  border-bottom: 1px solid #ddd;
}

.monitoring-header h3 {
  margin: 0;
  color: #333;
}

.video-container {
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.camera-section {
  background: #1a1a1a;
  border-radius: 8px;
  overflow: hidden;
  margin-bottom: 1rem;
}

.camera-section h3 {
  padding: 0.5rem 1rem;
  margin: 0;
  background: #2a2a2a;
  color: white;
}

.monitoring-info {
  padding: 20px;
  border-top: 1px solid #ddd;
}

.info-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
  padding: 8px;
  background: #f8f9fa;
  border-radius: 4px;
}

.info-item .label {
  color: #666;
}

.info-item .value {
  font-weight: 500;
  color: #333;
}

@media (max-width: 1600px) {
  .right-sidebar {
    width: 350px;
  }
}

@media (max-width: 768px) {
  .left-sidebar {
    position: fixed;
    left: -280px;
    top: 0;
    bottom: 0;
    z-index: 1000;
    transition: left 0.3s ease;
  }

  .left-sidebar.open {
    left: 0;
  }

  .right-sidebar {
    display: none;
  }
}

.alert-section {
  padding: 20px;
  background: white;
}

.alert-section h3 {
  margin: 0 0 15px 0;
  color: #333;
}

.alert-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.alert-item {
  padding: 12px;
  border-radius: 4px;
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.alert-item.warning {
  background-color: #fff3cd;
  border: 1px solid #ffeeba;
  color: #856404;
}

.alert-item.info {
  background-color: #cce5ff;
  border: 1px solid #b8daff;
  color: #004085;
}

.alert-item .time {
  font-size: 0.85em;
  opacity: 0.8;
}

.alert-item .message {
  font-weight: 500;
}

.divider {
  height: 1px;
  background: #ddd;
  margin: 0;
}
</style> 