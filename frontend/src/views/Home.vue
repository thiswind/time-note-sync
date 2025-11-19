<template>
  <div class="home">
    <van-nav-bar title="我的日志" fixed>
      <template #right>
        <van-icon
          v-if="!isSelectionMode"
          name="plus"
          size="20"
          @click="handleCreate"
          style="margin-right: 16px;"
        />
        <van-icon
          v-if="!isSelectionMode"
          name="setting-o"
          size="20"
          @click="handleSettings"
          style="margin-right: 16px;"
        />
        <van-icon
          v-if="!isSelectionMode"
          name="share-o"
          size="20"
          @click="handleBatchExport"
        />
      </template>
    </van-nav-bar>

    <div class="content">
      <van-tabs v-model:active="activeTab" @change="handleTabChange">
        <van-tab title="全部" name="all">
          <JournalList
            ref="journalListAll"
            :key="'all'"
            @enter-selection-mode="isSelectionMode = true"
            @exit-selection-mode="isSelectionMode = false"
          />
        </van-tab>
        <van-tab title="今天" name="today">
          <JournalList
            ref="journalListToday"
            :key="'today'"
            :date="todayDate"
            @enter-selection-mode="isSelectionMode = true"
            @exit-selection-mode="isSelectionMode = false"
          />
        </van-tab>
        <van-tab title="日期" name="date">
          <div class="date-navigation">
            <div class="date-header">
              <van-button
                icon="arrow-left"
                size="small"
                @click="handlePreviousDate"
              />
              <div class="date-display" @click="showDatePicker = true">
                <span class="date-text">{{ displayDate }}</span>
                <van-icon name="calendar-o" />
              </div>
              <van-button
                icon="arrow-right"
                size="small"
                @click="handleNextDate"
              />
            </div>
            <JournalList
              ref="journalListDate"
              :key="selectedDate"
              :date="selectedDate"
              @enter-selection-mode="isSelectionMode = true"
              @exit-selection-mode="isSelectionMode = false"
            />
          </div>
        </van-tab>
      </van-tabs>
    </div>

    <DatePicker
      v-model="selectedDate"
      v-model:show="showDatePicker"
      @confirm="handleDateConfirm"
    />
  </div>
</template>

<script>
import { ref, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import JournalList from '../components/JournalList.vue'
import DatePicker from '../components/DatePicker.vue'

export default {
  name: 'Home',
  components: {
    JournalList,
    DatePicker,
  },
  setup() {
    const router = useRouter()
    const activeTab = ref('all')
    const showDatePicker = ref(false)
    const isSelectionMode = ref(false)
    const journalListAll = ref(null)
    const journalListToday = ref(null)
    const journalListDate = ref(null)
    const selectedDate = ref(() => {
      const today = new Date()
      return `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, '0')}-${String(today.getDate()).padStart(2, '0')}`
    })

    const todayDate = computed(() => {
      const today = new Date()
      return `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, '0')}-${String(today.getDate()).padStart(2, '0')}`
    })

    const displayDate = computed(() => {
      if (!selectedDate.value) return '选择日期'
      const date = new Date(selectedDate.value)
      return date.toLocaleDateString('zh-CN', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
      })
    })

    const handleCreate = () => {
      router.push('/entry')
    }

    const handleSettings = () => {
      router.push('/settings')
    }

    const handleTabChange = (name) => {
      // Reset to today when switching to date tab
      if (name === 'date' && !selectedDate.value) {
        selectedDate.value = todayDate.value
      }
    }

    const handleDateConfirm = (dateStr) => {
      selectedDate.value = dateStr
    }

    const handlePreviousDate = () => {
      if (!selectedDate.value) return
      const date = new Date(selectedDate.value)
      date.setDate(date.getDate() - 1)
      selectedDate.value = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`
    }

    const handleNextDate = () => {
      if (!selectedDate.value) return
      const date = new Date(selectedDate.value)
      date.setDate(date.getDate() + 1)
      selectedDate.value = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`
    }

    const handleBatchExport = () => {
      // Get the current journal list component based on active tab
      let currentList = null
      if (activeTab.value === 'all') {
        currentList = journalListAll.value
      } else if (activeTab.value === 'today') {
        currentList = journalListToday.value
      } else if (activeTab.value === 'date') {
        currentList = journalListDate.value
      }

      if (currentList && currentList.enterSelectionMode) {
        currentList.enterSelectionMode()
      }
    }

    return {
      activeTab,
      todayDate,
      selectedDate,
      displayDate,
      showDatePicker,
      isSelectionMode,
      journalListAll,
      journalListToday,
      journalListDate,
      handleCreate,
      handleSettings,
      handleTabChange,
      handleDateConfirm,
      handlePreviousDate,
      handleNextDate,
      handleBatchExport,
    }
  },
}
</script>

<style scoped>
.home {
  min-height: 100vh;
  background-color: #f5f5f5;
}

.content {
  padding-top: 46px; /* NavBar height */
}

.date-navigation {
  padding: 16px;
}

.date-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
  padding: 12px;
  background-color: white;
  border-radius: 8px;
}

.date-display {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  flex: 1;
  justify-content: center;
}

.date-text {
  font-size: 16px;
  font-weight: 500;
  color: #323233;
}
</style>
