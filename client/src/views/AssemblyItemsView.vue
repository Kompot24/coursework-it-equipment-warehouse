<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const items = ref([]);
const components = ref([]);
const requests = ref([]);
const editId = ref(null);

const form = ref({ request: '', component: '', quantity: 1 });

async function fetchData() {
  const [itemsRes, compRes, reqRes] = await Promise.all([
    axios.get('/api/assembly-items/'),
    axios.get('/api/components/'),
    axios.get('/api/build-requests/')
  ]);
  items.value = itemsRes.data;
  components.value = compRes.data;
  requests.value = reqRes.data;
}

onMounted(fetchData);

function resetForm() {
  editId.value = null;
  form.value = { request: '', component: '', quantity: 1 };
}

async function onSubmit() {
  if (editId.value) {
    await axios.patch(`/api/assembly-items/${editId.value}/`, form.value);
  } else {
    await axios.post('/api/assembly-items/', form.value);
  }
  resetForm();
  await fetchData();
}

function startEdit(item) {
  editId.value = item.id;
  form.value = { request: item.request, component: item.component, quantity: item.quantity };
}

async function onRemove(item) {
  if (confirm(`Удалить деталь из сборки?`)) {
    await axios.delete(`/api/assembly-items/${item.id}/`);
    await fetchData();
  }
}
</script>

<template>
  <div class="container">
    <h3 class="mb-3">{{ editId ? 'Изменить состав сборки' : 'Добавить деталь в заявку' }}</h3>

    <form @submit.prevent="onSubmit" class="card p-3 mb-4 shadow-sm">
      <div class="row g-3">
        <div class="col-md-5">
          <select class="form-select" v-model="form.request" required>
            <option value="" disabled>Выберите заявку</option>
            <option v-for="r in requests" :key="r.id" :value="r.id">Заявка #{{ r.id }} ({{ r.target_workload }})</option>
          </select>
        </div>
        <div class="col-md-4">
          <select class="form-select" v-model="form.component" required>
            <option value="" disabled>Выберите комплектующее</option>
            <option v-for="c in components" :key="c.id" :value="c.id">{{ c.model_name }}</option>
          </select>
        </div>
        <div class="col-md-3">
          <input type="number" min="1" class="form-control" placeholder="Кол-во" v-model="form.quantity" required />
        </div>
        <div class="col-12 text-end">
          <button v-if="editId" @click="resetForm" type="button" class="btn btn-secondary me-2">Отмена</button>
          <button class="btn btn-primary" type="submit">{{ editId ? 'Сохранить' : 'Добавить в сборку' }}</button>
        </div>
      </div>
    </form>

    <h4 class="mb-3">Составы сборок</h4>
    <table class="table table-bordered table-hover">
      <thead class="table-light">
        <tr>
          <th>ID</th>
          <th>ID заявки</th>
          <th>ID компонента</th>
          <th>Количество</th>
          <th>Действия</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in items" :key="item.id">
          <td>{{ item.id }}</td>
          <td>#{{ item.request }}</td>
          <td>{{ item.component }}</td>
          <td>{{ item.quantity }} шт.</td>
          <td>
            <button class="btn btn-sm btn-outline-primary me-2" @click="startEdit(item)">✏️</button>
            <button class="btn btn-sm btn-outline-danger" @click="onRemove(item)">🗑️</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>