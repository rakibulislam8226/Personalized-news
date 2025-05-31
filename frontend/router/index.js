import { createRouter, createWebHistory } from "vue-router";

const routes = [
  {
    path: "/news",
    name: "article.index",
    component: () => import("@/views/articles/Index.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/profile",
    name: "profile.index",
    component: () => import("@/views/auth/Profile.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/register",
    name: "register.index",
    component: () => import("@/views/auth/Register.vue"),
  },
  {
    path: "/login",
    name: "login.index",
    component: () => import("@/views/auth/Login.vue"),
    meta: { guestOnly: true },
  },
  {
    path: "/logout",
    name: "logout.index",
    component: () => import("@/views/auth/Logout.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/:pathMatch(.*)*",
    name: "not-found",
    component: () => import("@views/errors/404.vue"),
  },
  
];

const router = createRouter({
  history: createWebHistory("/"),
  routes,
});
export default router;
