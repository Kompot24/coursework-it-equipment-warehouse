<script setup>
import { onBeforeMount, ref } from 'vue';
import axios from 'axios';
import Cookies from 'js-cookie';

const categories = ref([]);
const categoryToAdd = ref({
  name: '',
  is_standalone: false
});

const categoryToEdit = ref({});
const loading = ref(false);

async function fetchCategories() {
  loading.value = true;
  const r = await axios.get('/api/categories/');
  console.log(r.data);
  categories.value = r.data;
  loading.value = false;
}

onBeforeMount(async () => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get('csrftoken');
  await fetchCategories();
});

async function onCategoryAdd() {
  await axios.post('/api/categories/', categoryToAdd.value);
  categoryToAdd.value = {
    name: '',
    is_standalone: false
  };
  await fetchCategories();
}

async function onRemoveClick(category) {
  await axios.delete(`/api/categories/${category.id}/`);
  await fetchCategories();
}

function onEditClick(category) {
  categoryToEdit.value = { ...category };
}

async function onUpdateCategory() {
  const payload = { ...categoryToEdit.value };
  const id = payload.id;
  delete payload.id;

  await axios.put(`/api/categories/${id}/`, payload);
  await fetchCategories();
}
</script>

<template>
  <div class="container py-4">
    <h4 class="mb-3">Добавить категорию</h4>
    <form @submit.prevent.stop="onCategoryAdd">
      <div class="row g-3">
        <div class="col-md-6">
          <div class="form-floating">
            <input
              type="text"
              class="form-control"
              id="categoryNameInput"
              v-model="categoryToAdd.name"
              required
            />
            <label for="categoryNameInput">Название категории</label>
          </div>
        </div>

        <div class="col-md-4 d-flex align-items-center">
          <div class="form-check">
            <input
              class="form-check-input"
              type="checkbox"
              id="checkStandaloneAdd"
              v-model="categoryToAdd.is_standalone"
            />
            <label class="form-check-label" for="checkStandaloneAdd">
              Самостоятельное устройство
            </label>
          </div>
        </div>

        <div class="col-12">
          <button class="btn btn-primary" type="submit">
            Добавить
          </button>
        </div>
      </div>
    </form>

    <h4 class="my-4">Категории на складе</h4>
    <div v-if="loading" class="text-muted">Загрузка данных...</div>

    <table v-else class="table table-hover table-bordered">
      <thead class="table-light">
        <tr>
          <th>ID</th>
          <th>Название</th>
          <th>Тип</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in categories" :key="item.id">
          <td>{{ item.id }}</td>
          <td><strong>{{ item.name }}</strong></td>
          <td>{{ item.is_standalone ? 'Самостоятельное устройство' : 'Комплектующее' }}</td>
        </tr>
      </tbody>
    </table>

    <h4 class="my-4">Управление категориями</h4>
    <div
      v-for="item in categories"
      :key="item.id"
      class="d-flex align-items-center justify-content-between border p-2 mb-2 rounded bg-light"
    >
      <div>
        <strong>{{ item.name }}</strong>
        <span class="text-muted ms-2">({{ item.is_standalone ? 'Самостоятельное устройство' : 'Комплектующее' }})</span>
      </div>

      <div class="d-flex gap-2">
        <button
          class="btn btn-sm btn-outline-success"
          data-bs-toggle="modal"
          data-bs-target="#editCategoryModal"
          @click="onEditClick(item)"
          title="Редактировать"
        >
          <i class="bi bi-pencil-fill"></i> Редактировать
        </button>

        <button
          class="btn btn-sm btn-outline-danger"
          @click="onRemoveClick(item)"
          title="Удалить"
        >
          <i class="bi bi-trash-fill"></i> Удалить
        </button>
      </div>
    </div>

    <div class="modal fade" id="editCategoryModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5">Редактировать категорию</h1>
            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
              aria-label="Close"
            ></button>
          </div>
          <div class="modal-body">
            <div class="row g-3">
              <div class="col-12">
                <div class="form-floating">
                  <input
                    type="text"
                    class="form-control"
                    id="editCategoryName"
                    v-model="categoryToEdit.name"
                    required
                  />
                  <label for="editCategoryName">Название категории</label>
                </div>
              </div>
              <div class="col-12">
                <div class="form-check">
                  <input
                    class="form-check-input"
                    type="checkbox"
                    id="editStandaloneCheck"
                    v-model="categoryToEdit.is_standalone"
                  />
                  <label class="form-check-label" for="editStandaloneCheck">
                    Самостоятельное устройство
                  </label>
                </div>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button
              type="button"
              class="btn btn-secondary"
              data-bs-dismiss="modal"
            >
              Закрыть
            </button>
            <button
              data-bs-dismiss="modal"
              type="button"
              class="btn btn-primary"
              @click="onUpdateCategory"
            >
              Сохранить
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
</style>