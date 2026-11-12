<script setup>
import { computed, onBeforeMount, ref } from 'vue';
import axios from 'axios';
import Cookies from 'js-cookie';
import { Modal } from 'bootstrap';

const components = ref([]);
const componentToAdd = ref({
  model_name: '',
  category: '',
  serial_number: '',
  specifications: '',
  quantity_stock: 1,
  status: 'В наличии'
});

const categories = ref([]);
const componentToEdit = ref({});
const loading = ref(false);

const componentPictureRef = ref(null);
const componentAddPictureUrl = ref('');
const componentEditPictureRef = ref(null);
const previewPictureUrl = ref('');

const userInfo = ref({
  is_authenticated: false,
  is_superuser: false,
  users: []
});
const selectedUserId = ref('');

async function fetchComponents() {
  loading.value = true;
  const params = {};
  
  if (selectedUserId.value) {
    params.user = selectedUserId.value;
  }

  const r = await axios.get('/api/components/', { params });
  components.value = r.data;
  loading.value = false;
}

async function fetchCategories() {
  const r = await axios.get('/api/categories/');
  categories.value = r.data;
}

async function fetchUserInfo() {
  const r = await axios.get('/api/user-info/');
  userInfo.value = r.data;
}

const categoriesById = computed(() =>
  Object.fromEntries(categories.value.map(c => [c.id, c.name]))
);

const usersById = computed(() =>
  Object.fromEntries((userInfo.value.users || []).map(u => [u.id, u.username]))
);

onBeforeMount(async () => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get('csrftoken');
  await fetchUserInfo();
  await fetchCategories();
  await fetchComponents();
});

async function onComponentAdd() {
  const formData = new FormData();

  formData.append('picture', componentPictureRef.value.files[0]);

  formData.append('model_name', componentToAdd.value.model_name);
  formData.append('serial_number', componentToAdd.value.serial_number);
  formData.append('specifications', componentToAdd.value.specifications);
  formData.append('quantity_stock', componentToAdd.value.quantity_stock);
  formData.append('status', componentToAdd.value.status);

  const categoryId = typeof componentToAdd.value.category === 'object' ? componentToAdd.value.category.id : componentToAdd.value.category;
  formData.append('category', categoryId);

  await axios.post('/api/components/', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  });

  componentToAdd.value = {
    model_name: '',
    category: '',
    serial_number: '',
    specifications: '',
    quantity_stock: 1,
    status: 'В наличии'
  };
  
  componentPictureRef.value.value = '';
  componentAddPictureUrl.value = '';

  await fetchComponents();
}

async function onRemoveClick(component) {
  await axios.delete(`/api/components/${component.id}/`);
  await fetchComponents();
}

function onEditClick(component) {
  componentToEdit.value = { ...component };
}

async function onUpdateComponent() {
  const formData = new FormData();

  formData.append('picture', componentEditPictureRef.value.files[0]);

  formData.append('model_name', componentToEdit.value.model_name);
  formData.append('serial_number', componentToEdit.value.serial_number);
  formData.append('specifications', componentToEdit.value.specifications || '');
  formData.append('quantity_stock', componentToEdit.value.quantity_stock);
  formData.append('status', componentToEdit.value.status);

  const categoryId = typeof componentToEdit.value.category === 'object'
    ? componentToEdit.value.category.id
    : componentToEdit.value.category;
  formData.append('category', categoryId);

  await axios.patch(`/api/components/${componentToEdit.value.id}/`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  });

  componentEditPictureRef.value.value = '';

  await fetchComponents();
}

function componentAddPictureChange() {
  const file = componentPictureRef.value?.files?.[0];
  componentAddPictureUrl.value = file ? URL.createObjectURL(file) : '';
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
    <h4 class="mb-3">Добавить компонент на склад</h4>
    <form @submit.prevent.stop="onComponentAdd">
      <div class="row g-3">
        <div class="col-md-4">
          <div class="form-floating">
            <input
              type="text"
              class="form-control"
              id="modelInput"
              v-model="componentToAdd.model_name"
              required
            />
            <label for="modelInput">Модель</label>
          </div>
        </div>

        <div class="col-md-3">
          <div class="form-floating">
            <input
              type="text"
              class="form-control"
              id="serialInput"
              v-model="componentToAdd.serial_number"
              required
            />
            <label for="serialInput">Серийный номер</label>
          </div>
        </div>

        <div class="col-md-3">
          <div class="form-floating">
            <input
              type="text"
              class="form-control"
              id="specsInput"
              v-model="componentToAdd.specifications"
              required
            />
            <label for="specsInput">Технические характеристики</label>
          </div>
        </div>

        <div class="col-md-2">
          <div class="form-floating">
            <input
              type="number"
              class="form-control"
              id="quantityInput"
              v-model="componentToAdd.quantity_stock"
              min="1"
              required
            />
            <label for="quantityInput">Кол-во на складе</label>
          </div>
        </div>

        <div class="col-md-3">
          <div class="form-floating">
            <input
              type="text"
              class="form-control"
              id="statusInput"
              v-model="componentToAdd.status"
              required
            />
            <label for="statusInput">Статус</label>
          </div>
        </div>

        <div class="col-md-3">
          <div class="form-floating">
            <select class="form-select" id="categorySelect" v-model="componentToAdd.category" required>
              <option :value="g.id" v-for="g in categories" :key="g.id">{{ g.name }}</option>
            </select>
            <label for="categorySelect">Категория</label>
          </div>
        </div>

        <div class="col-auto d-flex align-items-center">
          <input
            class="form-control"
            type="file"
            accept="image/*"
            ref="componentPictureRef"
            @change="componentAddPictureChange"
          />
        </div>

        <div class="col-auto" v-if="componentAddPictureUrl">
          <img :src="componentAddPictureUrl" style="max-height: 60px;" class="rounded border" alt="Превью" />
        </div>

        <div class="col-12">
          <button class="btn btn-primary" type="submit">
            Добавить
          </button>
        </div>
      </div>
    </form>

    <h4 class="my-4">Компоненты на складе</h4>

    <div v-if="userInfo.is_superuser" class="row mb-3">
      <div class="col-md-4">
        <div class="form-floating">
          <select
            class="form-select"
            id="userFilterSelect"
            v-model="selectedUserId"
            @change="fetchComponents"
          >
            <option value="">Все пользователи</option>
            <option v-for="u in userInfo.users" :key="u.id" :value="u.id">
              {{ u.username }} (ID: {{ u.id }})
            </option>
          </select>
          <label for="userFilterSelect">Фильтр по пользователю</label>
        </div>
      </div>
    </div>

    <div v-if="loading" class="text-muted">Загрузка данных...</div>

    <table v-else class="table table-hover table-bordered align-middle">
      <thead class="table-light">
        <tr>
          <th>ID</th>
          <th>Модель</th>
          <th>Серийный номер</th>
          <th>Техническая характеристика</th>
          <th>Кол-во</th>
          <th>Статус</th>
          <th>Категория</th>
          <th>Изображение</th>
          <th v-if="userInfo.is_superuser">Пользователь</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in components" :key="item.id">
          <td>{{ item.id }}</td>
          <td><strong>{{ item.model_name }}</strong></td>
          <td><code>{{ item.serial_number }}</code></td>
          <td>{{ item.specifications }}</td>
          <td>{{ item.quantity_stock }}</td>
          <td>{{ item.status }}</td>
          <td>{{ categoriesById[item.category] ?? item.category }}</td>
          <td>
            <img
              v-if="item.picture"
              :src="item.picture"
              style="max-height: 60px; cursor: pointer;"
              class="rounded border shadow-sm"
              @click="onPictureClick(item.picture)"
              alt="Фото компонента"
            />
            <span v-else class="text-muted">Нет фото</span>
          </td>
          <td v-if="userInfo.is_superuser">
            {{ usersById[item.user] ?? item.user ?? '—' }}
          </td>
        </tr>
      </tbody>
    </table>

    <h4 class="my-4">Управление компонентами</h4>
    <div
      v-for="item in components"
      :key="item.id"
      class="d-flex align-items-center justify-content-between border p-2 mb-2 rounded bg-light"
    >
      <div>
        <strong>{{ item.model_name }}</strong>
        <span class="text-muted ms-2">({{ categoriesById[item.category] ?? item.category }})</span>
      </div>

      <div class="d-flex gap-2">
        <button
          class="btn btn-sm btn-success"
          data-bs-toggle="modal"
          data-bs-target="#editComponentModal"
          @click="onEditClick(item)"
          title="Редактировать"
        >
          <i class="bi bi-pen-fill"></i>
        </button>

        <button
          class="btn btn-sm btn-danger"
          @click="onRemoveClick(item)"
          title="Удалить"
        >
          <i class="bi bi-x"></i>
        </button>
      </div>
    </div>

    <div class="modal fade" id="editComponentModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5">Редактировать компонент</h1>
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
                    id="editModel"
                    v-model="componentToEdit.model_name"
                    required
                  />
                  <label for="editModel">Модель</label>
                </div>
              </div>

              <div class="col-12">
                <div class="form-floating">
                  <input
                    type="text"
                    class="form-control"
                    id="editSerial"
                    v-model="componentToEdit.serial_number"
                    required
                  />
                  <label for="editSerial">Серийный номер</label>
                </div>
              </div>

              <div class="col-12">
                <div class="form-floating">
                  <input
                    type="text"
                    class="form-control"
                    id="editSpecs"
                    v-model="componentToEdit.specifications"
                  />
                  <label for="editSpecs">Технические характеристики</label>
                </div>
              </div>

              <div class="col-12">
                <div class="form-floating">
                  <input
                    type="number"
                    class="form-control"
                    id="editQuantity"
                    min="0"
                    v-model="componentToEdit.quantity_stock"
                    required
                  />
                  <label for="editQuantity">Кол-во на складе</label>
                </div>
              </div>

              <div class="col-12">
                <div class="form-floating">
                  <input
                    type="text"
                    class="form-control"
                    id="editStatus"
                    v-model="componentToEdit.status"
                    required
                  />
                  <label for="editStatus">Статус</label>
                </div>
              </div>

              <div class="col-12">
                <div class="form-floating">
                  <select class="form-select" id="editCategory" v-model="componentToEdit.category" required>
                    <option :value="g.id" v-for="g in categories" :key="g.id">
                      {{ g.name }}
                    </option>
                  </select>
                  <label for="editCategory">Категория</label>
                </div>
              </div>

              <div class="col-12">
                <label class="form-label">Заменить изображение</label>
                <input
                  class="form-control"
                  type="file"
                  accept="image/*"
                  ref="componentEditPictureRef"
                />
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
              @click="onUpdateComponent"
            >
              Сохранить
            </button>
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
            <img :src="previewPictureUrl" class="img-fluid rounded shadow" alt="Увеличенное фото" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
</style>