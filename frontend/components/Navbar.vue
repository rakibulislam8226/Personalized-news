<template>
  <nav
    class="bg-sky-500/30 shadow-md px-6 py-3 sticky top-0 z-50 border-b border-gray-200 dark:bg-gray-900 dark:border-gray-200"
    role="navigation"
  >
    <div class="max-w-7xl mx-auto flex justify-between items-center">
      <!-- Logo -->
      <router-link
        to="/news"
        class="text-2xl font-extrabold text-blue-600 hover:text-blue-700 transition"
        aria-label="Homepage"
      >
        <span
          class="self-center text-2xl font-bold whitespace-nowrap dark:text-white"
          ><span class="text-red-500">TOT</span>OS</span
        >
      </router-link>

      <!-- Desktop Menu -->
      <div
        class="hidden md:flex space-x-8 items-center text-gray-400 font-medium"
      >
        <template v-if="auth.isAuthenticated">
          <router-link
            to="/news"
            class="hover:text-blue-600 transition"
            :class="{ 'text-blue-600 font-semibold': isActive('/news') }"
          >
            News
          </router-link>

          <router-link
            to="/profile"
            class="hover:text-blue-600 transition"
            :class="{ 'text-blue-600 font-semibold': isActive('/profile') }"
          >
            Profile
          </router-link>

          <!-- User Icon Button -->
          <div class="relative" ref="dropdownRef">
            <button
              @click="toggleDropdown"
              class="focus:outline-none rounded-full p-1 hover:bg-sky-500/40 transition cursor-pointer"
              aria-haspopup="true"
              :aria-expanded="dropdownOpen.toString()"
              aria-label="User menu"
              type="button"
            >
              <UserSvg class="w-8 h-8 text-gray-700" />
            </button>

            <transition name="fade">
              <div
                v-if="dropdownOpen"
                class="absolute right-0 mt-2 w-44 bg-white border border-gray-200 rounded-lg shadow-lg z-50"
              >
                <router-link
                  to="/profile"
                  class="block px-5 py-3 text-gray-700 hover:bg-gray-100 transition"
                  @click="dropdownOpen = false"
                >
                  Profile
                </router-link>
                <router-link
                  to="/logout"
                  class="block px-5 py-3 text-red-600 hover:bg-red-100 transition"
                  @click="dropdownOpen = false"
                >
                  Logout
                </router-link>
              </div>
            </transition>
          </div>
        </template>

        <template v-else>
          <router-link
            to="/register"
            class="hover:text-blue-600 transition"
            :class="{ 'text-blue-600 font-semibold': isActive('/register') }"
          >
            Register
          </router-link>
          <router-link
            to="/login"
            class="hover:text-blue-600 transition"
            :class="{ 'text-blue-600 font-semibold': isActive('/login') }"
          >
            Login
          </router-link>
        </template>
      </div>

      <!-- Mobile hamburger button -->
      <button
        @click="mobileMenuOpen = !mobileMenuOpen"
        class="md:hidden focus:outline-none focus:ring-2 focus:ring-blue-600 rounded p-1"
        aria-label="Toggle menu"
        :aria-expanded="mobileMenuOpen.toString()"
        type="button"
      >
        <svg
          v-if="!mobileMenuOpen"
          class="w-6 h-6 text-gray-700"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M4 6h16M4 12h16M4 18h16"
          />
        </svg>
        <svg
          v-else
          class="w-6 h-6 text-gray-700"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M6 18L18 6M6 6l12 12"
          />
        </svg>
      </button>
    </div>

    <!-- Mobile Menu -->
    <div
      v-if="mobileMenuOpen"
      class="md:hidden mt-2 space-y-2 bg-white border border-gray-200 rounded shadow-sm p-4"
    >
      <template v-if="auth.isAuthenticated">
        <router-link
          to="/news"
          class="block text-gray-700 hover:text-blue-600 font-medium transition"
          @click="mobileMenuOpen = false"
        >
          News
        </router-link>
        <router-link
          to="/profile"
          class="block text-gray-700 hover:text-blue-600 font-medium transition"
          @click="mobileMenuOpen = false"
        >
          Profile
        </router-link>
        <router-link
          to="/logout"
          class="block text-red-600 hover:text-red-800 font-medium transition"
          @click="mobileMenuOpen = false"
        >
          Logout
        </router-link>
      </template>
      <template v-else>
        <router-link
          to="/register"
          class="block text-gray-700 hover:text-blue-600 font-medium transition"
          @click="mobileMenuOpen = false"
        >
          Register
        </router-link>
        <router-link
          to="/login"
          class="block text-gray-700 hover:text-blue-600 font-medium transition"
          @click="mobileMenuOpen = false"
        >
          Login
        </router-link>
      </template>
    </div>
  </nav>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from "vue";
import { useRoute } from "vue-router";
import { useAuthStore } from "@/store/auth";
import UserSvg from "@svg/User.vue";

const auth = useAuthStore();
const dropdownOpen = ref(false);
const dropdownRef = ref(null);
const mobileMenuOpen = ref(false);

const route = useRoute();

function toggleDropdown() {
  dropdownOpen.value = !dropdownOpen.value;
}

function isActive(path) {
  return route.path === path;
}

// Close dropdown if clicked outside
function handleClickOutside(event) {
  if (dropdownRef.value && !dropdownRef.value.contains(event.target)) {
    dropdownOpen.value = false;
  }
}

onMounted(() => {
  document.addEventListener("click", handleClickOutside);
});
onBeforeUnmount(() => {
  document.removeEventListener("click", handleClickOutside);
});
</script>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
