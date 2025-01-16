<template>
  <div class="login-container">
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

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const loginForm = ref({
  username: '',
  password: '',
  captcha: ''
})

const handleLogin = async () => {
  // TODO: Implement login logic
  try {
    // API call would go here
    router.push('/dashboard')
  } catch (error) {
    console.error('Login failed:', error)
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
}

.logo {
  width: 200px;
  margin-bottom: 2rem;
}

.slogan {
  text-align: center;
  color: #333;
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
}

.login-form {
  width: 80%;
  max-width: 400px;
}

.login-form h3 {
  margin-bottom: 0.5rem;
  color: #333;
}

.login-form input {
  width: 100%;
  padding: 0.8rem;
  margin-bottom: 1rem;
  border: 1px solid #ddd;
  border-radius: 4px;
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
}

.login-button:hover {
  background-color: #333;
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
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
}

::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #555;
}
</style> 