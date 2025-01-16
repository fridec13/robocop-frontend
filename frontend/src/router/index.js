import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import DashboardView from '../views/DashboardView.vue'
import PointCloudViewer from '../components/dashboard/monitoring/PointCloudViewer.vue'
import StatsView from '../components/dashboard/stats/StatsView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'login',
      component: LoginView
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: DashboardView,
      children: [
        {
          path: 'monitoring',
          name: 'monitoring',
          component: () => import('../components/dashboard/monitoring/RealTimeMonitoring.vue')
        },
        {
          path: 'robot-management',
          name: 'robot-management',
          component: () => import('../components/dashboard/robot/RobotManagement.vue')
        },
        {
          path: 'point-cloud',
          name: 'point-cloud',
          component: PointCloudViewer
        },
        {
          path: 'stats',
          name: 'stats',
          component: StatsView
        },
        {
          path: 'settings',
          name: 'settings',
          component: () => import('../components/dashboard/settings/SettingsView.vue')
        }
      ]
    }
  ]
})

export default router
