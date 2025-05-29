<script setup>
const props = defineProps({
  file: {
    type: String,
  },
});
</script>

<template>
  <div
    v-if="file"
    class="d-flex justify-content-between align-items-center p-1 px-2 mt-2 rounded"
    style="background-color: #334858"
  >
    <span>
      <i class="fa fa-file-pdf text-success"></i>
      {{ file.substring(file.lastIndexOf("/") + 1) }}
    </span>
    <a :href="file" target="_blank" class="btn btn-sm btn-primary"> VIEW </a>
  </div>
</template>
