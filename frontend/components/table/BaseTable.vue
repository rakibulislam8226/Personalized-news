<template>
  <div
    class="table-responsive v-min-height"
    style="--mh: 430px"
    :id="`printArea${model}`"
  >
    <table
      :id="`pdf-table${model}`"
      class="table card-table table-vcenter text-nowrap datatable"
    >
      <thead>
        <tr>
          <slot name="column-start" :index="1"> </slot>
          <th class="sl text-center">#</th>
          <slot name="columns">
            <th
              v-for="(column, index) in table.columns"
              :key="`column${index}`"
              :class="column.class_name"
            >
              <slot :name="`column-${column.field}`" :index="1">
                {{ column.title }}
              </slot>
            </th>

            <th
              v-if="
                Object.keys(table.routes).length > 0 && routesPermissionStatus
              "
              :width="table.routes.width"
              class="text-center"
            >
              Action
            </th>
          </slot>
        </tr>
      </thead>
      <template v-if="!$root.tableSpinner">
        <tbody v-if="Object.keys(table.data).length > 0">
          <tr
            v-for="(item, index) in table.data"
            :key="index"
            :class="`update_item${item.id}`"
          >
            <slot name="data-start" :item="item"> </slot>
            <th class="text-center" v-if="table.meta">
              {{ table.meta.from + index }}
            </th>

            <th v-else class="text-center">{{ index + 1 }}</th>

            <slot
              v-for="(column, index) in table.columns"
              :name="column.field"
              :item="item"
              :index="index"
            >
              <td
                :key="`value${index}`"
                :class="column.class_name"
                :width="column.width"
              >
                <span v-if="column.date">
                  {{
                    date_format(itemValue(item, column.field), column.format)
                  }}
                </span>
                <slot v-else-if="column.image">
                  <img
                    class="img rounded"
                    v-if="column.image && itemValue(item, column.field)"
                    :src="itemValue(item, column.field)"
                    :width="column.imgWidth"
                    :height="column.height"
                  />
                  <small v-else>No Image</small>
                </slot>
                <span v-else-if="column.field == 'status'">
                  <span
                    :class="dangerClass"
                    v-if="
                      [
                        'failed',
                        'cancelled',
                        'rejected',
                        'deactivate',
                      ].includes(itemValue(item, column.field))
                    "
                  >
                    <i class="bi bi-circle-fill me-1"></i>
                    {{ itemValue(item, column.field) }}
                  </span>
                  <span
                    :class="warningClass"
                    v-if="
                      ['in-progress', 'pending'].includes(
                        itemValue(item, column.field)
                      )
                    "
                  >
                    <i class="bi bi-circle-fill me-1"></i>
                    {{ itemValue(item, column.field) }}
                  </span>
                  <span
                    :class="successClass"
                    v-if="
                      [
                        'success',
                        'approved',
                        'published',
                        'ACTIVE',
                        'active',
                        'completed',
                        'done',
                      ].includes(itemValue(item, column.field))
                    "
                  >
                    <i class="bi bi-circle-fill me-1"></i>
                    {{ itemValue(item, column.field) }}
                  </span>
                </span>
                <span v-else>
                  {{ itemValue(item, column.field) }}
                </span>
              </td>
            </slot>

            <td
              v-if="
                Object.keys(table.routes).length > 0 && routesPermissionStatus
              "
              class="text-center"
            >
              <slot name="actions-left" :item="item"> </slot>

              <!-- VIEW BUTTON -->
              <slot name="action-view" :item="item">
                <button
                  v-if="$root.checkPermission(table.routes.view_permission)"
                  type="button"
                  title="View"
                  class="btn btn-success btn-xs me-1"
                  @click="$emit('view-item', item)"
                  :disabled="selected_id == item.id && $root.spinner"
                >
                  <div
                    v-if="selected_id == item.id && $root.spinner"
                    class="action-spinner spinner-border spinner-border-sm"
                  ></div>
                  <i v-else class="bi bi-eye"></i>
                </button>
              </slot>

              <!-- EDIT BUTTON -->
              <slot name="action-edit" :item="item">
                <button
                  :disabled="selected_id == item.id && $root.spinner"
                  class="btn btn-primary btn-xs edit-btn"
                  title="Edit"
                  @click="$emit('edit-item', item)"
                  v-if="
                    table.routes.edit &&
                    $root.checkPermission(table.routes.edit_permission)
                  "
                >
                  <div
                    v-if="selected_id == item.id && $root.spinner"
                    class="action-spinner spinner-border spinner-border-sm"
                  ></div>
                  <i v-else class="bi bi-pencil"></i>
                </button>
              </slot>

              <!-- DELETE BUTTON -->
              <slot name="action-delete" :item="item">
                <AlertBox
                  v-if="
                    table.routes.destroy &&
                    $root.checkPermission(table.routes.destroy_permission)
                  "
                  @confirm="(modal) => destroyItem(item, modal)"
                  :processing="$root.submitting"
                  title="Delete"
                  :btnTriggerIcon="
                    item.status == 'deactivate'
                      ? 'bi bi-check-circle'
                      : 'bi bi-trash'
                  "
                  :btnTriggerClass="
                    item.status == 'deactivate'
                      ? 'ms-1 btn btn-success btn-xs '
                      : 'ms-1 btn btn-danger btn-xs '
                  "
                />
              </slot>

              <slot name="actions-right" :item="item"> </slot>
            </td>
          </tr>
        </tbody>
        <tbody v-else>
          <tr>
            <td :colspan="Object.keys(table.columns).length + 2">
              <p class="mb-0 text-center no-data">No data found.</p>
            </td>
          </tr>
        </tbody>
      </template>
    </table>

    <!-- Table Spinner -->
    <TableSpinner />
  </div>
</template>

<script>
import TableSpinner from "./TableSpinner.vue";
import AlertBox from "./AlertBox.vue";

export default {
  name: "BaseTable",
  components: { TableSpinner, AlertBox },
  props: {
    model: { type: String, default: "" },
    table: {
      type: Object,
      default: {
        meta: {
          from: 1,
        },
        data: [],
        columns: [],
        routes: {},
      },
    },
  },

  data() {
    return {
      selected_id: "",
    };
  },

  computed: {
    routesPermissionStatus() {
      let routes = this.table.routes;

      return Object.keys(routes)
        .filter((key) => key.includes("_permission"))
        .some((key) => {
          return this.$root.checkPermission(routes[key]);
        });
    },
  },

  methods: {
    itemValue(item, column) {
      if (typeof column === "function") {
        return column(item);
      }

      let value = String(column)
        .split(".")
        .reduce((prev, curr) => {
          if (prev instanceof Object) return prev[curr];
        }, item);

      return value;
    },

    destroyItem(item, modal) {
      this.$emit("delete-item", item, modal);
    },
  },

  mounted() {
    this.$eventBus.$on("selectedID", (id) => (this.selected_id = id));
  },
};
</script>
