<template>
  <div class="page-wrapper">
    <HeaderVue/>
    <div class="background-img">
      <img src="../assets/Vector2.png" alt="">
    </div>
    <div class="content-wrapper">
      <h2>Аналитика</h2>
      <div class="table-wrapper">
        <div class="card">
          <Chart type="bar" :data="chartData" :options="chartOptions" style="height: 600px" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from "vue";
import { useDataStore } from '../stores/counter';
import Chart from "primevue/chart";
import HeaderVue from "../components/HeaderVue.vue";

const store = useDataStore();
const map = computed(() => store.getMap);

onMounted(() => {
    store.FetchHitMap();
});

// 👇 создаём "растянутый" февраль
const chartData = computed(() => {
    if (!map.value) return null;

    return {
        labels: map.value.map(item => item.device_model),
        datasets: [
            {
                label: 'Количество проблем (Февраль)',
                data: map.value.map(item => item.problem_count)
            }
        ]
    };
});

const chartOptions = {
    maintainAspectRatio: false,
};
</script>

<style scoped>
.page-wrapper {
  width: 100%;
  min-height: 98vh;
  display: flex;
  justify-content: center;
  align-items: stretch;
  position: relative;
  overflow: hidden;
  padding: 80px 40px;
}

:deep(.table-wrapper) {
  height: 700px;
}

.background-img {
  position: absolute;
  z-index: -1;
  top: -80px;
  right: -80px;
}

.content-wrapper {
  width: 100%;
}

h2 {
  margin-bottom: 20px;
}
</style>