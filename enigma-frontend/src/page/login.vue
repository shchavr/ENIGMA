<template>
  <div class="login-wrapper">
    <form action="post">
      <h2>Вход</h2>
      <input type="text" id="login" placeholder="Логин*" />
      <input type="password" placeholder="Пароль">
      <Button text="Войти"/>
    </form>
  </div>
</template>

<script setup>
import Button from '../components/button.vue';
</script>

<style scoped>
.login-wrapper {
  width: 100%;
  min-height: 98vh;
  display: flex;
  justify-content: center;
  align-items: center;
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