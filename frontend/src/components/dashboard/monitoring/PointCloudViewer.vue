<template>
  <div class="point-cloud-container">
    <div class="controls">
      <button @click="resetCamera">카메라 초기화</button>
      <button @click="toggleRotation">회전 {{ isRotating ? '중지' : '시작' }}</button>
    </div>
    <div ref="container" class="viewer"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';

const container = ref(null);
const isRotating = ref(false);
let scene, camera, renderer, controls;
let points;
let ws = null;
let reconnectAttempts = 0;
const maxReconnectAttempts = 5;

const initThree = () => {
  scene = new THREE.Scene();
  camera = new THREE.PerspectiveCamera(75, container.value.clientWidth / container.value.clientHeight, 0.1, 2000);
  
  renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setSize(container.value.clientWidth, container.value.clientHeight);
  container.value.appendChild(renderer.domElement);
  
  // 카메라 위치를 더 멀리 이동
  camera.position.set(200, 200, 200);
  camera.lookAt(0, 0, 0);
  
  // 컨트롤 추가
  controls = new OrbitControls(camera, renderer.domElement);
  
  // 그리드 헬퍼 크기 증가
  const gridHelper = new THREE.GridHelper(400, 20);
  scene.add(gridHelper);
  
  // 축 헬퍼 크기 증가
  const axesHelper = new THREE.AxesHelper(100);
  scene.add(axesHelper);
  
  // 포인트 클라우드 초기화
  const geometry = new THREE.BufferGeometry();
  const material = new THREE.PointsMaterial({
    size: 2, // 포인트 크기 증가
    vertexColors: true,
    sizeAttenuation: true
  });
  
  pointCloud = new THREE.Points(geometry, material);
  scene.add(pointCloud);
  
  animate();
};

const connectWebSocket = () => {
  if (ws && ws.readyState === WebSocket.OPEN) {
    console.log('WebSocket이 이미 연결되어 있습니다.');
    return;
  }

  try {
    ws = new WebSocket('ws://localhost:8080/ws/sensor/ROBOT_001');
    
    ws.onopen = () => {
      console.log('센서 WebSocket 연결 성공');
      reconnectAttempts = 0;
      
      // 더미 데이터 전송 간격을 500ms로 단축
      setInterval(() => {
        updateLidarData(generateDummyLidarData());
      }, 500);
    };

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        console.log('센서 데이터 수신:', data);
        
        // LiDAR 데이터 처리
        if (data.lidar_data && data.lidar_data.points) {
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
        console.error('데이터 처리 중 오류 발생:', error);
      }
    };

    ws.onerror = (error) => {
      console.error('WebSocket 에러:', error);
    };

    ws.onclose = () => {
      console.log('WebSocket 연결 종료');
      if (reconnectAttempts < maxReconnectAttempts) {
        reconnectAttempts++;
        console.log(`재연결 시도 ${reconnectAttempts}/${maxReconnectAttempts}`);
        setTimeout(connectWebSocket, 3000);
      } else {
        console.log('최대 재연결 시도 횟수 초과');
      }
    };
  } catch (error) {
    console.error('WebSocket 연결 시도 중 오류 발생:', error);
  }
};

const updatePointCloud = (points) => {
  if (!scene) return;
  
  // 기존 포인트 클라우드 제거
  if (scene.getObjectByName('pointCloud')) {
    scene.remove(scene.getObjectByName('pointCloud'));
  }
  
  const geometry = new THREE.BufferGeometry();
  const positions = new Float32Array(points.length * 3);
  const colors = new Float32Array(points.length * 3);
  
  points.forEach((point, i) => {
    positions[i * 3] = point.x;
    positions[i * 3 + 1] = point.y;
    positions[i * 3 + 2] = point.z;
    
    // intensity를 색상으로 변환
    colors[i * 3] = point.intensity;
    colors[i * 3 + 1] = point.intensity;
    colors[i * 3 + 2] = point.intensity;
  });
  
  geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  
  const material = new THREE.PointsMaterial({
    size: 0.1,
    vertexColors: true
  });
  
  points = new THREE.Points(geometry, material);
  points.name = 'pointCloud';
  scene.add(points);
};

const animate = () => {
  requestAnimationFrame(animate);
  
  if (isRotating.value && points) {
    points.rotation.y += 0.01;
  }
  
  renderer.render(scene, camera);
};

const resetCamera = () => {
  camera.position.set(10, 10, 10);
  camera.lookAt(0, 0, 0);
  controls.reset();
};

const toggleRotation = () => {
  isRotating.value = !isRotating.value;
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
  
  if (validPoints.length === 0) {
    console.warn('유효한 포인트가 없습니다.');
    return;
  }

  if (scene && pointCloud) {
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
  }
};

// updateRobotPosition 함수 추가
const updateRobotPosition = (data) => {
  console.log('로봇 위치 업데이트:', data);
  // 3D 뷰에서는 로봇 위치 표시가 필요 없으므로 로그만 출력
};

// 더미 LiDAR 데이터 생성 함수 수정
const generateDummyLidarData = () => {
  const points = [];
  const numPoints = 1000;
  
  for (let i = 0; i < numPoints; i++) {
    const angle = (Math.PI * 2 * i) / numPoints;
    const radius = 100 + Math.random() * 100; // 반경을 100~200으로 증가
    const height = Math.random() * 50 - 25; // 높이 범위도 증가 (-25~25)
    
    points.push([
      radius * Math.cos(angle),
      radius * Math.sin(angle),
      height
    ]);
  }
  return points;
};

onMounted(() => {
  initThree();
  const ws = connectWebSocket();
  
  window.addEventListener('resize', () => {
    if (!container.value) return;
    camera.aspect = container.value.clientWidth / container.value.clientHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(container.value.clientWidth, container.value.clientHeight);
  });
  
  onUnmounted(() => {
    if (ws) {
      ws.close();
    }
  });
});

onUnmounted(() => {
  if (renderer) {
    renderer.dispose();
    container.value?.removeChild(renderer.domElement);
  }
});
</script>

<style scoped>
.point-cloud-container {
  width: 100%;
  height: 100%;
  position: relative;
}

.viewer {
  width: 100%;
  height: 100%;
  background: #1a1a1a;
}

.controls {
  position: absolute;
  top: 10px;
  left: 10px;
  z-index: 1;
  display: flex;
  gap: 10px;
}

.controls button {
  padding: 8px 16px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: white;
  border-radius: 4px;
  cursor: pointer;
  transition: background 0.3s;
}

.controls button:hover {
  background: rgba(255, 255, 255, 0.2);
}
</style> 