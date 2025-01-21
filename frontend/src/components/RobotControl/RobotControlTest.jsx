import React, { useState, useEffect } from 'react';
import { RobotControl } from '../../services/websocket/robotControl';
import './RobotControlTest.css';

export function RobotControlTest() {
    const [robotId, setRobotId] = useState('');
    const [isConnected, setIsConnected] = useState(false);
    const [controlInstance, setControlInstance] = useState(null);
    const [lastCommand, setLastCommand] = useState(null);
    const [error, setError] = useState(null);

    // 연결 상태에 따른 스타일 클래스
    const statusClass = isConnected ? 'status-connected' : 'status-disconnected';

    const handleConnect = () => {
        if (!robotId) {
            setError('로봇 ID를 입력해주세요');
            return;
        }

        const control = new RobotControl(robotId, {
            onConnect: () => {
                setIsConnected(true);
                setError(null);
            },
            onDisconnect: () => {
                setIsConnected(false);
            },
            onError: (error) => {
                setError(error);
            },
            onFeedback: (data) => {
                setLastCommand({
                    linear: data.twist.linear.x.toFixed(2),
                    angular: data.twist.angular.z.toFixed(2),
                    keys: data.pressed_keys
                });
            }
        });

        control.connect();
        setControlInstance(control);
    };

    const handleDisconnect = () => {
        if (controlInstance) {
            controlInstance.disconnect();
            setControlInstance(null);
            setIsConnected(false);
        }
    };

    useEffect(() => {
        return () => {
            if (controlInstance) {
                controlInstance.disconnect();
            }
        };
    }, [controlInstance]);

    return (
        <div className="robot-control-test">
            <h2>로봇 제어 테스트</h2>
            
            <div className="connection-panel">
                <input
                    type="text"
                    value={robotId}
                    onChange={(e) => setRobotId(e.target.value)}
                    placeholder="로봇 ID 입력"
                    disabled={isConnected}
                />
                {!isConnected ? (
                    <button onClick={handleConnect}>연결</button>
                ) : (
                    <button onClick={handleDisconnect}>연결 해제</button>
                )}
            </div>

            <div className={`status-panel ${statusClass}`}>
                <div className="status-indicator">
                    상태: {isConnected ? '연결됨' : '연결 끊김'}
                </div>
                {error && <div className="error-message">{error}</div>}
            </div>

            {isConnected && (
                <div className="control-info">
                    <h3>조작 방법</h3>
                    <ul>
                        <li>↑: 전진</li>
                        <li>↓: 후진</li>
                        <li>←: 좌회전</li>
                        <li>→: 우회전</li>
                        <li>방향키 동시 입력: 대각선 이동</li>
                    </ul>
                </div>
            )}

            {lastCommand && (
                <div className="command-feedback">
                    <h3>현재 명령</h3>
                    <div>선속도: {lastCommand.linear} m/s</div>
                    <div>각속도: {lastCommand.angular} rad/s</div>
                    <div>눌린 키: {lastCommand.keys.join(', ')}</div>
                </div>
            )}
        </div>
    );
} 