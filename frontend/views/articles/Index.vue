<template>
  <div class="max-w-6xl mx-auto px-4 py-8">
    
    <div v-if="data.length">
      <h1 class="text-4xl font-bold text-green-600 mb-8 text-center">Top News</h1>
      <div
        class="flex flex-col md:flex-row md:items-end md:justify-between gap-4 mb-8"
      >
        <!-- Search -->
        <div class="flex-1">
          <label class="block mb-1 text-sm font-medium text-gray-700"
            >Search</label
          >
          <input
            v-model="searchQuery"
            @input="handleSearch"
            type="text"
            placeholder="Search articles..."
            class="w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <!-- Source Filter -->
        <div class="flex-1">
          <label class="block mb-1 text-sm font-medium text-gray-700"
            >Source</label
          >
          <select
            v-model="selectedSource"
            @change="handleFilters"
            class="w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">All Sources</option>
            <option
              v-for="source in availableSources"
              :key="source"
              :value="source"
            >
              {{ source }}
            </option>
          </select>
        </div>

        <!-- Date Filter -->
        <div class="flex-1">
          <label class="block mb-1 text-sm font-medium text-gray-700"
            >Published After</label
          >
          <input
            type="date"
            v-model="publishedAfter"
            @change="handleFilters"
            class="w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
      </div>
      <!-- First article -->
      <div class="mb-10" v-if="data[0]">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <img
            :src="data[0].article.url_to_image"
            alt="Article Image"
            class="w-full h-72 object-cover rounded-lg shadow"
          />
          <div>
            <h2 class="text-2xl font-bold mb-2">
              {{ data[0].article.title }}
            </h2>
            <p class="text-gray-700 mb-2">{{ data[0].article.source_name }}</p>
            <p class="text-gray-500 mb-4 text-sm">
              {{ formatDate(data[0].article.published_at) }}
            </p>
            <p class="text-gray-700 mb-4">{{ data[0].article.description }}</p>
            <a
              :href="data[0].article.url"
              target="_blank"
              class="inline-block bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition"
            >
              Read more
            </a>
          </div>
        </div>
      </div>

      <!-- Other articles -->
      <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div
          v-for="(item, index) in data.slice(1)"
          :key="item.id"
          class="bg-white rounded-lg shadow hover:shadow-md transition overflow-hidden"
        >
          <img
            :src="item.article.url_to_image"
            alt="Article Image"
            class="w-full h-40 object-cover"
          />
          <div class="p-4">
            <h3 class="text-lg font-semibold mb-1">
              {{ item.article.title }}
            </h3>
            <p class="text-xs text-gray-500 mb-1">
              {{ item.article.source_name }} ·
              {{ formatDate(item.article.published_at) }}
            </p>
            <p class="text-sm text-gray-600 mb-3">
              {{ item.article.description }}
            </p>
            <a
              :href="item.article.url"
              target="_blank"
              class="text-blue-600 hover:underline text-sm font-medium"
            >
              Read more →
            </a>
          </div>
        </div>
      </div>

      <!-- Pagination -->
      <Pagination
        v-if="meta && meta.num_pages > 1"
        :meta="meta"
        @search-event="handlePageChange"
      />
    </div>

    <div v-else class="text-center py-16 text-gray-500">
        <p>No articles found.</p>
    </div>
  </div>
</template>

<script setup>
import axios from "@/plugins/axiosConfig.js";
import { ref, onMounted } from "vue";
import debounce from "lodash.debounce";
import Pagination from "@/components/table/Pagination.vue";

const data = ref([]);
const meta = ref(null);
const currentPage = ref(1);
const searchQuery = ref("");
const selectedSource = ref("");
const availableSources = ref([]);
const publishedAfter = ref("");

const fetchSources = async () => {
  try {
    const response = await axios.get("articles/sources/");
    availableSources.value = response.data.sources;
  } catch (error) {
    console.error("Failed to fetch sources", error);
  }
};

const fetchArticlesList = async (page = 1, search = "") => {
  try {
    const response = await axios.get("articles/", {
      params: {
        page,
        search: search.trim(),
        source: selectedSource.value,
        published_after: publishedAfter.value,
      },
    });
    data.value = response.data.data || [];
    meta.value = response.data.meta || null;
    currentPage.value = page;
  } catch (error) {
    console.error(error);
    data.value = [];
    meta.value = null;
  }
};

const handlePageChange = (page) => {
  if (page !== currentPage.value) {
    fetchArticlesList(page);
  }
};

const handleSearch = debounce(() => {
  fetchArticlesList(1, searchQuery.value);
}, 400);

const handleFilters = () => {
  fetchArticlesList(1);
};

const formatDate = (dateStr) => {
  return new Date(dateStr).toISOString().slice(0, 10);
};

onMounted(() => {
  fetchArticlesList();
  fetchSources();
});
</script>
