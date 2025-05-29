<template>
  <div
    v-if="meta && !$root.tableSpinner"
    class="flex flex-col md:flex-row items-center justify-between px-4 py-3 border-t border-gray-200 bg-white"
  >
    <div v-if="historyCount" class="text-sm text-gray-600 mb-2 md:mb-0">
      Showing
      <span class="font-semibold">{{ num_format(meta.from, 0) }}</span>
      to
      <span class="font-semibold">{{ num_format(meta.to, 0) }}</span>
      of total
      <span class="font-semibold">{{ num_format(meta.total, 0) }}</span>
      entries
    </div>

    <ul
      v-if="meta.num_pages > 1"
      :class="[msAuto]"
      class="inline-flex -space-x-px rounded-md shadow-sm"
    >
      <!-- pagination buttons here -->
      <li v-if="firstLast">
        <a
          :class="[
            'relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-gray-500 hover:bg-gray-50 cursor-pointer',
            { 'opacity-50 cursor-not-allowed': !meta.has_previous },
          ]"
          href="javascript:void(0)"
          @click="meta.has_previous ? $emit('search-event', 1) : ''"
        >
          <LeftSvg />
        </a>
      </li>
      <li>
        <a
          :class="[
            'relative inline-flex items-center px-2 py-2 border border-gray-300 bg-white text-gray-500 hover:bg-gray-50 cursor-pointer',
            { 'opacity-50 cursor-not-allowed': !meta.has_previous },
          ]"
          href="javascript:void(0)"
          @click="
            meta.has_previous
              ? $emit('search-event', meta.current_page - 1)
              : ''
          "
        >
          <PrevSvg />
        </a>
      </li>

      <template v-for="num in pageNumbers" :key="num">
        <li>
          <a
            :class="[
              'relative inline-flex items-center px-4 py-2 border border-gray-300 cursor-pointer',
              num === meta.current_page
                ? 'bg-green-600 text-white cursor-default'
                : 'bg-white text-gray-700 hover:bg-gray-100',
            ]"
            href="javascript:void(0)"
            @click="
              num !== meta.current_page ? $emit('search-event', num) : null
            "
          >
            {{ num }}
          </a>
        </li>
      </template>

      <template v-if="meta.num_pages > range && !isShowingLastPage">
        <li>
          <a
            class="relative inline-flex items-center px-3 py-2 border border-gray-300 bg-white text-gray-500 cursor-default"
            href="javascript:void(0)"
          >
            <DotSvg />
          </a>
        </li>
        <li>
          <a
            class="relative inline-flex items-center px-4 py-2 border border-gray-300 bg-white text-gray-700 hover:bg-gray-100 cursor-pointer"
            href="javascript:void(0)"
            @click="$emit('search-event', meta.num_pages)"
          >
            {{ meta.num_pages }}
          </a>
        </li>
      </template>

      <li>
        <a
          :class="[
            'relative inline-flex items-center px-2 py-2 border border-gray-300 bg-white text-gray-500 hover:bg-gray-50 cursor-pointer',
            { 'opacity-50 cursor-not-allowed': !meta.has_next },
          ]"
          href="javascript:void(0)"
          @click="
            meta.has_next ? $emit('search-event', meta.current_page + 1) : ''
          "
        >
          <NextSvg />
        </a>
      </li>
      <li v-if="firstLast">
        <a
          :class="[
            'relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-gray-500 hover:bg-gray-50 cursor-pointer',
            { 'opacity-50 cursor-not-allowed': !meta.has_next },
          ]"
          href="javascript:void(0)"
          @click="meta.has_next ? $emit('search-event', meta.num_pages) : ''"
        >
          <RightSvg />
        </a>
      </li>
    </ul>
  </div>
</template>

<script>
import LeftSvg from "@svg/Left.vue";
import PrevSvg from "@svg/Prev.vue";
import RightSvg from "@svg/Right.vue";
import NextSvg from "@svg/Next.vue";
import DotSvg from "@svg/Dot.vue";

export default {
  name: "Pagination",

  components: { LeftSvg, PrevSvg, RightSvg, NextSvg, DotSvg },

  props: ["meta"],
  props: {
    meta: {
      type: Object,
      default: {},
    },
    msAuto: {
      default: "ms-auto",
    },
    firstLast: {
      type: Boolean,
      default: true,
    },
    historyCount: {
      type: Boolean,
      default: true,
    },
    range: {
      type: undefined,
      default: 8,
    },
  },
  computed: {
    pageNumbers() {
      const startPage = Math.max(
        1,
        Math.min(
          this.meta.current_page - Math.floor(this.range / 2),
          this.meta.num_pages - this.range + 1
        )
      );
      const endPage = Math.min(this.meta.num_pages, startPage + this.range - 1);
      return Array.from(
        { length: endPage - startPage + 1 },
        (_, i) => startPage + i
      );
    },
    isShowingLastPage() {
      return this.pageNumbers.includes(this.meta.num_pages);
    },
  },
  methods: {
    num_format(value, decimals = 0) {
      return Number(value).toLocaleString(undefined, {
        minimumFractionDigits: decimals,
        maximumFractionDigits: decimals,
      });
    },
  },
};
</script>
