<script setup>
import { onBeforeMount, ref } from 'vue';
import axios from 'axios';
import Cookies from 'js-cookie';

const buildRequests = ref([]);
const buildRequestToAdd = ref({
  employee: 1,
  target_workload: '',
  request_type: 'assembly',
  status: 'pending',
  comment: ''
});

const buildRequestToEdit = ref({});
const loading = ref(false);

async function fetchBuildRequests() {
  loading.value = true;
  const r = await axios.get('/api/build-requests/');
  console.log(r.data);
  buildRequests.value = r.data;
  loading.value = false;
}

onBeforeMount(async () => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get('csrftoken');
  await fetchBuildRequests();
});

async function onBuildRequestAdd() {
  await axios.post('/api/build-requests/', buildRequestToAdd.value);
  buildRequestToAdd.value = {
    employee: 1,
    target_workload: '',
    request_type: 'assembly',
    status: 'pending',
    comment: ''
  };
  await fetchBuildRequests();
}

async function onRemoveClick(item) {
  await axios.delete(`/api/build-requests/${item.id}/`);
  await fetchBuildRequests();
}

function onEditClick(item) {
  buildRequestToEdit.value = { ...item };
}

async function onUpdateBuildRequest() {
  const payload = { ...buildRequestToEdit.value };
  const id = payload.id;
  delete payload.id;

  await axios.put(`/api/build-requests/${id}/`, payload);
  await fetchBuildRequests();
}
</script>

<template>
  <div class="container py-4">
    <h4 class="mb-3">Создать заявку на сборку</h4>
    <form @submit.prevent.stop="onBuildRequestAdd">
      <div class="row g-3">
        <div class="col-md-4">
          <div class="form-floating">
            <input
              type="text"
              class="form-control"
              id="workloadInput"
              v-model="buildRequestToAdd.target_workload"
              required
            />
            <label for="workloadInput">Под какие цели</label>
          </div>
        </div>

        <div class="col-md-3">
          <div class="form-floating">
            <input
              type="number"
              class="form-control"
              id="employeeInput"
              v-model="buildRequestToAdd.employee"
              min="1"
              required
            />
            <label for="employeeInput">ID сотрудника</label>
          </div>
        </div>

        <div class="col-md-2">
          <div class="form-floating">
            <select class="form-select" id="typeSelect" v-model="buildRequestToAdd.request_type" required>
              <option value="assembly">Сборка</option>
              <option value="upgrade">Апгрейд</option>
            </select>
            <label for="typeSelect">Тип заявки</label>
          </div>
        </div>

        <div class="col-md-3">
          <div class="form-floating">
            <select class="form-select" id="statusSelect" v-model="buildRequestToAdd.status" required>
              <option value="pending">Ожидает</option>
              <option value="in_progress">В сборке</option>
              <option value="completed">Готово</option>
              <option value="cancelled">Отменено</option>
            </select>
            <label for="statusSelect">Статус</label>
          </div>
        </div>

        <div class="col-12">
          <div class="form-floating">
            <input
              type="text"
              class="form-control"
              id="commentInput"
              v-model="buildRequestToAdd.comment"
            />
            <label for="commentInput">Комментарий к заявке</label>
          </div>
        </div>

        <div class="col-12">
          <button class="btn btn-primary" type="submit">
            Добавить
          </button>
        </div>
      </div>
    </form>

    <h4 class="my-4">Заявки на сборку</h4>
    <div v-if="loading" class="text-muted">Загрузка данных...</div>

    <table v-else class="table table-hover table-bordered">
      <thead class="table-light">
        <tr>
          <th>ID</th>
          <th>Назначение</th>
          <th>ID сотрудника</th>
          <th>Тип</th>
          <th>Статус</th>
          <th>Комментарий</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in buildRequests" :key="item.id">
          <td>{{ item.id }}</td>
          <td><strong>{{ item.target_workload }}</strong></td>
          <td>{{ item.employee }}</td>
          <td>{{ item.request_type }}</td>
          <td>{{ item.status }}</td>
          <td>{{ item.comment }}</td>
        </tr>
      </tbody>
    </table>

    <h4 class="my-4">Управление заявками</h4>
    <div
      v-for="item in buildRequests"
      :key="item.id"
      class="d-flex align-items-center justify-content-between border p-2 mb-2 rounded bg-light"
    >
      <div>
        <strong>Заявка #{{ item.id }}: {{ item.target_workload }}</strong>
        <span class="text-muted ms-2">(Статус: {{ item.status }}, Сотрудник ID: {{ item.employee }})</span>
      </div>

      <div class="d-flex gap-2">
        <button
          class="btn btn-sm btn-outline-success"
          data-bs-toggle="modal"
          data-bs-target="#editBuildRequestModal"
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

    <div class="modal fade" id="editBuildRequestModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5">Редактировать заявку</h1>
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
                    id="editWorkload"
                    v-model="buildRequestToEdit.target_workload"
                    required
                  />
                  <label for="editWorkload">Назначение</label>
                </div>
              </div>
              <div class="col-12">
                <div class="form-floating">
                  <input
                    type="number"
                    class="form-control"
                    id="editEmployee"
                    v-model="buildRequestToEdit.employee"
                    min="1"
                    required
                  />
                  <label for="editEmployee">ID сотрудника</label>
                </div>
              </div>
              <div class="col-12">
                <div class="form-floating">
                  <select class="form-select" id="editType" v-model="buildRequestToEdit.request_type" required>
                    <option value="assembly">Сборка</option>
                    <option value="upgrade">Апгрейд</option>
                  </select>
                  <label for="editType">Тип заявки</label>
                </div>
              </div>
              <div class="col-12">
                <div class="form-floating">
                  <select class="form-select" id="editStatusSelect" v-model="buildRequestToEdit.status" required>
                    <option value="pending">Ожидает</option>
                    <option value="in_progress">В сборке</option>
                    <option value="completed">Готово</option>
                    <option value="cancelled">Отменено</option>
                  </select>
                  <label for="editStatusSelect">Статус</label>
                </div>
              </div>
              <div class="col-12">
                <div class="form-floating">
                  <input
                    type="text"
                    class="form-control"
                    id="editComment"
                    v-model="buildRequestToEdit.comment"
                  />
                  <label for="editComment">Комментарий</label>
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
              @click="onUpdateBuildRequest"
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