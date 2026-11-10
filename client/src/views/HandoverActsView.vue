<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const acts = ref([]);
const requests = ref([]);
const editId = ref(null);

const form = ref({
  request: '',
  receiver_user: 1,
  issuer_user: 1,
  inventory_tag: '',
  workplace_location: ''
});

async function fetchData() {
  const [actRes, reqRes] = await Promise.all([
    axios.get('/api/handover-acts/'),
    axios.get('/api/build-requests/')
  ]);
  acts.value = actRes.data;
  requests.value = reqRes.data;
}

onMounted(fetchData);

function resetForm() {
  editId.value = null;
  form.value = {
    request: '',
    receiver_user: 1,
    issuer_user: 1,
    inventory_tag: '',
    workplace_location: ''
  };
}

async function onSubmit() {
  if (editId.value) {
    await axios.patch(`/api/handover-acts/${editId.value}/`, form.value);
  } else {
    await axios.post('/api/handover-acts/', form.value);
  }
  resetForm();
  await fetchData();
}

function startEdit(act) {
  editId.value = act.id;
  form.value = { ...act };
}

async function onRemove(act) {
  if (confirm(`Удалить акт #${act.inventory_tag}?`)) {
    await axios.delete(`/api/handover-acts/${act.id}/`);
    await fetchData();
  }
}
</script>

<template>
  <div class="container">
    <h3 class="mb-3">{{ editId ? 'Редактировать акт' : 'Оформить акт выдачи' }}</h3>

    <form @submit.prevent="onSubmit" class="card p-3 mb-4 shadow-sm">
      <div class="row g-3">
        <div class="col-md-4">
          <select class="form-select" v-model="form.request" required>
            <option value="" disabled>Заявка на выдачу</option>
            <option v-for="r in requests" :key="r.id" :value="r.id">Заявка #{{ r.id }}</option>
          </select>
        </div>
        <div class="col-md-4">
          <input type="text" class="form-control" placeholder="Инвентарный номер" v-model="form.inventory_tag" required />
        </div>
        <div class="col-md-4">
          <input type="text" class="form-control" placeholder="Место установки (кабинет)" v-model="form.workplace_location" required />
        </div>
        <div class="col-md-6">
          <input type="number" class="form-control" placeholder="ID получателя" v-model="form.receiver_user" required />
        </div>
        <div class="col-md-6">
          <input type="number" class="form-control" placeholder="ID инженера (выдавшего)" v-model="form.issuer_user" required />
        </div>
        <div class="col-12 text-end">
          <button v-if="editId" @click="resetForm" type="button" class="btn btn-secondary me-2">Отмена</button>
          <button class="btn btn-primary" type="submit">{{ editId ? 'Сохранить' : 'Оформить акт' }}</button>
        </div>
      </div>
    </form>

    <h4 class="mb-3">Акты выдачи оборудования</h4>
    <table class="table table-bordered table-hover">
      <thead class="table-light">
        <tr>
          <th>ID</th>
          <th>Инв. номер</th>
          <th>Кабинет</th>
          <th>ID заявки</th>
          <th>Получатель</th>
          <th>Выдал</th>
          <th>Действия</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="act in acts" :key="act.id">
          <td>{{ act.id }}</td>
          <td><strong>{{ act.inventory_tag }}</strong></td>
          <td>{{ act.workplace_location }}</td>
          <td>#{{ act.request }}</td>
          <td>Пользователь {{ act.receiver_user }}</td>
          <td>Инженер {{ act.issuer_user }}</td>
          <td>
            <button class="btn btn-sm btn-outline-primary me-2" @click="startEdit(act)">✏️</button>
            <button class="btn btn-sm btn-outline-danger" @click="onRemove(act)">🗑️</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>