<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const categories = ref([]);
const editId = ref(null);
const form = ref({ name: '', is_standalone: false });

async function fetchData() {
  const r = await axios.get('/api/categories/');
  categories.value = r.data;
}

onMounted(fetchData);

function resetForm() {
  editId.value = null;
  form.value = { name: '', is_standalone: false };
}

async function onSubmit() {
  if (editId.value) {
    await axios.patch(`/api/categories/${editId.value}/`, form.value);
  } else {
    await axios.post('/api/categories/', form.value);
  }
  resetForm();
  await fetchData();
}

function startEdit(cat) {
  editId.value = cat.id;
  form.value = { name: cat.name, is_standalone: cat.is_standalone };
}

async function onRemove(cat) {
  if (confirm(`Удалить категорию "${cat.name}"?`)) {
    await axios.delete(`/api/categories/${cat.id}/`);
    await fetchData();
  }
}
</script>

<template>
  <div class="container">
    <h3 class="mb-3">{{ editId ? 'Редактировать категорию' : 'Добавить категорию' }}</h3>

    <form @submit.prevent="onSubmit" class="card p-3 mb-4 shadow-sm">
      <div class="row g-3 align-items-center">
        <div class="col-md-6">
          <input type="text" class="form-control" placeholder="Название категории" v-model="form.name" required />
        </div>
        <div class="col-md-3">
          <div class="form-check">
            <input class="form-check-input" type="checkbox" id="standaloneCheck" v-model="form.is_standalone" />
            <label class="form-check-label" for="standaloneCheck">Самостоятельное устройство</label>
          </div>
        </div>
        <div class="col-md-3 text-end">
          <button v-if="editId" @click="resetForm" type="button" class="btn btn-secondary me-2">Отмена</button>
          <button class="btn btn-primary" type="submit">{{ editId ? 'Сохранить' : 'Добавить' }}</button>
        </div>
      </div>
    </form>

    <h4 class="mb-3">Список категорий</h4>
    <table class="table table-bordered table-hover">
      <thead class="table-light">
        <tr>
          <th>ID</th>
          <th>Название</th>
          <th>Самостоятельное</th>
          <th>Действия</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="cat in categories" :key="cat.id">
          <td>{{ cat.id }}</td>
          <td>{{ cat.name }}</td>
          <td>{{ cat.is_standalone ? 'Да' : 'Нет' }}</td>
          <td>
            <button class="btn btn-sm btn-outline-primary me-2" @click="startEdit(cat)">✏️</button>
            <button class="btn btn-sm btn-outline-danger" @click="onRemove(cat)">🗑️</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>