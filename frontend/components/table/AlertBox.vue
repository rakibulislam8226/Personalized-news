<template>
  <slot name="trigger" :modal="bsModal">
    <button
      type="button"
      @click.prevent="modal('show')"
      :class="[btnTriggerClass, btnTriggerSize]"
      :disabled="disabled"
      :title="title"
      class="btn"
    >
      <i v-if="btnTriggerIcon" :class="[btnTriggerIcon]"></i>
      {{ btnTriggerText }}
    </button>
  </slot>
  <Teleport to="body">
    <div
      tabindex="-1"
      :ref="bsModalRef"
      class="modal fade modal-sm"
      data-bs-backdrop="static"
      data-bs-keyboard="false"
      aria-labelledby="bs__modal"
      aria-hidden="true"
    >
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-body">
            <slot name="content">
              <slot>
                <div class="mb-4 text-center">
                  <i
                    v-if="icon"
                    :class="[icon]"
                    style="color: #555; font-size: 2rem"
                  ></i>
                  <p class="mt-2 alert-text-title">{{ text }}</p>
                </div>
              </slot>
              <slot name="btn:actions">
                <div
                  class="d-flex mb-3"
                  :class="`justify-content-${actionsAlign}`"
                >
                  <slot name="btn:actions:start"></slot>
                  <button
                    type="button"
                    :disabled="processing"
                    class="btn btn-secondary btn-sm me-2"
                    data-bs-dismiss="modal"
                  >
                    <i class="bi bi-x"></i> {{ btnCancelText }}
                  </button>
                  <button
                    type="button"
                    v-if="showConfirm"
                    @click.prevent="confirm"
                    :disabled="processing"
                    class="btn btn-sm px-3"
                    :class="btnConfirmClass"
                  >
                    <div
                      v-if="processing"
                      class="spinner-grow spinner-grow-sm me-1"
                    ></div>
                    <i v-else class="bi bi-check-circle me-1"></i>
                    <span> {{ btnConfirmText }}</span>
                  </button>
                  <slot name="btn:actions:end"></slot>
                </div>
              </slot>
            </slot>
          </div>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script>
const events = ["show", "shown", "hide", "hidden", "hidePrevented"];

export default {
  name: "AlertBox",

  props: {
    title: { type: String, default: "" },
    text: { type: String, default: "Are you sure?" },
    btnCancelText: { type: String, default: "Cancel" },
    btnConfirmText: { type: String, default: "Confirm" },
    btnConfirmClass: { type: undefined, default: "btn-success" },
    btnTriggerSize: { type: String, default: "btn-xs" },
    btnTriggerIcon: { type: undefined, default: "" },
    btnTriggerText: { type: String, default: "" },
    btnTriggerClass: { type: undefined, default: "" },
    disabled: { type: Boolean, default: false },
    actionsAlign: { type: String, default: "center" },
    showConfirm: { type: Boolean, default: true },
    icon: { type: undefined, default: "bi bi-info-circle-fill" },
    processing: { type: Boolean, default: false },
  },

  emits: [...events, "confirm"],

  data() {
    return {
      bsModal: null,
      bsModalRef: "bootstrap__modal",
    };
  },

  methods: {
    confirm(ev) {
      this.$emit("confirm", this.bsModal, ev);
    },

    modal(method = null, ...args) {
      return this.bsModal[method](...args);
    },

    getInstance() {
      const modal = this.$refs[this.bsModalRef];
      const { Modal } = window.bootstrap;
      return new Modal(modal, this.options);
    },

    registerEvents() {
      const ref = this.$refs[this.bsModalRef];
      events.forEach((en) => {
        ref.addEventListener(`${en}.bs.modal`, (ev) => {
          this.$emit(en, ev);
        });
      });
    },
  },

  mounted() {
    this.bsModal = this.getInstance();
    this.registerEvents();
  },
};
</script>