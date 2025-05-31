import { defineStore } from "pinia";
import axios from "axios";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    access: localStorage.getItem("access") || null,
    refresh: localStorage.getItem("refresh") || null,
  }),

  // to access globally auth.isAuthenticated to check user logged info
  getters: {
    isAuthenticated: (state) => !!state.access,
  },
  actions: {
    async login(email, password) {
      const res = await axios.post(
        "/api/v1/token/",
        {
          email,
          password,
        },
        {
          headers: {
            "Content-Type": "application/json",
            Accept: "application/json",
          },
        }
      );
      this.access = res.data.access;
      this.refresh = res.data.refresh;
      localStorage.setItem("access", this.access);
      localStorage.setItem("refresh", this.refresh);

      axios.defaults.headers.common["Authorization"] = `Bearer ${this.access}`;
    },
    async logout() {
      try {
        await axios.post(
          "/api/v1/logout/",
          { refresh: this.refresh },
          {
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${this.access}`,
            },
          }
        );
      } catch (err) {
        console.warn("Logout failed or token already expired");
      }

      // Clear local tokens and Axios header
      this.access = null;
      this.refresh = null;
      localStorage.removeItem("access");
      localStorage.removeItem("refresh");
      delete axios.defaults.headers.common["Authorization"];
    },
  },
});
