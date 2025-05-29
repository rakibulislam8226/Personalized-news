<template>
  <button
    :disabled="this.$root.submitting"
    :title="detail"
    type="submit"
    :class="[
      'btn d-flex justify-content-center align-items-center',
      btnColor,
      btnSize,
      btnClass,
    ]"
  >
    <div
      v-if="this.$root.submitting"
      class="spinner-border spinner-border-sm"
    ></div>

    <template v-else>
      <i
        v-if="icon"
        :class="icon"
        style="font-size: 12px; padding-top: 3px"
      ></i>
      <i
        v-else
        class="bi bi-save"
        style="font-size: 12px; padding-top: 3px"
      ></i>
    </template>

    &nbsp;{{ title }}
  </button>
</template>

<script>
export default {
  props: {
    title: String,
    btnColor: { default: "btn-primary" },
    btnSize: { default: "" },
    btnClass: { default: "" },
    icon: { default: "" },
    detail: {
      type: String,
      default: "",
    },
  },
};
</script>