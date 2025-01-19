import cv2
import time

def test_camera():
    print("카메라 테스트 시작...")
    
    # 카메라 초기화
    cap = cv2.VideoCapture(0)
    print("\n1. 카메라 초기화")
    print(f"- 연결 상태: {'성공' if cap.isOpened() else '실패'}")
    
    if not cap.isOpened():
        print("카메라를 열 수 없습니다!")
        return
    
    # 카메라 속성 확인
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    
    print("\n2. 카메라 속성")
    print(f"- 해상도: {width}x{height}")
    print(f"- FPS: {fps}")
    
    # 프레임 읽기 테스트
    print("\n3. 프레임 읽기 테스트")
    success = True
    for i in range(10):  # 10프레임 테스트
        ret, frame = cap.read()
        if not ret:
            success = False
            print(f"- {i+1}번째 프레임 읽기 실패")
            break
        print(f"- {i+1}번째 프레임 읽기 성공 (크기: {frame.shape})")
        time.sleep(0.1)  # 100ms 대기
    
    print(f"\n테스트 결과: {'성공' if success else '실패'}")
    
    # 카메라 해제
    cap.release()
    print("\n카메라 해제 완료")

if __name__ == "__main__":
    test_camera() 