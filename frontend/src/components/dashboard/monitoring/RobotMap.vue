<template>
  <div class="robot-map">
    <div class="map-header">
      <h4>실시간 로봇 위치</h4>
      <div class="map-controls">
        <button @click="toggleMapType" class="map-type-btn">
          {{ isPointCloud ? '2D 맵' : '포인트 클라우드' }}
        </button>
        <button @click="resetView" class="reset-btn">
          <span class="reset-icon">⟲</span>
        </button>
      </div>
    </div>

    <!-- 2D Canvas 맵 -->
    <canvas
      ref="mapCanvas"
      class="map-canvas"
      :class="{ hidden: isPointCloud }"
      @wheel="handleZoom"
      @mousedown="startPan"
      @mousemove="pan"
      @mouseup="endPan"
      @mouseleave="endPan"
    ></canvas>

    <!-- Three.js 포인트 클라우드 뷰 -->
    <div
      ref="pointCloudContainer"
      class="point-cloud-container"
      :class="{ hidden: !isPointCloud }"
    ></div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import * as THREE from 'three'
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls'

// 상태 관리
const isPointCloud = ref(false)
const mapCanvas = ref(null)
const pointCloudContainer = ref(null)
const isPanning = ref(false)
const lastPos = ref({ x: 0, y: 0 })
const scale = ref(1)
const offset = ref({ x: 0, y: 0 })

// Three.js 관련 변수
let scene, camera, renderer, controls, pointCloud

// 2D 맵 관련
const mapData = ref({
  width: 1000,  // 실제 공간의 너비 (cm)
  height: 1000, // 실제 공간의 높이 (cm)
  resolution: 5 // 1픽셀당 cm
})

// 로봇 위치 데이터
const robotPositions = ref([
  {
    id: 'ROBOT_001',
    x: 0,
    y: 0,
    heading: 0
  }
])

// LiDAR 데이터 (예시)
const lidarData = ref({
  points: [], // [x, y, z] 좌표 배열
  intensity: [] // 각 포인트의 강도값
})

// WebSocket 연결 관리
let ws = null
let reconnectAttempts = 0
const MAX_RECONNECT_ATTEMPTS = 5

// 더미 LiDAR 데이터 생성
const generateDummyLidarData = () => {
  const points = [];
  const numPoints = 1000;
  
  for (let i = 0; i < numPoints; i++) {
    const angle = (Math.PI * 2 * i) / numPoints;
    const radius = 2 + Math.random() * 2; // 2~4m 반경
    const height = Math.random() * 2 - 1; // -1~1m 높이
    
    points.push([
      radius * Math.cos(angle),
      radius * Math.sin(angle),
      height
    ]);
  }
  return points;
};

const connectWebSocket = () => {
  if (ws && ws.readyState === WebSocket.OPEN) {
    console.log('WebSocket이 이미 연결되어 있습니다.');
    return;
  }

  try {
    ws = new WebSocket('ws://localhost:8080/ws/sensor/ROBOT_001');
    
    ws.onopen = () => {
      console.log('맵 WebSocket 연결 성공');
      reconnectAttempts = 0;
      
      // 연결 성공 시 더미 데이터 전송 시작
      setInterval(() => {
        updateLidarData(generateDummyLidarData());
      }, 1000);
    };

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        
        // LiDAR 데이터 처리
        if (data.lidar_data) {
          const points = data.lidar_data.points.map(point => [point.x, point.y, point.z]);
          updateLidarData(points);
        }
        
        // 로봇 위치 업데이트
        if (data.position) {
          updateRobotPosition({
            robotId: data.robot_id,
            x: data.position.x,
            y: data.position.y,
            heading: data.position.orientation
          });
        }
      } catch (error) {
        console.error('데이터 처리 중 오류:', error);
      }
    };

    ws.onerror = (error) => {
      console.error('맵 WebSocket 에러:', error);
    };

    ws.onclose = () => {
      console.log('맵 WebSocket 연결 끊김');
      if (reconnectAttempts < MAX_RECONNECT_ATTEMPTS) {
        reconnectAttempts++;
        setTimeout(connectWebSocket, 3000);
      }
    };
  } catch (error) {
    console.error('WebSocket 연결 실패:', error);
  }
};

// 2D 맵 렌더링
const render2DMap = () => {
  if (!mapCanvas.value) {
    console.warn('맵 캔버스가 준비되지 않았습니다.');
    return;
  }

  const ctx = mapCanvas.value.getContext('2d')
  const canvas = mapCanvas.value
  
  // 캔버스 크기 설정
  canvas.width = canvas.clientWidth || 800  // 기본값 설정
  canvas.height = canvas.clientHeight || 600
  
  // 배경 지우기
  ctx.fillStyle = '#f8f9fa'
  ctx.fillRect(0, 0, canvas.width, canvas.height)
  
  // 변환 매트릭스 적용
  ctx.save()
  ctx.translate(canvas.width/2 + offset.value.x, canvas.height/2 + offset.value.y)
  ctx.scale(scale.value, scale.value)
  
  // 그리드 그리기
  ctx.strokeStyle = '#ddd'
  ctx.lineWidth = 1 / scale.value
  const gridSize = 50 // cm
  const gridCount = 20 // 그리드 개수
  const gridExtent = gridSize * gridCount / 2
  
  for (let x = -gridExtent; x <= gridExtent; x += gridSize) {
    ctx.beginPath()
    ctx.moveTo(x, -gridExtent)
    ctx.lineTo(x, gridExtent)
    ctx.stroke()
  }
  for (let y = -gridExtent; y <= gridExtent; y += gridSize) {
    ctx.beginPath()
    ctx.moveTo(-gridExtent, y)
    ctx.lineTo(gridExtent, y)
    ctx.stroke()
  }
  
  // LiDAR 포인트 그리기
  ctx.fillStyle = 'rgba(0, 123, 255, 0.5)'
  for (const point of lidarData.value.points) {
    ctx.beginPath()
    ctx.arc(point[0], point[1], 2 / scale.value, 0, Math.PI * 2)
    ctx.fill()
  }
  
  // 로봇 그리기
  for (const robot of robotPositions.value) {
    ctx.save()
    ctx.translate(robot.x, robot.y)
    ctx.rotate((robot.heading * Math.PI) / 180)
    
    // 로봇 본체
    ctx.fillStyle = '#28a745'
    ctx.beginPath()
    ctx.arc(0, 0, 20 / scale.value, 0, Math.PI * 2)
    ctx.fill()
    
    // 방향 표시
    ctx.strokeStyle = '#fff'
    ctx.lineWidth = 2 / scale.value
    ctx.beginPath()
    ctx.moveTo(0, 0)
    ctx.lineTo(20 / scale.value, 0)
    ctx.stroke()
    
    ctx.restore()
  }
  
  ctx.restore()
}

// Three.js 포인트 클라우드 설정
const setupPointCloud = () => {
  if (!pointCloudContainer.value) {
    console.error('포인트 클라우드 컨테이너가 준비되지 않았습니다.');
    return;
  }

  // Scene 초기화
  scene = new THREE.Scene();
  scene.background = new THREE.Color(0xf8f9fa);
  
  const containerWidth = pointCloudContainer.value.clientWidth || window.innerWidth;
  const containerHeight = pointCloudContainer.value.clientHeight || window.innerHeight;
  
  // 카메라 설정
  camera = new THREE.PerspectiveCamera(75, containerWidth / containerHeight, 0.1, 1000);
  camera.position.set(5, 5, 5);
  camera.lookAt(0, 0, 0);
  
  // 렌더러 설정
  renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setSize(containerWidth, containerHeight);
  pointCloudContainer.value.innerHTML = ''; // 기존 요소 제거
  pointCloudContainer.value.appendChild(renderer.domElement);
  
  // 컨트롤 설정
  controls = new OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;
  controls.dampingFactor = 0.05;
  
  // 그리드 헬퍼 추가
  const gridHelper = new THREE.GridHelper(20, 20);
  scene.add(gridHelper);
  
  // 축 헬퍼 추가
  const axesHelper = new THREE.AxesHelper(5);
  scene.add(axesHelper);
  
  // 포인트 클라우드 생성
  const geometry = new THREE.BufferGeometry();
  const material = new THREE.PointsMaterial({
    size: 0.05,
    vertexColors: true,
    sizeAttenuation: true
  });
  
  pointCloud = new THREE.Points(geometry, material);
  scene.add(pointCloud);
  
  // 애니메이션 루프
  const animate = () => {
    requestAnimationFrame(animate);
    controls.update();
    renderer.render(scene, camera);
  };
  animate();
};

// LiDAR 데이터 업데이트
const updateLidarData = (points) => {
  // 유효하지 않은 데이터 필터링
  const validPoints = points.filter(point => 
    point && 
    Array.isArray(point) && 
    point.length === 3 && 
    point.every(coord => typeof coord === 'number' && !isNaN(coord))
  );

  lidarData.value.points = validPoints;
  
  if (isPointCloud.value && scene && pointCloud) {
    // Three.js 포인트 클라우드 업데이트
    if (validPoints.length === 0) {
      console.warn('유효한 포인트 데이터가 없습니다.');
      return;
    }

    const positions = new Float32Array(validPoints.length * 3);
    const colors = new Float32Array(validPoints.length * 3);
    
    validPoints.forEach((point, i) => {
      positions[i * 3] = point[0];
      positions[i * 3 + 1] = point[1];
      positions[i * 3 + 2] = point[2];
      
      // 높이에 따른 색상 설정 (파란색 -> 빨간색)
      const height = Math.max(-5, Math.min(5, point[2]));  // -5 ~ 5 범위로 제한
      const normalizedHeight = (height + 5) / 10;  // 0 ~ 1로 정규화
      const color = new THREE.Color();
      color.setHSL(normalizedHeight * 0.3 + 0.6, 1, 0.5);
      
      colors[i * 3] = color.r;
      colors[i * 3 + 1] = color.g;
      colors[i * 3 + 2] = color.b;
    });
    
    pointCloud.geometry.setAttribute(
      'position',
      new THREE.BufferAttribute(positions, 3)
    );
    pointCloud.geometry.setAttribute(
      'color',
      new THREE.BufferAttribute(colors, 3)
    );
    
    // boundingSphere 계산 전에 position 속성이 있는지 확인
    if (pointCloud.geometry.attributes.position) {
      pointCloud.geometry.computeBoundingSphere();
    }
  } else if (!isPointCloud.value) {
    render2DMap();
  }
};

// 로봇 위치 업데이트
const updateRobotPosition = (data) => {
  const index = robotPositions.value.findIndex(r => r.id === data.robotId)
  if (index !== -1) {
    // 좌표계 변환: 미터 단위를 센티미터로 변환 (x100)
    robotPositions.value[index] = {
      ...robotPositions.value[index],
      x: data.x * 100,  // 미터를 센티미터로 변환
      y: data.y * 100,
      heading: data.heading
    }
    console.log('로봇 위치 업데이트:', robotPositions.value[index]);
  }
  
  if (!isPointCloud.value) {
    render2DMap()
  }
}

// 이벤트 핸들러
const toggleMapType = () => {
  isPointCloud.value = !isPointCloud.value;
  if (isPointCloud.value) {
    // nextTick을 사용하여 DOM 업데이트 후 Three.js 초기화
    nextTick(() => {
      if (!scene) {
        setupPointCloud();
      }
    });
  }
};

const handleZoom = (e) => {
  if (isPointCloud.value) return
  
  e.preventDefault()
  const delta = e.deltaY > 0 ? 0.9 : 1.1
  scale.value = Math.max(0.5, Math.min(5, scale.value * delta))
  render2DMap()
}

const startPan = (e) => {
  if (isPointCloud.value) return
  
  isPanning.value = true
  lastPos.value = {
    x: e.clientX - offset.value.x,
    y: e.clientY - offset.value.y
  }
}

const pan = (e) => {
  if (!isPanning.value || isPointCloud.value) return
  
  offset.value = {
    x: e.clientX - lastPos.value.x,
    y: e.clientY - lastPos.value.y
  }
  render2DMap()
}

const endPan = () => {
  isPanning.value = false
}

const resetView = () => {
  if (isPointCloud.value) {
    camera.position.set(0, 3, 5)
    camera.lookAt(0, 0, 0)
    controls.reset()
  } else {
    scale.value = 1
    offset.value = { x: 0, y: 0 }
    render2DMap()
  }
}

// 라이프사이클 훅
onMounted(async () => {
  await nextTick();
  if (mapCanvas.value) {
    render2DMap();
  }
  connectWebSocket();
  
  // 리사이즈 이벤트 핸들러
  window.addEventListener('resize', () => {
    if (isPointCloud.value && renderer && pointCloudContainer.value) {
      const width = pointCloudContainer.value.clientWidth;
      const height = pointCloudContainer.value.clientHeight;
      
      camera.aspect = width / height;
      camera.updateProjectionMatrix();
      renderer.setSize(width, height);
    }
    render2DMap();
  })
})

onUnmounted(() => {
  if (ws) {
    ws.close();
  }
  
  // renderer가 존재하고 DOM에 추가된 상태인 경우에만 제거
  if (renderer && pointCloudContainer.value && renderer.domElement.parentNode) {
    renderer.dispose();
    pointCloudContainer.value.removeChild(renderer.domElement);
  }
})
</script>

<style scoped>
.robot-map {
  height: 300px;
  background: #fff;
  border-radius: 8px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.map-header {
  padding: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #dee2e6;
}

.map-controls {
  display: flex;
  gap: 0.5rem;
}

.map-type-btn,
.reset-btn {
  padding: 0.25rem 0.5rem;
  border: 1px solid #dee2e6;
  border-radius: 4px;
  background: #fff;
  cursor: pointer;
  font-size: 0.875rem;
}

.reset-icon {
  display: inline-block;
}

.map-canvas,
.point-cloud-container {
  flex: 1;
  width: 100%;
}

.hidden {
  display: none;
}

/* 모바일 대응 */
@media (max-width: 768px) {
  .robot-map {
    height: 250px;
  }
}
</style>

<!-- 
지도/위치 기능 구현 방법 및 고려사항:

1. LiDAR 데이터 처리
- 포인트 클라우드 데이터 실시간 수신
- 데이터 필터링 및 노이즈 제거
- 좌표계 변환 및 정규화

2. 시각화 방식
- 2D 맵: Canvas API 사용
  - 그리드 표시
  - 로봇 위치 및 방향 표시
  - LiDAR 스캔 포인트 표시
  - 줌/팬 기능

- 3D 포인트 클라우드: Three.js 사용
  - 실시간 포인트 클라우드 렌더링
  - 색상을 통한 높이 정보 표현
  - 카메라 컨트롤 (OrbitControls)

3. 성능 최적화
- WebGL 렌더링 최적화
- 포인트 클라우드 데시메이션
- 뷰포트 컬링
- 메모리 관리

4. 데이터 동기화
- WebSocket을 통한 실시간 데이터 수신
- 위치 데이터와 LiDAR 데이터 통합
- 타임스탬프 기반 동기화

5. 사용자 인터랙션
- 맵 타입 전환 (2D/3D)
- 줌/팬/회전 컨트롤
- 뷰 리셋 기능

6. 확장성
- 다중 로봇 지원
- 경로 계획 시각화
- 장애물 탐지 및 표시
--> 