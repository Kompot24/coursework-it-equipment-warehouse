<script setup>
import { computed, onBeforeMount, ref } from 'vue';
import axios from 'axios';
import Cookies from 'js-cookie';

const assemblyItems = ref([]);
const assemblyItemToAdd = ref({
  request: '',
  component: '',
  quantity: 1
});

const components = ref([]);
const buildRequests = ref([]);
const assemblyItemToEdit = ref({});
const loading = ref(false);

async function fetchAssemblyItems() {
  loading.value = true;
  const r = await axios.get('/api/assembly-items/');
  console.log(r.data);
  assemblyItems.value = r.data;
  loading.value = false;
}

async function fetchComponents() {
  const r = await axios.get('/api/components/');
  components.value = r.data;
}

async function fetchBuildRequests() {
  const r = await axios.get('/api/build-requests/');
  buildRequests.value = r.data;
}

const componentsById = computed(() =>
  Object.fromEntries(components.value.map(c => [c.id, c.model_name]))
);

const requestsById = computed(() =>
  Object.fromEntries(buildRequests.value.map(req => [req.id, req.target_workload]))
);

onBeforeMount(async () => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get('csrftoken');
  await fetchComponents();
  await fetchBuildRequests();
  await fetchAssemblyItems();
});

async function onAssemblyItemAdd() {
  await axios.post('/api/assembly-items/', assemblyItemToAdd.value);
  assemblyItemToAdd.value = {
    request: '',
    component: '',
    quantity: 1
  };
  await fetchAssemblyItems();
}

async function onRemoveClick(item) {
  await axios.delete(`/api/assembly-items/${item.id}/`);
  await fetchAssemblyItems();
}

function onEditClick(item) {
  assemblyItemToEdit.value = { ...item };
}

async function onUpdateAssemblyItem() {
  const payload = { ...assemblyItemToEdit.value };
  const id = payload.id;
  delete payload.id;

  await axios.put(`/api/assembly-items/${id}/`, payload);
  await fetchAssemblyItems();
}
</script>

<template>
  <div class="container py-4">
    <h4 class="mb-3">Добавить деталь в сборку</h4>
    <form @submit.prevent.stop="onAssemblyItemAdd">
      <div class="row g-3">
        <div class="col-md-5">
          <div class="form-floating">
            <select class="form-select" id="reqSelect" v-model="assemblyItemToAdd.request" required>
              <option :value="req.id" v-for="req in buildRequests" :key="req.id">
                Заявка #{{ req.id }} ({{ req.target_workload }})
              </option>
            </select>
            <label for="reqSelect">Заявка на сборку</label>
          </div>
        </div>

        <div class="col-md-5">
          <div class="form-floating">
            <select class="form-select" id="compSelect" v-model="assemblyItemToAdd.component" required>
              <option :value="c.id" v-for="c in components" :key="c.id">
                {{ c.model_name }}
              </option>
            </select>
            <label for="compSelect">Компонент</label>
          </div>
        </div>

        <div class="col-md-2">
          <div class="form-floating">
            <input
              type="number"
              class="form-control"
              id="quantityAdd"
              v-model="assemblyItemToAdd.quantity"
              min="1"
              required
            />
            <label for="quantityAdd">Количество</label>
          </div>
        </div>

        <div class="col-12">
          <button class="btn btn-primary" type="submit">
            Добавить
          </button>
        </div>
      </div>
    </form>

    <h4 class="my-4">Детали сборок</h4>
    <div v-if="loading" class="text-muted">Загрузка данных...</div>

    <table v-else class="table table-hover table-bordered">
      <thead class="table-light">
        <tr>
          <th>ID</th>
          <th>Заявка</th>
          <th>Компонент</th>
          <th>Количество</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in assemblyItems" :key="item.id">
          <td>{{ item.id }}</td>
          <td>Заявка #{{ item.request }} ({{ requestsById[item.request] ?? item.request }})</td>
          <td><strong>{{ componentsById[item.component] ?? item.component }}</strong></td>
          <td>{{ item.quantity }} шт.</td>
        </tr>
      </tbody>
    </table>

    <h4 class="my-4">Управление деталями сборок</h4>
    <div
      v-for="item in assemblyItems"
      :key="item.id"
      class="d-flex align-items-center justify-content-between border p-2 mb-2 rounded bg-light"
    >
      <div>
        <strong>{{ componentsById[item.component] ?? ('Компонент #' + item.component) }}</strong>
        <span class="text-muted ms-2">(Заявка #{{ item.request }}: {{ requestsById[item.request] ?? item.request }} — {{ item.quantity }} шт.)</span>
      </div>

      <div class="d-flex gap-2">
        <button
          class="btn btn-success"
          data-bs-toggle="modal"
          data-bs-target="#editAssemblyItemModal"
          @click="onEditClick(item)"
        >
          <i class="bi bi-pen-fill"></i>
        </button>

        <button class="btn btn-danger"@click="onRemoveClick(item)">
          <i class="bi bi-x"></i>
        </button>
      </div>
    </div>

    <div class="modal fade" id="editAssemblyItemModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5">Редактировать деталь сборки</h1>
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
                  <select class="form-select" id="editReqSelect" v-model="assemblyItemToEdit.request" required>
                    <option :value="req.id" v-for="req in buildRequests" :key="req.id">
                      Заявка #{{ req.id }} ({{ req.target_workload }})
                    </option>
                  </select>
                  <label for="editReqSelect">Заявка на сборку</label>
                </div>
              </div>
              <div class="col-12">
                <div class="form-floating">
                  <select class="form-select" id="editCompSelect" v-model="assemblyItemToEdit.component" required>
                    <option :value="c.id" v-for="c in components" :key="c.id">
                      {{ c.model_name }}
                    </option>
                  </select>
                  <label for="editCompSelect">Компонент</label>
                </div>
              </div>
              <div class="col-12">
                <div class="form-floating">
                  <input
                    type="number"
                    class="form-control"
                    id="editQuantityInput"
                    v-model="assemblyItemToEdit.quantity"
                    min="1"
                    required
                  />
                  <label for="editQuantityInput">Количество</label>
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
              @click="onUpdateAssemblyItem"
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