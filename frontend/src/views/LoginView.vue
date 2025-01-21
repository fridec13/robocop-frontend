<template>
  <div class="login-container" :class="{ 'dark-mode': isDarkMode }">
    <div class="left-column">
      <img src="@/assets/logo.png" alt="Robocop Logo" class="logo">
      <div class="slogan">
        <h2>세상에 없던</h2>
        <h2>자율 무인 경비로봇 시스템</h2>
        <h2>ROBOCOP이 만들어갑니다!</h2>
      </div>
    </div>
    <div class="right-column">
      <div class="login-form">
        <h3>아이디</h3>
        <input type="text" v-model="loginForm.username" placeholder="ID를 입력해주세요">
        <h3>비밀번호</h3>
        <input type="password" v-model="loginForm.password" placeholder="비밀번호">
        <input type="text" v-model="loginForm.captcha" placeholder="캡스워드를 입력해주세요">
        <button @click="handleLogin" class="login-button">로그인</button>
      </div>
    </div>
  </div>
</template>
192.168.100.103
<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const loginForm = ref({
  username: '',
  password: '',
  captcha: ''
})

const isDarkMode = ref(localStorage.getItem('darkMode') === 'true')

const toggleTheme = () => {
  isDarkMode.value = !isDarkMode.value
  localStorage.setItem('darkMode', isDarkMode.value)
}

onMounted(() => {
  // 페이지 로드 시 저장된 테마 설정 적용
  const savedTheme = localStorage.getItem('darkMode')
  if (savedTheme !== null) {
    isDarkMode.value = savedTheme === 'true'
  }
})

const handleLogin = async () => {
  try {
    // TODO: 실제 로그인 API 호출로 대체
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // 로그인 성공 처리
    localStorage.setItem('isAuthenticated', 'true')
    
    // 대시보드(모니터링)로 이동
    router.push({ name: 'monitoring' })
  } catch (error) {
    console.error('로그인 실패:', error)
    alert('로그인에 실패했습니다. 다시 시도해주세요.')
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  height: 100vh;
  min-width: fit-content;
  position: relative;
  background-color: #ffffff;
  transition: all 0.3s ease;
}

.login-container.dark-mode {
  background-color: #1a1a1a;
  color: #ffffff;
}

.theme-toggle {
  position: absolute;
  top: 20px;
  right: 20px;
  z-index: 1000;
}

.theme-button {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  padding: 8px;
  border-radius: 50%;
  transition: background-color 0.3s ease;
}

.theme-button:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.left-column {
  width: 50%;
  flex: 1 1 50%;
  min-width: 600px;
  background-color: #f5f5f5;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  transition: background-color 0.3s ease;
}

.dark-mode .left-column {
  background-color: #2a2a2a;
}

.logo {
  width: 200px;
  margin-bottom: 2rem;
}

.slogan {
  text-align: center;
  color: #333;
  transition: color 0.3s ease;
}

.dark-mode .slogan {
  color: #ffffff;
}

.slogan h2 {
  margin-bottom: 0.5rem;
  font-size: 1.5rem;
}

.right-column {
  width: 50%;
  flex: 1 1 50%;
  min-width: 600px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  background-color: #ffffff;
  transition: background-color 0.3s ease;
}

.dark-mode .right-column {
  background-color: #1a1a1a;
}

.login-form {
  width: 80%;
  max-width: 400px;
}

.login-form h3 {
  margin-bottom: 0.5rem;
  color: #333;
  transition: color 0.3s ease;
}

.dark-mode .login-form h3 {
  color: #ffffff;
}

.login-form input {
  width: 100%;
  padding: 0.8rem;
  margin-bottom: 1rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: #ffffff;
  color: #333;
  transition: all 0.3s ease;
}

.dark-mode .login-form input {
  background-color: #2a2a2a;
  border-color: #444;
  color: #ffffff;
}

.dark-mode .login-form input::placeholder {
  color: #888;
}

.login-button {
  width: 100%;
  padding: 1rem;
  background-color: #000;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s ease;
}

.dark-mode .login-button {
  background-color: #007bff;
}

.login-button:hover {
  background-color: #333;
}

.dark-mode .login-button:hover {
  background-color: #0056b3;
}

/* 태블릿 크기 */
@media (max-width: 1024px) {
  .slogan h2 {
    font-size: 1.2rem;
  }
  
  .logo {
    width: 150px;
  }
  
  .login-form {
    width: 90%;
  }
}

/* 모바일 크기 */
@media (max-width: 768px) {
  .login-container {
    flex-direction: column;
    height: auto;
    min-height: 100vh;
  }
  
  .left-column, .right-column {
    width: 100%;
    min-width: 0;
    flex: none;
  }
  
  .left-column {
    padding: 2rem 1rem;
  }
  
  .logo {
    width: 120px;
    margin-bottom: 1rem;
  }
  
  .slogan h2 {
    font-size: 1rem;
  }
  
  .right-column {
    padding: 1rem;
  }
  
  .login-form {
    width: 100%;
  }
  
  .login-form input {
    padding: 0.6rem;
  }
  
  .login-button {
    padding: 0.8rem;
  }
}

/* 스크롤바 스타일링 */
.dark-mode ::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

.dark-mode ::-webkit-scrollbar-track {
  background: #2a2a2a;
}

.dark-mode ::-webkit-scrollbar-thumb {
  background: #666;
  border-radius: 4px;
}

.dark-mode ::-webkit-scrollbar-thumb:hover {
  background: #888;
}
</style> 