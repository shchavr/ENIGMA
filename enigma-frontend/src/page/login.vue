<template>
  <div class="login-wrapper">
    <form @submit.prevent="handleSubmit">
      <h2>Вход</h2>
      <input 
        type="text" 
        placeholder="Логин*" 
        v-model="formData.email"
        required
        autocomplete="off"
      />
      <input 
        type="password" 
        placeholder="Пароль"
        v-model="formData.password"
        required
        autocomplete="off"
      >
      <Button text="Войти"/>

      {{ errorMessage }}
    </form>
    <div class="line-background">
      <img src="../assets/Vector.png" alt="">
    </div>
  </div>
</template>

<script setup>
import Button from '../components/button.vue';
import { useDataStore } from '../stores/counter';
import { useRouter } from 'vue-router';
import { ref } from 'vue';

const store = useDataStore();
const router = useRouter();

const formData = ref({
  email: '',
  password: ''
});

const errorMessage = ref('')


const handleSubmit = async () => {
  try {
    const loginFormData = new FormData()
    loginFormData.append('username', formData.value.email)  // бэкенд ждет username
    loginFormData.append('password', formData.value.password)

    console.log

    await store.PostLogin(loginFormData);

    router.push('/');
  } catch (error) {
    if (error.response?.status === 401) {
      errorMessage.value = 'Неверный email или пароль'
      console.error('Неверные данные:', error.response?.data?.detail || error.message)
    } else if (error.response?.status === 403) {
      errorMessage.value = 'Пользователь заблокирован'
    } else {
      errorMessage.value = 'Произошла ошибка при входе'
      console.error('Произошла ошибка:', error)
    }
    console.error('Ошибка входа:', error)
  }
};
</script>

<style scoped>
.login-wrapper {
  width: 100%;
  min-height: 98vh;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  overflow: hidden;
}

.line-background {
  content: '';
  background-image: url(../assets/Vector.png);
  background-repeat: no-repeat;
  background-size: cover;
  position: absolute;
  z-index: -1;
  top: -80px;
  right: -80px;
}


form {
  display: flex;
  flex-direction: column;
  justify-content: center;
  border: 1px solid #365e48;
  border-radius: 14px;
  gap: 40px;
  padding: 45px;
  width: 579px;
  height: 387px;
  box-shadow: 0 4px 13px 0 rgba(0, 0, 0, 0.25);
  background: rgba(255, 255, 255, 0.1);
}

label {
    display: block;
    font-size: 20px;
    margin-bottom: 8px;
}

input {
    width: 100%;
    border: none;
    border-bottom: 2px solid #999;
    font-size: 20px;
    background: transparent;
    font-size: 18px;
    padding: 5px 0;
    outline: none;
}

input:focus {
    border-bottom: 2px solid #000;
}
</style>