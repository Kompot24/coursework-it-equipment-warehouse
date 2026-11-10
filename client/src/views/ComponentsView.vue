<script setup>
import { computed, onBeforeMount, ref } from 'vue';
import axios from 'axios';
import Cookies from 'js-cookie';

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

async function fetchComponents() {
  loading.value = true;
  const r = await axios.get('/api/components/');
  console.log(r.data);
  components.value = r.data;
  loading.value = false;
}

async function fetchCategories() {
  loading.value = true;
  const r = await axios.get('/api/categories/');
  console.log(r.data);
  categories.value = r.data;
  loading.value = false;
}

const categoriesById = computed(() =>
  Object.fromEntries(categories.value.map(c => [c.id, c.name]))
);

onBeforeMount(async () => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get('csrftoken');
  await fetchCategories();
  await fetchComponents();
});

async function onComponentAdd() {
  await axios.post('/api/components/', componentToAdd.value);
  componentToAdd.value = {
    model_name: '',
    category: '',
    serial_number: '',
    specifications: '',
    quantity_stock: 1,
    status: 'В наличии'
  };
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
  const payload = { ...componentToEdit.value };
  const id = payload.id;
  delete payload.id;

  await axios.put(`/api/components/${id}/`, payload);
  await fetchComponents();
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

        <div class="col-12">
          <button class="btn btn-primary" type="submit">
            Добавить
          </button>
        </div>
      </div>
    </form>

    <h4 class="my-4">Компоненты на складе</h4>
    <div v-if="loading" class="text-muted">Загрузка данных...</div>

    <table v-else class="table table-hover table-bordered">
      <thead class="table-light">
        <tr>
          <th>ID</th>
          <th>Модель</th>
          <th>Серийный номер</th>
          <th>Техническая характеристика</th>
          <th>Кол-во</th>
          <th>Статус</th>
          <th>Категория</th>
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
          class="btn btn-sm btn-outline-success"
          data-bs-toggle="modal"
          data-bs-target="#editComponentModal"
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
  </div>
</template>

<style scoped>
</style>