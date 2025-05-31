<template>
  <div class="max-w-xl mx-auto p-6 bg-sky-200/10 rounded-xl shadow">
    <h1 class="text-2xl font-bold mb-4">Register</h1>
    <form @submit.prevent="submitForm" class="space-y-4">
      <!-- Email -->
      <Input
        v-model="form.email"
        label="Email"
        type="email"
        placeholder="Email"
        :serverError="serverErrors['email']"
        required
      />

      <!-- Password -->
      <Input
        v-model="form.password"
        label="Password"
        type="password"
        placeholder="Password"
        :serverError="serverErrors['password']"
        required
      />

      <!-- Confirm Password -->
      <Input
        v-model="form.confirm_password"
        label="Confirm Password"
        type="password"
        placeholder="Confirm Password"
        :serverError="serverErrors['confirm_password']"
        required
      />

      <!-- First Name -->
      <Input
        v-model="form.first_name"
        label="First Name"
        placeholder="First Name"
      />

      <!-- Last Name -->
      <Input
        v-model="form.last_name"
        label="Last Name"
        placeholder="Last Name"
      />

      <!-- Countries input with search and multi-select -->

      <div class="relative">
        <Input
          label="Country"
          v-model="searchCountry"
          @input="showDropdown = true"
          @focus="showDropdown = true"
          @blur="onCountryBlur"
          placeholder="Search country..."
          required
        />
        <ul
          v-if="showDropdown && filteredCountries.length"
          class="absolute z-10 bg-white border w-full mt-1 rounded shadow max-h-40 overflow-y-auto"
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
          v-for="(code, index) in form.countries"
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

      <!-- Sources input -->
      <div class="flex items-end gap-2">
        <Input
          label="Source"
          v-model="sourceInput"
          @keydown.enter.prevent="addSource"
          @blur="addSource"
          placeholder="Add source and press Enter or blur"
          required
        />
        <button
          type="button"
          @click="addSource"
          class="h-[42px] px-4 mb-4 bg-green-600 text-white rounded hover:bg-green-700"
        >
          Add
        </button>
      </div>

      <div class="flex flex-wrap gap-2">
        <span
          v-for="(source, index) in form.sources"
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

      <!-- Keywords input -->
      <div class="flex gap-2 items-end">
        <Input
          label="Keywords"
          v-model="keywordInput"
          @keydown.enter.prevent="addKeyword"
          @blur="addKeyword"
          placeholder="Add keyword and press Enter or blur"
        />
        <button
          type="button"
          @click="addKeyword"
          class="h-[42px] px-4 mb-4 bg-yellow-600 text-white rounded hover:bg-yellow-700"
        >
          Add
        </button>
      </div>
      <div class="flex flex-wrap gap-2 mt-2">
        <span
          v-for="(keyword, index) in form.keywords"
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

      <!-- Submit -->
      <button
        type="submit"
        class="w-full bg-blue-700 text-white py-2 rounded hover:bg-blue-800 transition"
      >
        Register
      </button>
    </form>
    <p class="mt-4 text-sm text-gray-600">
      Already have an account? <router-link to="/login" class="text-blue-600">Login</router-link>
    </p>
  </div>
</template>

<script setup>
import { ref, computed, inject } from "vue";
import { useRouter } from "vue-router";
import axios from "@/plugins/axiosConfig.js";
import { countryChoices } from "@/constants/countryChoices.js";

const serverErrors = ref({});
const $toast = inject("toast");
const router = useRouter();

const form = ref({
  email: "",
  password: "",
  confirm_password: "",
  first_name: "",
  last_name: "",
  countries: ["nz"],
  sources: ["BBC News", "CNN"],
  keywords: ["car", "automobile"],
});

const searchCountry = ref("");
const showDropdown = ref(false);

const filteredCountries = computed(() => {
  const search = searchCountry.value.toLowerCase().trim();
  if (!search) return [];
  return Object.entries(countryChoices)
    .filter(([code, name]) => name.toLowerCase().includes(search))
    .map(([code, name]) => ({ code, name }));
});

const selectCountry = (code) => {
  if (!form.value.countries.includes(code)) {
    form.value.countries.push(code);
  }
  searchCountry.value = "";
  showDropdown.value = false;
};

const removeCountry = (index) => {
  form.value.countries.splice(index, 1);
};

const sourceInput = ref("");
const keywordInput = ref("");

const addSource = () => {
  const val = sourceInput.value.trim();
  if (val && !form.value.sources.includes(val)) {
    form.value.sources.push(val);
    sourceInput.value = "";
  }
};

const removeSource = (index) => {
  form.value.sources.splice(index, 1);
};

const addKeyword = () => {
  const val = keywordInput.value.trim();
  if (val && !form.value.keywords.includes(val)) {
    form.value.keywords.push(val);
    keywordInput.value = "";
  }
};

const removeKeyword = (index) => {
  form.value.keywords.splice(index, 1);
};

// Fix blur for country input dropdown - delay to allow click to register
const onCountryBlur = () => {
  setTimeout(() => {
    showDropdown.value = false;
  }, 150);
};

// for converting error pattern to show in form
function flattenErrors(errors) {
  let formattedErrors = {};
  for (const key in errors) {
    if (typeof errors[key] === "object" && !Array.isArray(errors[key])) {
      Object.assign(formattedErrors, errors[key]);
    } else {
      formattedErrors[key] = errors[key];
    }
  }
  return formattedErrors;
}

const submitForm = async () => {
  try {
    const payload = {
      ...form.value,
      countries: form.value.countries,
      sources: form.value.sources,
      keywords: form.value.keywords,
    };

    console.log("Submitting payload:", payload);

    const response = await axios.post("register/", payload);
    $toast.success("Registration successful! Please log in.");
    router.push("/login");
  } catch (error) {
    console.error("Register error caught in submitForm:", error);
    if (error.response.status === 400) {
      serverErrors.value = flattenErrors(error.response.data);
    }
    if (error.response) {
      console.error("Server response data:", error.response.data);
    }
    let errorMessage =
      error.response?.data?.message || "Failed to send invitation.";
    $toast.error(errorMessage);
  }
};
</script>
