<template>
  <div class="date-picker">
    <van-popup
      v-model:show="showPicker"
      position="bottom"
      round
      :style="{ height: '50%' }"
    >
      <van-date-picker
        v-model="currentDate"
        :min-date="minDate"
        :max-date="maxDate"
        title="选择日期"
        @confirm="onConfirm"
        @cancel="onCancel"
      />
    </van-popup>
  </div>
</template>

<script>
import { ref, watch } from 'vue'

export default {
  name: 'DatePicker',
  props: {
    modelValue: {
      type: String,
      default: null,
    },
    show: {
      type: Boolean,
      default: false,
    },
  },
  emits: ['update:modelValue', 'update:show', 'confirm', 'cancel'],
  setup(props, { emit }) {
    const showPicker = ref(props.show)
    
    const getInitialDate = () => {
      if (props.modelValue) {
        const date = new Date(props.modelValue)
        return [date.getFullYear(), date.getMonth() + 1, date.getDate()]
      }
      const today = new Date()
      return [today.getFullYear(), today.getMonth() + 1, today.getDate()]
    }
    
    const currentDate = ref(getInitialDate())

    const today = new Date()
    const minDate = new Date(2000, 0, 1)
    const maxDate = new Date(today.getFullYear() + 10, 11, 31)

    watch(() => props.show, (newVal) => {
      showPicker.value = newVal
    })

    watch(showPicker, (newVal) => {
      emit('update:show', newVal)
    })

    watch(() => props.modelValue, (newVal) => {
      if (newVal) {
        const date = new Date(newVal)
        currentDate.value = [date.getFullYear(), date.getMonth() + 1, date.getDate()]
      }
    })

    const onConfirm = ({ selectedValues }) => {
      const [year, month, day] = selectedValues
      const dateStr = `${year}-${String(month).padStart(2, '0')}-${String(day).padStart(2, '0')}`
      emit('update:modelValue', dateStr)
      emit('confirm', dateStr)
      showPicker.value = false
    }

    const onCancel = () => {
      emit('cancel')
      showPicker.value = false
    }

    return {
      showPicker,
      currentDate,
      minDate,
      maxDate,
      onConfirm,
      onCancel,
    }
  },
}
</script>

<style scoped>
.date-picker {
  /* Component styles */
}
</style>

