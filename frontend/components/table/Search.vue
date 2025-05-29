<script setup>
const props = defineProps({
  search_data: { default: {} },
  search_fields: { default: {} },
});
</script>

<template>
  <form @submit.prevent="$emit('searchEvent')">
    <div class="row">
      <slot></slot>

      <template v-if="Object.keys(search_fields).length > 0">
        <div class="col-md-2 col-12 pe-0 mb-2">
          <select
            v-model="search_data.field"
            class="form-select form-select-sm"
          >
            <option :value="null" disabled>--Select--</option>

            <option
              v-for="field in search_fields"
              :key="field.key"
              :value="field.key"
            >
              {{ field.title }}
            </option>
          </select>
        </div>
        <div class="col-md-2 col-7 pe-0 mb-2 ps-0">
          <input
            v-model="search_data.value"
            type="text"
            class="form-control form-control-sm"
            placeholder="Type your text..."
          />
        </div>
      </template>

      <!-- <div v-if="search_data.limit" class="col-md-1 col-3 px-0">
        <select
          @change="$emit('searchEvent')"
          v-model="search_data.limit"
          class="form-control form-control-sm text-center"
        >
          <option disabled>Showing</option>
          <option>10</option>
          <option>15</option>
          <option>16</option>
          <option>25</option>
          <option>50</option>
          <option>100</option>
          <option>200</option>
          <option>500</option>
          <option>1000</option>
        </select>
      </div> -->
      <div class="col-1 mb-2 ps-0 d-flex justify-content-between">
        <button
          type="submit"
          :disabled="$root.tableSpinner"
          title="SEARCH"
          class="btn btn-primary btn-sm"
        >
          <div
            v-if="$root.tableSpinner"
            class="spinner-border spinner-border-sm"
          ></div>
          <i v-else class="bi bi-search"></i>
        </button>
        <button
          @click="$emit('resetEvent')"
          v-if="search_data"
          type="button"
          title="Reset Search Parameters"
          class="btn btn-default border btn-sm text-end"
        >
          <i class="bi bi-arrow-counterclockwise"></i>
        </button>
      </div>

      <slot name="right"></slot>
    </div>
  </form>
</template>

<script>
export default {
  props: {
    search_fields: { Array },
    search_data: { Object },
  },
  methods: {
    resetSearch() {
      this.search_data = { ...this.search_data };
      this.search();
      this.hideTooltip;
    },
  },
};
</script>
