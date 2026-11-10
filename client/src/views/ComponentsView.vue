<script setup>
import {computed, onBeforeMount, ref} from 'vue';
import axios from 'axios';
import Cookies from 'js-cookie';

const components = ref([]);
const componentToAdd = ref({});

const categories = ref([]);
const componentToEdit = ref({});

const loading = ref(false);

async function fetchComponents() {
    loading.value = true;
    const r = await axios.get("/api/components/");
    console.log(r.data)
    components.value = r.data;
    loading.value = false;
}

async function fetchCategories() {
    loading.value = true;
    const r = await axios.get("/api/categories/");
    console.log(r.data)
    categories.value = r.data;
    loading.value = false;
}

const categoriesById = computed(() =>
  Object.fromEntries(categories.value.map(c => [c.id, c.name]))
);


onBeforeMount(async () => {
    axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken")
    await fetchCategories();
    await fetchComponents();
})

async function onComponentAdd() {
  await axios.post("/api/components/", componentToAdd.value);
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

async function onStudentEditClick(component) {
  componentToEdit.value = { ...component };
}

async function onUpdateStudent() {
    await axios.put(`/api/components/${componentToEdit.value.id}/`, studentToEdit.value,);
    await fetchStudents();
}

async function onUpdateComponent() {
  const payload = { ...componentToEdit.value };
  const id = payload.id;
  delete payload.id; // id не должен уходить в тело PUT

  await axios.put(`/api/components/${id}/`, payload);
  await fetchComponents();
}

function onEditClick(component) {
    componentToEdit.value = { ...component };
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
                v-model="componentToAdd.model_name"
                required
                />
                <label for="floatingInput">Модель</label>
            </div>
        </div>

        <div class="col-md-3">
            <div class="form-floating">
                <input
                type="text"
                class="form-control"
                v-model="componentToAdd.serial_number"
                required
                />
                <label for="floatingInput">Серийный номер</label>
            </div>
        </div>

        <div class="col-md-3">
            <div class="form-floating">
                <input
                type="text"
                class="form-control"
                v-model="componentToAdd.specifications"
                required
                />
                <label for="floatingInput">Технические характеристики</label>
            </div>
        </div>

        <div class="col-md-3">
            <div class="form-floating">
                <input
                type="text"
                class="form-control"
                v-model="componentToAdd.quantity_stock"
                min="1"
                required
                />
                <label for="floatingInput">Кол-во на складе</label>
            </div>
        </div>

        <div class="col-md-3">
            <div class="form-floating">
                <input
                type="text"
                class="form-control"
                v-model="componentToAdd.status"
                required
                />
                <label for="floatingInput">Статус</label>
            </div>
        </div>

        <div class="col-md-2">
            <div class="form-floating">
                <select class="form-select" v-model="componentToAdd.category" required>
                <option :value="g.id" v-for="g in categories">{{ g.name }}</option>
                </select>
                <label for="floatingInput">Категория</label>
            </div>
        </div>

        <div class="col-12">
        <button class="btn btn-primary">
            Добавить
        </button>
        </div>
    </div>
    </form>
    <h4 class="mb-3">Компоненты на складе</h4>
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
                    <th>Категория (ID)</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="item in components" :key="item.id">
                    <td>{{ item.id }}</td>
                    <td><strong>{{ item.model_name }}</strong></td>
                    <td><code>{{ item.serial_number }}</code></td>
                    <td>{{ item.specifications}}</td>
                    <td>{{ item.quantity_stock }}</td>
                    <td>{{ item.status }}</td>
                    <td>{{ item.category }}</td>
                </tr>
            </tbody>
        </table>
        <h4 class="mb-3">Удалить компонент со склада</h4>
        <div v-for="item in components" class="component-item">
            <div>{{ item.model_name }}</div>
            <button class="btn btn-danger" @click="onRemoveClick(item)">
                <i class="bi bi-x"></i>
            </button>
        </div>
        <div class="modal fade" id="editComponentModal" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h1 class="modal-title fs-5" id="exampleModalLabel">
            редактировать
          </h1>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"
          ></button>
        </div>
        <div class="modal-body">
          <div class="row">
            <div class="col">
              <div class="form-floating">
                <input
                  type="text"
                  class="form-control"
                  v-model="componentToEdit.model_name"
                />
                <label for="floatingInput">Модель</label>
              </div>
            </div>
            <div class="col-auto">
              <div class="form-floating">
                <select class="form-select" v-model="componentToEdit.category">
                  <option :value="g.id" v-for="g in categories">
                    {{ g.name }}
                  </option>
                </select>
                <label for="floatingInput">Категория</label>
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
<div v-for="item in components" class="component-item">
  <div>{{ item.name }}</div>
  <div>{{ categoriesById[item.category]?.name }}</div>
<div>{{ categoriesById[item.category] ?? item.category }}</div>
  <div>
    <button
      class="btn btn-sm btn-success"
      data-bs-toggle="modal"
      data-bs-target="#editComponentModal"
      @click="onEditClick(item)"
    >
      <i class="bi bi-pen-fill"></i>
    </button>
    <button class="btn btn-sm btn-danger" @click="onRemoveClick(item)">
      <i class="bi bi-x"></i>
    </button>
</div>
</div>
    </div>
</template>

<style scoped>
</style>
