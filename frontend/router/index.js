import { createRouter, createWebHistory } from "vue-router";

const routes = [
  {
    path: "/news",
    name: "article.index",
    component: () => import("@/views/articles/Index.vue"),
    meta: { requiresAuth: true },
  },
  
];

const router = createRouter({
  history: createWebHistory("/"),
  routes,
});
export default router;
