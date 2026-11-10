<script setup>
import { computed, onBeforeMount, ref } from 'vue';
import axios from 'axios';
import Cookies from 'js-cookie';

const handoverActs = ref([]);
const handoverActToAdd = ref({
  request: '',
  receiver_user: 1,
  issuer_user: 1,
  inventory_tag: '',
  workplace_location: ''
});

const buildRequests = ref([]);
const handoverActToEdit = ref({});
const loading = ref(false);

async function fetchHandoverActs() {
  loading.value = true;
  const r = await axios.get('/api/handover-acts/');
  console.log(r.data);
  handoverActs.value = r.data;
  loading.value = false;
}

async function fetchBuildRequests() {
  const r = await axios.get('/api/build-requests/');
  buildRequests.value = r.data;
}

const requestsById = computed(() =>
  Object.fromEntries(buildRequests.value.map(req => [req.id, req.target_workload]))
);

onBeforeMount(async () => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get('csrftoken');
  await fetchBuildRequests();
  await fetchHandoverActs();
});

async function onHandoverActAdd() {
  await axios.post('/api/handover-acts/', handoverActToAdd.value);
  handoverActToAdd.value = {
    request: '',
    receiver_user: 1,
    issuer_user: 1,
    inventory_tag: '',
    workplace_location: ''
  };
  await fetchHandoverActs();
}

async function onRemoveClick(act) {
  await axios.delete(`/api/handover-acts/${act.id}/`);
  await fetchHandoverActs();
}

function onEditClick(act) {
  handoverActToEdit.value = { ...act };
}

async function onUpdateHandoverAct() {
  const payload = { ...handoverActToEdit.value };
  const id = payload.id;
  delete payload.id;

  await axios.put(`/api/handover-acts/${id}/`, payload);
  await fetchHandoverActs();
}
</script>

<template>
  <div class="container py-4">
    <h4 class="mb-3">Оформить акт выдачи оборудования</h4>
    <form @submit.prevent.stop="onHandoverActAdd">
      <div class="row g-3">
        <div class="col-md-4">
          <div class="form-floating">
            <select class="form-select" id="actReqSelect" v-model="handoverActToAdd.request" required>
              <option :value="req.id" v-for="req in buildRequests" :key="req.id">
                Заявка #{{ req.id }} ({{ req.target_workload }})
              </option>
            </select>
            <label for="actReqSelect">Заявка на выдачу</label>
          </div>
        </div>

        <div class="col-md-4">
          <div class="form-floating">
            <input
              type="text"
              class="form-control"
              id="tagInput"
              v-model="handoverActToAdd.inventory_tag"
              required
            />
            <label for="tagInput">Инвентарный номер</label>
          </div>
        </div>

        <div class="col-md-4">
          <div class="form-floating">
            <input
              type="text"
              class="form-control"
              id="locationInput"
              v-model="handoverActToAdd.workplace_location"
              required
            />
            <label for="locationInput">Место установки (кабинет)</label>
          </div>
        </div>

        <div class="col-md-6">
          <div class="form-floating">
            <input
              type="number"
              class="form-control"
              id="receiverInput"
              v-model="handoverActToAdd.receiver_user"
              min="1"
              required
            />
            <label for="receiverInput">ID получателя</label>
          </div>
        </div>

        <div class="col-md-6">
          <div class="form-floating">
            <input
              type="number"
              class="form-control"
              id="issuerInput"
              v-model="handoverActToAdd.issuer_user"
              min="1"
              required
            />
            <label for="issuerInput">ID инженера</label>
          </div>
        </div>

        <div class="col-12">
          <button class="btn btn-primary" type="submit">
            Добавить
          </button>
        </div>
      </div>
    </form>

    <h4 class="my-4">Акты выдачи оборудования</h4>
    <div v-if="loading" class="text-muted">Загрузка данных...</div>

    <table v-else class="table table-hover table-bordered">
      <thead class="table-light">
        <tr>
          <th>ID</th>
          <th>Инв. номер</th>
          <th>Кабинет</th>
          <th>Заявка</th>
          <th>Получатель</th>
          <th>Выдал</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in handoverActs" :key="item.id">
          <td>{{ item.id }}</td>
          <td><code>{{ item.inventory_tag }}</code></td>
          <td>{{ item.workplace_location }}</td>
          <td>Заявка #{{ item.request }} ({{ requestsById[item.request] ?? item.request }})</td>
          <td>Пользователь {{ item.receiver_user }}</td>
          <td>Инженер {{ item.issuer_user }}</td>
        </tr>
      </tbody>
    </table>

    <h4 class="my-4">Управление актами</h4>
    <div
      v-for="item in handoverActs"
      :key="item.id"
      class="d-flex align-items-center justify-content-between border p-2 mb-2 rounded bg-light"
    >
      <div>
        <strong>{{ item.inventory_tag }}</strong>
        <span class="text-muted ms-2">({{ item.workplace_location }}, Заявка #{{ item.request }})</span>
      </div>

      <div class="d-flex gap-2">
        <button
          class="btn btn-sm btn-outline-success"
          data-bs-toggle="modal"
          data-bs-target="#editHandoverActModal"
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

    <div class="modal fade" id="editHandoverActModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5">Редактировать акт выдачи</h1>
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
                  <select class="form-select" id="editActReqSelect" v-model="handoverActToEdit.request" required>
                    <option :value="req.id" v-for="req in buildRequests" :key="req.id">
                      Заявка #{{ req.id }} ({{ req.target_workload }})
                    </option>
                  </select>
                  <label for="editActReqSelect">Заявка на выдачу</label>
                </div>
              </div>
              <div class="col-12">
                <div class="form-floating">
                  <input
                    type="text"
                    class="form-control"
                    id="editTagInput"
                    v-model="handoverActToEdit.inventory_tag"
                    required
                  />
                  <label for="editTagInput">Инвентарный номер</label>
                </div>
              </div>
              <div class="col-12">
                <div class="form-floating">
                  <input
                    type="text"
                    class="form-control"
                    id="editLocationInput"
                    v-model="handoverActToEdit.workplace_location"
                    required
                  />
                  <label for="editLocationInput">Место установки (кабинет)</label>
                </div>
              </div>
              <div class="col-12">
                <div class="form-floating">
                  <input
                    type="number"
                    class="form-control"
                    id="editReceiverInput"
                    v-model="handoverActToEdit.receiver_user"
                    min="1"
                    required
                  />
                  <label for="editReceiverInput">ID получателя (User ID)</label>
                </div>
              </div>
              <div class="col-12">
                <div class="form-floating">
                  <input
                    type="number"
                    class="form-control"
                    id="editIssuerInput"
                    v-model="handoverActToEdit.issuer_user"
                    min="1"
                    required
                  />
                  <label for="editIssuerInput">ID инженера (User ID)</label>
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
              @click="onUpdateHandoverAct"
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