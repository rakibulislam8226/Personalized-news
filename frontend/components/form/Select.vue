<template>
  <div :class="fieldClass">
    <div class="form-group mb-3">
      <label class="form-label mb-1" :for="id">
        {{ label }}
        <b v-if="required" class="text-danger">*</b>
        <span v-html="hints" class="ms-2"></span>
      </label>

      <slot name="field">
        <select
          :id="id"
          :name="name"
          :value="modelValue"
          @change="handleInput"
          :class="[
            inputClass,
            serverError.length > 0 || error ? 'is-error' : '',
          ]"
        >
          <option value="" selected="true" :disabled="!isNullable">
            --Select Any--
          </option>
          <template v-if="data_val && data_field">
            <option
              v-for="(item, key) in data"
              :key="key"
              :value="item[data_val]"
            >
              {{ itemValue(item, data_field) }}
            </option>
          </template>
          <template v-else>
            <option v-for="(value, key) in data" :key="key">
              {{ value }}
            </option>
          </template>
        </select>
      </slot>

      <!-- client error -->
      <span class="text-danger" :class="error ? 'show' : ''">
        {{ error }}
      </span>

      <!-- server error -->
      <span
        :class="serverError.length > 0 && !error ? 'show' : ''"
        class="text-danger"
      >
        {{ serverError?.[0] }}
      </span>
    </div>
  </div>
</template>

<script>
export default {
  name: "Select",
  props: {
    isNullable: { type: Boolean, default: true },
    modelValue: undefined,
    label: { type: String },
    hints: { type: undefined, default: "" },
    id: { type: String },
    name: { type: String, default: "" },
    data: { default: [] },
    data_field: { type: String, default: "" },
    data_val: { type: String, default: "" },
    fieldClass: { type: String, default: "col-6" },
    inputClass: { type: String, default: "form-control" },
    required: { type: Boolean, default: false },
    error: { type: String, default: "" },
    serverError: { type: String, default: "" },
  },

  emits: ["update:modelValue"],

  methods: {
    handleInput(ev) {
      let val = ev.target.value;
      if (!ev.target.value) val = null;
      this.$emit("update:modelValue", val);
    },

    itemValue(item, column) {
      let value = String(column)
        .split(".")
        .reduce((prev, curr) => {
          if (prev instanceof Object) return prev[curr];
        }, item);

      return value;
    },
  },
};
</script>
