<template>
  <div class="page-wrapper">
    <div class="background-img">
      <img src="../assets/Vector2.png" alt="">
    </div>
    <div class="content-wrapper">
      <h2>История обращений</h2>
      <div class="table-wrapper">
        <DataTable
          class="custom-table"
          v-model:filters="filters"
          :value="emails"
          :globalFilterFields="['date', 'full_name', 'object', 'phone', 'email', 'serial_numbers', 'category', 'sentiment', 'status']"
          removableSort
          tableStyle="min-width: 50rem"
          @row-click="openSidebar"
        >
          <template #header>
            <div class="search-wrapper">
              <i class="pi pi-search"></i>
              <InputText v-model="filters.global.value" placeholder="Поиск..." />
            </div>
          </template>
        
          <Column field="date" header="Дата" sortable>
            <template #body="slotProps">
              {{ formatDate(slotProps.data.date) }}
            </template>
          </Column>
          <Column field="full_name" header="ФИО" sortable />
          <Column field="object" header="Объект" sortable />
          <Column field="phone" header="Телефон" sortable>
            <template #body="slotProps">
              <div class="nowrap">
                {{ slotProps.data.phone }}
              </div>
            </template>
          </Column>
          <Column field="email" header="Email" sortable>
            <template #body="slotProps">
              <div class="nowrap-cell">
                {{ slotProps.data.email }}
              </div>
            </template>
          </Column>
          <Column field="serial_numbers" header="Серийные номера" sortable>
            <template #body="slotProps">
              <div class="nowrap">
                {{ slotProps.data.serial_numbers }}
              </div>
            </template>
          </Column>
          <Column field="category" header="Тема" sortable > 
          </Column>
          <Column field="sentiment" header="Тональность" sortable />
          <Column field="status" header="Статус" sortable />
        </DataTable>

        <Sidebar 
          v-model:visible="sidebarVisible" 
          position="right"
          :baseZIndex="1000"
          :showCloseIcon="true"
          :dismissable="true"
          :modal="true"
          class="details-sidebar"
          :style="{ minWidth: '800px', maxWidth: '850px', width: '100%' }"
        >
          <template #header>
            <h3 class="sidebar-title">Детали записи</h3>
          </template>

          <div v-if="selectedRow" class="sidebar-content">
            <div class="detail-item">
              <div class="detail-label">Дата:</div>
              <div class="detail-value">{{ formatDate(selectedRow.date) }}</div>
            </div>
            <div class="detail-item">
              <div class="detail-label">ФИО:</div>
              <div class="detail-value">{{ selectedRow.full_name }}</div>
            </div>

            <div class="detail-item">
              <div class="detail-label">Объект:</div>
              <div class="detail-value">{{ selectedRow.object }}</div>
            </div>

            <div class="detail-item">
              <div class="detail-label">Телефон:</div>
              <div class="detail-value">{{ selectedRow.phone }}</div>
            </div>

            <div class="detail-item">
              <div class="detail-label">Email:</div>
              <div class="detail-value">{{ selectedRow.email }}</div>
            </div>

            <div class="detail-item">
              <div class="detail-label">Серийные номера:</div>
              <div class="detail-value">{{ selectedRow.serial_numbers }}</div>
            </div>

            <div class="detail-item">
              <div class="detail-label">Тема:</div>
              <div class="detail-value">{{ selectedRow.category }}</div>
            </div>

            <div class="detail-item">
              <div class="detail-label">Тональность:</div>
              <div class="detail-value">{{ selectedRow.sentiment }}</div>
            </div>

            <div class="detail-item">
              <div class="detail-label">Статус:</div>
              <div class="detail-value">{{ selectedRow.status }}</div>
            </div>
            
            <div class="detail-item">
              <div class="detail-label">Суть обращения:</div>
              <div class="detail-value">{{ selectedRow.subject }}</div>
            </div>

            <div class="text-dialog">
              <div class="user">
                <p>{{ selectedRow.raw_body }}</p>
              </div>
            
              <div class="operator">
                <div class="textarea-wrapper">

                <p class="operator-answer" v-if="!answerSend">
                  {{ operatorMessage }}
                </p>

                  <textarea 
                    placeholder="Ответ"
                    v-model="operatorMessage"
                    :disabled="generateStatus"
                    v-if="answerSend"
                  ></textarea>
                
                  <button 
                    class="ai-button"
                    type="button"
                    @click="generateAIResponse(selectedRow.ai_generated_response)"
                    title="Сгенерировать ответ"
                    v-if="answerSend"
                  >
                    <img src="/src/assets/wand.png" alt="Генерация ответа">
                  </button>

                  <button 
                    class="send-button"
                    type="button"
                    @click="sendAnswer(selectedRow.id, operatorMessage, selectedRow.subject)"
                    title="Сгенерировать ответ"
                    :disabled="generateStatus"
                    v-if="answerSend"
                  >
                    <img src="/src/assets/plane.png" alt="Отправить">
                  </button>
                </div>
              
              </div>
            </div>
          </div>
        </Sidebar>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useDataStore } from '../stores/counter';
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import InputText from 'primevue/inputtext'
import Sidebar from 'primevue/sidebar';

const store = useDataStore();
const emails = computed(() => store.getEmails);
const operatorMessage = ref('')
const generateStatus = ref(false)
const answerSend = ref(true)

onMounted(() => {
  store.FetchEmails();
});

const filters = ref({
  global: { value: null, matchMode: 'contains' }
})

const sidebarVisible = ref(false);
const selectedRow = ref(null);

const openSidebar = (event) => {
  selectedRow.value = event.data;
  sidebarVisible.value = true;
};

const formatDate = (dateString) => {
  if (!dateString) return '';
  
  const date = new Date(dateString);
  const day = String(date.getDate()).padStart(2, '0');
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const year = String(date.getFullYear()).slice(-2); // Последние 2 цифры года
  
  return `${day}.${month}.${year}`;
};

function generateAIResponse(ai_generated_response, ) {
  generateStatus.value = true
  if (!ai_generated_response) {
    console.log("Нет данных для генерации ответа нужен запрос на генерацию");
    generateStatus.value = false
    return
  }
  
  operatorMessage.value = "Генерирую ответ...";
  
  setTimeout(() => {
    operatorMessage.value = `AI-ответ: ${ai_generated_response}`;
  }, 1000);
  generateStatus.value = false
}

async function sendAnswer(id, operatorMessage, subject) {
  alert('Начал')
  generateStatus.value = true
  try {
    await store.PostAnswer(id, {
      subject: subject,
      body: operatorMessage
    });
    console.log('Ответ успешно отправлен');
    answerSend.value = false;
    generateStatus.value = false;
  } catch (error) {
    console.error('Ошибка отправки:', error);
  }
}
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

.background-img {
  position: absolute;
  z-index: -1;
  top: -80px;
  right: -80px;
}

:deep(.nowrap) {
  white-space: nowrap;     /* Запрещает перенос текста */
}

:deep(.nowrap-cell) {
  white-space: nowrap; 
  overflow: hidden;        /* Скрывает выходящий текст */
  text-overflow: ellipsis; /* Добавляет многоточие если текст не помещается */
  max-width: 90px;
}

:deep(.p-datatable .p-datatable-header) {
  background: none;
  margin-bottom: 20px;
  border: none;
}

:deep(.p-inputtext) {
  width: 700px;
}

:deep(.p-datatable .p-datatable-wrapper) {
  background: none;
  border: 2px solid #F5F5F5;
  border-radius: 14px;
  overflow: hidden;
}

.content-wrapper {
  width: 100%;
}

:deep(.p-datatable .p-datatable-tbody > tr) {
  border: none !important;
  height: 100px;
  max-height: 100px;
}

:deep(.p-datatable .p-datatable-tbody > tr > td) {
  border-top: 2px solid transparent;
  border-bottom: 2px solid transparent;
  transition: border-color 0.2s;
}

:deep(.cell-content) {
  display: -webkit-box;
  -webkit-line-clamp: 4;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
  box-sizing: border-box;
  word-break: break-word;
  line-height: 1.4;
}

:deep(.p-datatable .p-datatable-tbody > tr > td:first-child) {
  border-left: 2px solid transparent;
  border-top-left-radius: 10px;
  border-bottom-left-radius: 10px;
}

:deep(.p-datatable .p-datatable-tbody > tr > td:last-child) {
  border-right: 2px solid transparent;
  border-top-right-radius: 10px;
  border-bottom-right-radius: 10px;
}

:deep(.p-datatable .p-datatable-tbody > tr:hover > td) {
  border-color: #6AB23D;
}

:deep(.p-datatable-table-container) {
  border-color: #6AB23D;
}

:deep(.p-datatable .p-datatable-tbody > tr:nth-child(odd) > td) {
  background-color: rgba(79, 214, 134, 0.1);
}

:deep(.p-datatable .p-datatable-tbody > tr:nth-child(even) > td) {
  background-color: #ffffff;
}

.search-wrapper {
  display: flex;
  align-items: center;
  gap: 8px;
}

h2 {
  margin-bottom: 20px;
}

.sidebar-title {
  font-family: 'Lato', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  text-align: center;
  width: 100%;
  margin: 0;
  transform: translateX(36px);
}

:deep(.details-sidebar .p-sidebar-header) {
  padding: 1.5rem 1.5rem 0.5rem 1.5rem;
  border-bottom: 1px solid #e9ecef;
}

:deep(.details-sidebar .p-sidebar-header h3) {
  margin: 0 auto;
}

:deep(.details-sidebar .p-sidebar-content) {
  padding: 1.5rem;
}

.sidebar-content {
  height: 100%;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 1.2rem;
  padding-bottom: 0.8rem;
}

.detail-item:last-child {
  border-bottom: none;
}

.detail-label {
  color: #6AB23D;
  font-family: 'Lato', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  min-width: max-content;
}

.detail-value {
  font-family: 'Lato', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
}


.detail-value.long-text {
  max-height: 200px;
  overflow-y: auto;
  padding: 0.5rem;
  background: #f8f9fa;
  border-radius: 4px;
}

:deep(.custom-table .p-datatable-tbody > tr) {
  cursor: pointer;
  transition: background-color 0.2s;
}

:deep(.custom-table .p-datatable-tbody > tr:hover) {
  background-color: #f3f4f6 !important;
}

.text-dialog {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-bottom: 50px;
}

.user, .operator-answer {
  border-radius: 8px;
  width: 500px;
  padding: 10px;
  background: #edfbf3;
}

.textarea-wrapper {
  position: relative;
  width: 100%;
  display: flex;
  justify-content: flex-end;
  margin-bottom: 200px;
}

.textarea-wrapper textarea {
  width: 500px;
  min-height: 120px;
  resize: vertical;

  padding: 16px 48px 16px 16px; /* место справа под кнопку */
  font-size: 14px;
  font-family: inherit;

  border: 1px solid #e5e7eb;
  border-radius: 16px;
  outline: none;

  background-color: #f9fafb;
}

.textarea-wrapper textarea::placeholder {
  color: #9ca3af;
}

.textarea-wrapper textarea:focus {
  border-color: #cbd5e1;
  background-color: #ffffff;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.08);
}

.textarea-wrapper > button > img {
  width: 20px;
}

/* Кнопка AI */
.ai-button {
  position: absolute;
  right: -10px;
  top: -10px;

  width: 36px;
  height: 36px;

  border-radius: 50%;
  border: none;

  background: #ffffff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);

  cursor: pointer;
  font-size: 16px;

  display: flex;
  align-items: center;
  justify-content: center;

  transition: all 0.2s ease;
}

.ai-button:hover, .send-button:hover {
  background: #f3f4f6;
  transform: scale(1.05);
}

.ai-button:active, .send-button:active {
  transform: scale(0.95);
}

.send-button {
  position: absolute;
  right: 12px;
  bottom: 12px;

  width: 36px;
  height: 36px;

  border-radius: 50%;
  border: none;

  background: #ffffff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);

  cursor: pointer;
  font-size: 16px;

  display: flex;
  align-items: center;
  justify-content: center;

  transition: all 0.2s ease;
}
</style>