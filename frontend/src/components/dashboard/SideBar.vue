export default {
  name: 'SideBar',
  data() {
    return {
      items: [
        {
          title: '모니터링',
          icon: 'mdi-monitor-dashboard',
          items: [
            {
              title: '실시간 모니터링',
              to: '/monitoring'
            },
            {
              title: '포인트 클라우드',
              to: '/point-cloud'
            },
            {
              title: '타임라인',
              to: '/timeline'
            },
            {
              title: '지도',
              to: '/map'
            }
          ]
        },
        {
          title: '로봇 관리',
          icon: 'mdi-robot',
          items: [
            {
              title: '로봇 목록',
              to: '/robot/management'
            },
            {
              title: '로봇 제어',
              to: '/robot/control'
            },
            {
              title: '로봇 제어 테스트',
              to: '/robot/control-test',
              icon: 'mdi-gamepad-variant'
            },
            {
              title: '경로 관리',
              to: '/course-management'
            },
            {
              title: '센서 데이터',
              to: '/sensor-data'
            }
          ]
        },
        {
          title: '통계',
          icon: 'mdi-chart-bar',
          items: [
            {
              title: '요약',
              to: '/stats-summary'
            },
            {
              title: '영상',
              to: '/stats-video'
            }
          ]
        },
        {
          title: '설정',
          icon: 'mdi-cog',
          to: '/settings'
        }
      ]
    }
  }
} 