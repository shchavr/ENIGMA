<script setup>
import { RouterView } from 'vue-router'
</script>

<template>
  <router-view />
</template>

<style scoped>
.p-datatable {
    margin: 1rem;
    background: white;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.p-datatable .p-datatable-thead > tr > th {
    background: #f8fafc;
    padding: 1rem;
    font-weight: 600;
    text-align: left;
    border-bottom: 2px solid #e2e8f0;
}

.p-datatable .p-datatable-tbody > tr > td {
    padding: 1rem;
    border-bottom: 1px solid #e2e8f0;
}

.p-datatable .p-sortable-column:hover {
    background: #f1f5f9;
    cursor: pointer;
}
</style>
