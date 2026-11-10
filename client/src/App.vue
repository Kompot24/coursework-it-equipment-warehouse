<template>
  <div> 
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark mb-4">
      <div class="container">
        <span class="navbar-brand">IT-Склад ПК</span>

        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNavDropdown"
          aria-controls="navbarNavDropdown"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse justify-content-between" id="navbarNavDropdown">
          <ul class="navbar-nav">
            <li class="nav-item">
              <router-link to="/components" class="nav-link" active-class="active">Компоненты</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/categories" class="nav-link" active-class="active">Категории</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/build-requests" class="nav-link" active-class="active">Заявки на сборку</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/assembly-items" class="nav-link" active-class="active">Детали сборок</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/handover-acts" class="nav-link" active-class="active">Акты выдачи</router-link>
            </li>
          </ul>

          <ul class="navbar-nav">
            <li class="nav-item dropdown">
              <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                Пользователь
              </a>
              <ul class="dropdown-menu">
                <li><a class="dropdown-item" href="/admin">Админка</a></li>
              </ul>
            </li>
          </ul>
        </div>
      </div>
    </nav>
    <main>
      <router-view />
    </main>
  </div>
</template>