<template>
  <div class="stat-charts">
    <div class="chart-container">
      <v-chart class="chart" :option="operatingTimeOption" autoresize />
    </div>
    <div class="chart-container">
      <v-chart class="chart" :option="incidentOption" autoresize />
    </div>
    <div class="chart-container">
      <v-chart class="chart" :option="batteryOption" autoresize />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import {
  LineChart,
  BarChart,
  PieChart,
  GaugeChart
} from 'echarts/charts'
import {
  GridComponent,
  TooltipComponent,
  LegendComponent,
  DataZoomComponent,
  ToolboxComponent
} from 'echarts/components'
import VChart from 'vue-echarts'

// ECharts 컴포넌트 등록
use([
  CanvasRenderer,
  LineChart,
  BarChart,
  PieChart,
  GaugeChart,
  GridComponent,
  TooltipComponent,
  LegendComponent,
  DataZoomComponent,
  ToolboxComponent
])

// 운영 시간 차트 옵션
const operatingTimeOption = ref({
  title: {
    text: '로봇 운영 시간',
    left: 'center'
  },
  tooltip: {
    trigger: 'axis',
    formatter: '{b}: {c} 시간'
  },
  toolbox: {
    feature: {
      saveAsImage: { title: '이미지로 저장' }
    }
  },
  xAxis: {
    type: 'category',
    data: ['월', '화', '수', '목', '금', '토', '일'],
    axisLabel: { interval: 0 }
  },
  yAxis: {
    type: 'value',
    name: '운영 시간 (시간)',
    nameLocation: 'middle',
    nameGap: 50
  },
  series: [
    {
      name: 'Robot 1',
      type: 'line',
      smooth: true,
      data: [8, 7.5, 8.2, 7.8, 8.5, 6, 5],
      itemStyle: {
        color: '#409EFF'
      },
      areaStyle: {
        color: {
          type: 'linear',
          x: 0,
          y: 0,
          x2: 0,
          y2: 1,
          colorStops: [
            { offset: 0, color: 'rgba(64,158,255,0.3)' },
            { offset: 1, color: 'rgba(64,158,255,0.1)' }
          ]
        }
      }
    },
    {
      name: 'Robot 2',
      type: 'line',
      smooth: true,
      data: [7, 8, 7.8, 8.1, 7.5, 5.5, 4.8],
      itemStyle: {
        color: '#67C23A'
      },
      areaStyle: {
        color: {
          type: 'linear',
          x: 0,
          y: 0,
          x2: 0,
          y2: 1,
          colorStops: [
            { offset: 0, color: 'rgba(103,194,58,0.3)' },
            { offset: 1, color: 'rgba(103,194,58,0.1)' }
          ]
        }
      }
    }
  ]
})

// 특이사항 발생 차트 옵션
const incidentOption = ref({
  title: {
    text: '특이사항 발생 현황',
    left: 'center'
  },
  tooltip: {
    trigger: 'axis',
    axisPointer: {
      type: 'shadow'
    }
  },
  legend: {
    top: '10%'
  },
  grid: {
    left: '3%',
    right: '4%',
    bottom: '3%',
    top: '20%',
    containLabel: true
  },
  xAxis: {
    type: 'category',
    data: ['월', '화', '수', '목', '금', '토', '일']
  },
  yAxis: {
    type: 'value',
    name: '발생 건수'
  },
  series: [
    {
      name: '보안',
      type: 'bar',
      stack: 'total',
      emphasis: {
        focus: 'series'
      },
      data: [2, 1, 3, 0, 2, 1, 0]
    },
    {
      name: '안전',
      type: 'bar',
      stack: 'total',
      emphasis: {
        focus: 'series'
      },
      data: [1, 2, 1, 3, 1, 0, 1]
    },
    {
      name: '시스템',
      type: 'bar',
      stack: 'total',
      emphasis: {
        focus: 'series'
      },
      data: [0, 1, 0, 2, 1, 1, 0]
    }
  ]
})

// 배터리 사용 차트 옵션
const batteryOption = ref({
  title: {
    text: '배터리 사용 현황',
    left: 'center'
  },
  tooltip: {
    formatter: '{a} <br/>{b} : {c}%'
  },
  series: [
    {
      name: 'Robot 1',
      type: 'gauge',
      progress: {
        show: true,
        width: 18
      },
      axisLine: {
        lineStyle: {
          width: 18
        }
      },
      axisTick: {
        show: false
      },
      splitLine: {
        length: 15,
        lineStyle: {
          width: 2,
          color: '#999'
        }
      },
      pointer: {
        icon: 'path://M12.8,0.7l12,40.1H0.7L12.8,0.7z',
        length: '12%',
        width: 20,
        offsetCenter: [0, '-60%'],
        itemStyle: {
          color: 'inherit'
        }
      },
      axisLabel: {
        color: '#464646',
        fontSize: 20,
        distance: -60,
        formatter: function (value) {
          if (value === 0.875) {
            return '충전 중';
          }
          return '';
        }
      },
      detail: {
        valueAnimation: true,
        formatter: '{value}%',
        color: 'inherit'
      },
      data: [
        {
          value: 85,
          name: '배터리'
        }
      ]
    },
    {
      name: 'Robot 2',
      type: 'gauge',
      progress: {
        show: true,
        width: 18
      },
      axisLine: {
        lineStyle: {
          width: 18
        }
      },
      axisTick: {
        show: false
      },
      splitLine: {
        length: 15,
        lineStyle: {
          width: 2,
          color: '#999'
        }
      },
      pointer: {
        icon: 'path://M12.8,0.7l12,40.1H0.7L12.8,0.7z',
        length: '12%',
        width: 20,
        offsetCenter: [0, '-60%'],
        itemStyle: {
          color: 'inherit'
        }
      },
      axisLabel: {
        color: '#464646',
        fontSize: 20,
        distance: -60,
        formatter: function (value) {
          if (value === 0.875) {
            return '충전 중';
          }
          return '';
        }
      },
      detail: {
        valueAnimation: true,
        formatter: '{value}%',
        color: 'inherit'
      },
      data: [
        {
          value: 25,
          name: '배터리'
        }
      ]
    }
  ]
})

// WebSocket 연결 설정
let ws = null

const connectWebSocket = () => {
  ws = new WebSocket('ws://localhost:8080/stats')
  
  ws.onmessage = (event) => {
    const data = JSON.parse(event.data)
    updateChartData(data)
  }

  ws.onclose = () => {
    setTimeout(connectWebSocket, 3000)
  }
}

// 차트 데이터 업데이트
const updateChartData = (data) => {
  if (data.type === 'operating_time') {
    operatingTimeOption.value.series[0].data = data.robot1
    operatingTimeOption.value.series[1].data = data.robot2
  } else if (data.type === 'incidents') {
    incidentOption.value.series.forEach((series, index) => {
      series.data = data.incidents[series.name]
    })
  } else if (data.type === 'battery') {
    batteryOption.value.series[0].data[0].value = data.robot1
    batteryOption.value.series[1].data[0].value = data.robot2
  }
}

onMounted(() => {
  connectWebSocket()
})
</script>

<style scoped>
.stat-charts {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1rem;
  padding: 1rem;
}

.chart-container {
  background: white;
  border-radius: 8px;
  padding: 1rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.chart {
  height: 300px;
}

@media (max-width: 768px) {
  .stat-charts {
    grid-template-columns: 1fr;
  }
  
  .chart {
    height: 250px;
  }
}
</style> 