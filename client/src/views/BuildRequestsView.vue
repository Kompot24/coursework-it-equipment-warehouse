<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const requests = ref([]);
const editId = ref(null);
const form = ref({
  employee: 1,
  target_workload: '',
  request_type: 'assembly',
  status: 'pending',
  comment: ''
});

async function fetchData() {
  const r = await axios.get('/api/build-requests/');
  requests.value = r.data;
}

onMounted(fetchData);

function resetForm() {
  editId.value = null;
  form.value = { employee: 1, target_workload: '', request_type: 'assembly', status: 'pending', comment: '' };
}

async function onSubmit() {
  if (editId.value) {
    await axios.patch(`/api/build-requests/${editId.value}/`, form.value);
  } else {
    await axios.post('/api/build-requests/', form.value);
  }
  resetForm();
  await fetchData();
}

function startEdit(item) {
  editId.value = item.id;
  form.value = { ...item };
}

async function onRemove(item) {
  if (confirm(`Удалить заявку #${item.id}?`)) {
    await axios.delete(`/api/build-requests/${item.id}/`);
    await fetchData();
  }
}
</script>

<template>
  <div class="container">
    <h3 class="mb-3">{{ editId ? 'Редактировать заявку' : 'Создать заявку на сборку' }}</h3>

    <form @submit.prevent="onSubmit" class="card p-3 mb-4 shadow-sm">
      <div class="row g-3">
        <div class="col-md-4">
          <input type="text" class="form-control" placeholder="Назначение (Офис, 3D, Сервер)" v-model="form.target_workload" required />
        </div>
        <div class="col-md-4">
          <select class="form-select" v-model="form.status" required>
            <option value="pending">Ожидает (Pending)</option>
            <option value="in_progress">В сборке (In Progress)</option>
            <option value="completed">Готово (Completed)</option>
            <option value="cancelled">Отменено (Cancelled)</option>
          </select>
        </div>
        <div class="col-md-4">
          <input type="number" class="form-control" placeholder="ID сотрудника" v-model="form.employee" required />
        </div>
        <div class="col-12">
          <input type="text" class="form-control" placeholder="Комментарий к сборке" v-model="form.comment" />
        </div>
        <div class="col-12 text-end">
          <button v-if="editId" @click="resetForm" type="button" class="btn btn-secondary me-2">Отмена</button>
          <button class="btn btn-primary" type="submit">{{ editId ? 'Сохранить' : 'Создать заявку' }}</button>
        </div>
      </div>
    </form>

    <h4 class="mb-3">Список заявок на сборку</h4>
    <table class="table table-bordered table-hover">
      <thead class="table-light">
        <tr>
          <th>№</th>
          <th>Назначение</th>
          <th>Статус</th>
          <th>ID сотрудника</th>
          <th>Комментарий</th>
          <th>Действия</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="req in requests" :key="req.id">
          <td>{{ req.id }}</td>
          <td>{{ req.target_workload }}</td>
          <td><span class="badge bg-secondary">{{ req.status }}</span></td>
          <td>{{ req.employee }}</td>
          <td>{{ req.comment }}</td>
          <td>
            <button class="btn btn-sm btn-outline-primary me-2" @click="startEdit(req)">✏️</button>
            <button class="btn btn-sm btn-outline-danger" @click="onRemove(req)">🗑️</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>