<template>
  <button>{{ text }}</button>
</template>

<script setup>
defineProps({
  text: String,
})
</script>

<style scoped>
button{
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
  width: 226;
  height: 45;
  border-radius: 51px;
  padding: 10px 50px;
  background: #ffffff;
  color: #6AB23D;
  font-weight: 400;
  font-size: 20px;
  border: 1px solid #6AB23D;
  transition: all 0.5s ease;
}

button:hover{
  color: white;
  background: #6AB23D;
}

button:active{
  color: white;
  background: linear-gradient(90deg, #365e48 0%, #6ab23d 100%);
}
</style>
