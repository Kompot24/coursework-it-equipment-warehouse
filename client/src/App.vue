<script setup>
import { onMounted } from 'vue';
import axios from 'axios';
import Cookies from 'js-cookie';

onMounted(() => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get('csrftoken');
});
</script>

<template>
  <div>
    <!-- Навигационная панель -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark mb-4">
      <div class="container">
        <span class="navbar-brand">IT-Склад ПК</span>
        <div class="navbar-nav">
          <router-link to="/components" class="nav-link" active-class="active">Компоненты</router-link>
          <router-link to="/categories" class="nav-link" active-class="active">Категории</router-link>
          <router-link to="/build-requests" class="nav-link" active-class="active">Заявки на сборку</router-link>
          <router-link to="/assembly-items" class="nav-link" active-class="active">Детали сборок</router-link>
          <router-link to="/handover-acts" class="nav-link" active-class="active">Акты выдачи</router-link>
        </div>
      </div>
    </nav>

    <!-- Сюда подгружается выбранная страница -->
    <main>
      <router-view />
    </main>
  </div>
</template>

<style scoped>
.nav-link.active {
  font-weight: bold;
  border-bottom: 2px solid #0d6efd;
}
</style>