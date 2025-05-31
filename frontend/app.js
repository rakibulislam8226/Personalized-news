import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import iziToastPlugin from "@/plugins/izitoast.js";
import Input from "@components/form/Input.vue";
import { createPinia } from "pinia";
import axios from "axios";

// Restore token from localStorage if available
const access = localStorage.getItem("access");
if (access) {
  axios.defaults.headers.common["Authorization"] = `Bearer ${access}`;
}

const app = createApp(App);
const pinia = createPinia();
app.use(pinia);
app.use(router);
app.use(iziToastPlugin);
app.component("Input", Input);
app.mount("#app");
