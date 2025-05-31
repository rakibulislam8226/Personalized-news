<template>
  <div
    class="fixed inset-0 flex items-center justify-center backdrop-blur-sm bg-sky-500/10 z-50"
  >
    <div class="bg-sky-500/20 p-6 rounded-lg shadow-lg max-w-sm w-full text-center">
      <h2 class="text-xl font-bold mb-4">Confirm Logout</h2>
      <p class="text-gray-700 mb-6">Are you sure you want to log out?</p>
      <div class="flex justify-center space-x-4">
        <button
          @click="confirmLogout"
          class="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700 transition"
        >
          Yes, Logout
        </button>
        <button
          @click="cancelLogout"
          class="bg-gray-300 text-gray-800 px-4 py-2 rounded hover:bg-gray-400 transition"
        >
          Cancel
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { inject } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/store/auth";

const auth = useAuthStore();
const router = useRouter();
const $toast = inject("toast");

const confirmLogout = async () => {
  await auth.logout();
  $toast.success("You have been logged out successfully.");
  router.push("/login");
};

const cancelLogout = () => {
  router.push("/news");
};
</script>
