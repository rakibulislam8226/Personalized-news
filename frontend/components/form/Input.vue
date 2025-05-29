<template>
  <div :class="fieldClass">
    <div class="mb-4">
      <!-- Label -->
      <label :for="id" class="block text-sm font-medium text-gray-700 mb-1">
        <span v-html="label"></span>
        <b v-if="required" class="text-red-600">&nbsp;*</b>
        <slot name="lable"></slot>
      </label>

      <!-- Default input or custom slot -->
      <slot name="field">
        <input
          :id="id"
          :type="type"
          :step="step"
          :name="name"
          :value="modelValue"
          @input="handleInput"
          :class="[
            inputClass,
            'w-full px-3 py-2 border rounded shadow-sm focus:outline-none transition',
            serverError?.length > 0 || error
              ? 'border-red-500 focus:border-red-500 focus:ring-red-300'
              : 'border-gray-300 focus:border-blue-500 focus:ring-blue-300'
          ]"
          :placeholder="placeholder"
          autocomplete="off"
          :readonly="readonly"
          :disabled="disabled"
          :min="min"
        />
      </slot>

      <!-- Hints slot -->
      <slot name="hints"></slot>

      <!-- Client-side error -->
      <p v-if="error" class="text-sm text-red-600 mt-1">{{ error }}</p>

      <!-- Server-side error -->
      <p v-else-if="serverError?.length > 0" class="text-sm text-red-600 mt-1">
        {{ serverError[0] }}
      </p>
    </div>
  </div>
</template>

<script>
export default {
  name: "Input",
  props: {
    modelValue: undefined,
    label: String,
    id: String,
    name: { type: String, default: "" },
    type: { type: String, default: "text" },
    step: { default: 0 },
    fieldClass: { type: String, default: "w-full" },
    inputClass: { type: String, default: "" }, 
    readonly: { type: Boolean, default: false },
    disabled: { type: Boolean, default: false },
    required: { type: Boolean, default: false },
    placeholder: { type: String, default: "" },
    error: { type: String, default: "" },
    serverError: { default: () => [] },
    min: { default: "" },
  },
  emits: ["update:modelValue"],
  methods: {
    handleInput(ev) {
      this.$emit("update:modelValue", ev.target.value);
    },
  },
};
</script>
