<template>
  <div class="max-w-xl mx-auto p-6 bg-white rounded-xl shadow-md">
    <h1 class="text-2xl font-bold mb-6 text-green-600 text-center">Profile</h1>
      <BtnBack @click="$router.go(-1)" abc="efh" />

    <div v-if="profile">
      <form @submit.prevent="updateProfile" class="space-y-6">
        <!-- Email  -->
        <div>
          <label class="block font-semibold mb-1">Email</label>
          <input
            v-model="profile.email"
            type="email"
            disabled
            class="w-full border border-gray-300 px-3 py-2 rounded bg-gray-100"
          />
        </div>

        <!-- First Name -->
        <div>
          <label class="block font-semibold mb-1">First Name</label>
          <input
            v-model="profile.first_name"
            type="text"
            class="w-full border border-gray-300 px-3 py-2 rounded focus:outline-none focus:ring-2 focus:ring-green-400"
          />
        </div>

        <!-- Last Name -->
        <div>
          <label class="block font-semibold mb-1">Last Name</label>
          <input
            v-model="profile.last_name"
            type="text"
            class="w-full border border-gray-300 px-3 py-2 rounded focus:outline-none focus:ring-2 focus:ring-green-400"
          />
        </div>

        <!-- Countries-->
        <div>
          <label class="block font-semibold mb-1">Countries</label>
          <div class="relative">
            <input
              v-model="searchCountry"
              @input="showDropdown = true"
              @focus="showDropdown = true"
              @blur="onCountryBlur"
              type="text"
              placeholder="Search country..."
              class="w-full border border-gray-300 px-3 py-2 rounded focus:outline-none focus:ring-2 focus:ring-green-400"
            />
            <ul
              v-if="showDropdown && filteredCountries.length"
              class="absolute z-10 bg-white border border-gray-300 w-full mt-1 rounded shadow max-h-40 overflow-y-auto"
            >
              <li
                v-for="{ code, name } in filteredCountries"
                :key="code"
                @mousedown.prevent="selectCountry(code)"
                class="px-4 py-2 hover:bg-gray-100 cursor-pointer"
              >
                {{ name }}
              </li>
            </ul>
          </div>

          <div class="flex flex-wrap gap-2 mt-2">
            <div
              v-for="(code, index) in profile.countries"
              :key="code"
              class="flex items-center bg-blue-600 text-white text-sm px-3 py-1 rounded-full"
            >
              {{ countryChoices[code] || code }}
              <button
                type="button"
                class="ml-2 focus:outline-none"
                @click="removeCountry(index)"
                aria-label="Remove country"
              >
                ×
              </button>
            </div>
          </div>
        </div>

        <!-- Sources -->
        <div>
          <label class="block font-semibold mb-1">Sources</label>
          <div class="flex gap-2 items-end">
            <input
              v-model="sourceInput"
              @keydown.enter.prevent="addSource"
              @blur="addSource"
              placeholder="Add source and press Enter or blur"
              class="flex-grow border border-gray-300 px-3 py-2 rounded focus:outline-none focus:ring-2 focus:ring-green-400"
            />
            <button
              type="button"
              @click="addSource"
              class="h-[42px] px-2 md:px-4 bg-green-600 text-white rounded hover:bg-green-700"
            >
              Add
            </button>
          </div>
          <div class="flex flex-wrap gap-2 mt-2">
            <span
              v-for="(source, index) in profile.sources"
              :key="source"
              class="bg-green-600 text-white text-sm px-3 py-1 rounded-full flex items-center"
            >
              {{ source }}
              <button
                type="button"
                class="ml-2 focus:outline-none"
                @click="removeSource(index)"
                aria-label="Remove source"
              >
                ×
              </button>
            </span>
          </div>
        </div>

        <!-- Keywords  -->
        <div>
          <label class="block font-semibold mb-1">Keywords</label>
          <div class="flex gap-2 items-end">
            <input
              v-model="keywordInput"
              @keydown.enter.prevent="addKeyword"
              @blur="addKeyword"
              placeholder="Add keyword and press Enter or blur"
              class="flex-grow border border-gray-300 px-3 py-2 rounded focus:outline-none focus:ring-2 focus:ring-green-400"
            />
            <button
              type="button"
              @click="addKeyword"
              class="h-[42px] px-2 md:px-4 bg-yellow-600 text-white rounded hover:bg-yellow-700"
            >
              Add
            </button>
          </div>
          <div class="flex flex-wrap gap-2 mt-2">
            <span
              v-for="(keyword, index) in profile.keywords"
              :key="keyword"
              class="bg-yellow-600 text-white text-sm px-3 py-1 rounded-full flex items-center"
            >
              {{ keyword }}
              <button
                type="button"
                class="ml-2 focus:outline-none"
                @click="removeKeyword(index)"
                aria-label="Remove keyword"
              >
                ×
              </button>
            </span>
          </div>
        </div>

        <button
          type="submit"
          class="w-full bg-green-600 text-white py-2 rounded hover:bg-green-700 transition"
        >
          Save Changes
        </button>
      </form>
    </div>

    <div v-else class="text-center text-gray-500">Loading profile...</div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, inject } from "vue";
import { useRouter } from "vue-router";
import axios from "@/plugins/axiosConfig.js";
import { countryChoices } from "@/constants/countryChoices.js";

import BtnBack from "@/components/BtnBack.vue";

const profile = ref(null);
const searchCountry = ref("");
const showDropdown = ref(false);

const sourceInput = ref("");
const keywordInput = ref("");

const router = useRouter();
const $toast = inject("toast");

const filteredCountries = computed(() => {
  if (!profile.value) return [];
  const search = searchCountry.value.toLowerCase().trim();
  if (!search) return [];
  return Object.entries(countryChoices)
    .filter(
      ([code, name]) =>
        name.toLowerCase().includes(search) &&
        !profile.value.countries.includes(code)
    )
    .map(([code, name]) => ({ code, name }));
});

// Add country to profile.countries
const selectCountry = (code) => {
  if (profile.value && !profile.value.countries.includes(code)) {
    profile.value.countries.push(code);
  }
  searchCountry.value = "";
  showDropdown.value = false;
};

// Remove country by index
const removeCountry = (index) => {
  if (profile.value) {
    profile.value.countries.splice(index, 1);
  }
};

// Add source tag
const addSource = () => {
  if (!profile.value) return;
  const val = sourceInput.value.trim();
  if (val && !profile.value.sources.includes(val)) {
    profile.value.sources.push(val);
    sourceInput.value = "";
  }
};

// Remove source tag
const removeSource = (index) => {
  if (profile.value) {
    profile.value.sources.splice(index, 1);
  }
};

// Add keyword tag
const addKeyword = () => {
  if (!profile.value) return;
  const val = keywordInput.value.trim();
  if (val && !profile.value.keywords.includes(val)) {
    profile.value.keywords.push(val);
    keywordInput.value = "";
  }
};

// Remove keyword tag
const removeKeyword = (index) => {
  if (profile.value) {
    profile.value.keywords.splice(index, 1);
  }
};

const onCountryBlur = () => {
  setTimeout(() => {
    showDropdown.value = false;
  }, 150);
};

const fetchProfile = async () => {
  try {
    const response = await axios.get("profile/");
    profile.value = response.data;

    if (!Array.isArray(profile.value.countries)) profile.value.countries = [];
    if (!Array.isArray(profile.value.sources)) profile.value.sources = [];
    if (!Array.isArray(profile.value.keywords)) profile.value.keywords = [];
  } catch (error) {
    console.error("Failed to fetch profile:", error);
  }
};

const updateProfile = async () => {
  if (!profile.value) return;

  const updatedData = {
    first_name: profile.value.first_name,
    last_name: profile.value.last_name,
    countries: profile.value.countries,
    sources: profile.value.sources,
    keywords: profile.value.keywords,
  };

  try {
    const response = await axios.patch("profile/", updatedData);
    profile.value = response.data;
    $toast.success("Profile updated successfully.");
    router.push("/news");
  } catch (error) {
    console.error("Update failed:", error);
    $toast.error("Failed to update profile.");
  }
};

onMounted(() => {
  fetchProfile();
});
</script>
