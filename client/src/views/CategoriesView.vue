<script setup>
import { onBeforeMount, ref } from 'vue';
import axios from 'axios';
import Cookies from 'js-cookie';
import { Modal } from 'bootstrap';

const categories = ref([]);
const categoryToAdd = ref({
  name: '',
  is_standalone: false
});

const categoryToEdit = ref({});
const loading = ref(false);

const categoryPictureRef = ref();
const categoryAddPictureUrl = ref();
const categoryEditPictureRef = ref();
const previewPictureUrl = ref('');

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
  const formData = new FormData();

  formData.append('name', categoryToEdit.value.name);
  formData.append('is_standalone', categoryToEdit.value.is_standalone);
  formData.append('picture', categoryEditPictureRef.value.files[0]);

  await axios.put(`/api/categories/${categoryToEdit.value.id}/`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  });

  categoryEditPictureRef.value.value = '';

  await fetchComponents();
}

async function categoryAddPictureChange() {
  componentAddPictureUrl.value = URL.createObjectURL(componentPictureRef.value.files[0])
}

function onPictureClick(url) {
  const fullUrl = url.startsWith('http') ? url : `http://localhost:8000${url}`;
  previewPictureUrl.value = fullUrl;
  const modalEl = document.getElementById('picturePreviewModal');
  const modal = Modal.getOrCreateInstance(modalEl);
  modal.show();
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
        <div class="col-auto">
          <input class="form-control" type="file" ref="categoryPictureRef" @change="categoryAddPictureChange">
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
          <th>Изображение</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in categories" :key="item.id">
          <td>{{ item.id }}</td>
          <td><strong>{{ item.name }}</strong></td>
          <td>{{ item.is_standalone ? 'Самостоятельное устройство' : 'Комплектующее' }}</td>
          <td v-if="item.picture">
            <img :src="item.picture" style="max-height: 60px; cursor: pointer;" class="rounded border shadow-sm"@click="onPictureClick(item.picture)"/>
          </td>
          <td v-else class="text-muted">Нет фото</td>
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
          class="btn btn-success"
          data-bs-toggle="modal"
          data-bs-target="#editCategoryModal"
          @click="onEditClick(item)"
        >
          <i class="bi bi-pen-fill"></i>
        </button>

        <button class="btn btn-danger"@click="onRemoveClick(item)">
          <i class="bi bi-x"></i>
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
              <div class="col-12">
                <label class="form-label">Заменить изображение</label>
                <input class="form-control" type="file" ref="categoryEditPictureRef">
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
  <div class="modal fade" id="picturePreviewModal" tabindex="-1" aria-hidden="true">
  <div class="modal-dialog modal-dialog-centered modal-lg">
    <div class="modal-content">
      <div class="modal-header border-0 pb-0">
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      <div class="modal-body text-center pt-0">
        <img :src="previewPictureUrl" class="img-fluid rounded shadow"/>
      </div>
    </div>
  </div>
</div>
</template>

<style scoped>
</style>