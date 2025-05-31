<template>
  <div
    class="max-w-md mx-auto lg:mt-40 sm:mt-10 p-6 shadow-md rounded bg-sky-200/20"
  >
    <h2 class="text-2xl font-bold mb-4">Login</h2>
    <form @submit.prevent="submitLogin">
      <input
        v-model="email"
        type="email"
        placeholder="Email"
        class="mb-4 w-full px-3 py-2 border rounded"
      />
      <input
        v-model="password"
        type="password"
        placeholder="Password"
        class="mb-4 w-full px-3 py-2 border rounded"
      />
      <button
        type="submit"
        class="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700"
      >
        Login
      </button>
      <p v-if="error" class="text-red-600 mt-2">{{ error }}</p>
    </form>
    <p class="mt-4 text-sm text-gray-600">
      Don't have an account?
      <router-link to="/register" class="text-blue-600 hover:underline">
        Register
      </router-link>
    </p>
  </div>
</template>

<script setup>
import { ref, inject } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/store/auth";

const $toast = inject("toast");
const email = ref("");
const password = ref("");
const error = ref("");
const router = useRouter();
const auth = useAuthStore();

const submitLogin = async () => {
  error.value = "";
  try {
    await auth.login(email.value, password.value);
    $toast.success("Login successful!");
    router.push("/news");
  } catch (err) {
    error.value = "Invalid credentials";
  }
};
</script>
