<template>
  <div class="journal-list">
    <!-- Selection mode toolbar -->
    <van-action-bar v-if="selectionMode">
      <van-action-bar-icon
        icon="cross"
        text="Cancel"
        @click="exitSelectionMode"
      />
      <van-action-bar-button
        type="primary"
        :text="`Export (${selectedEntries.length})`"
        :disabled="selectedEntries.length === 0"
        @click="handleBatchExport"
      />
    </van-action-bar>

    <!-- Entry list -->
    <van-list
      v-model:loading="loading"
      :finished="finished"
      finished-text="没有更多了"
      @load="onLoad"
    >
      <van-cell
        v-for="entry in entries"
        :key="entry.id"
        :title="entry.title"
        :label="formatDate(entry.date)"
        :is-link="!selectionMode"
        @click="handleEntryClick(entry.id, selectionMode)"
      >
        <template #icon v-if="selectionMode">
          <van-checkbox
            :model-value="isSelected(entry.id)"
            @click.stop="toggleSelection(entry.id)"
          />
        </template>
        <template #value>
          <div class="entry-preview">{{ truncateContent(entry.content) }}</div>
          <div v-if="entry.sync_status" class="sync-status">
            <van-icon
              :name="getSyncStatusIcon(entry.sync_status)"
              :color="getSyncStatusColor(entry.sync_status)"
              size="14"
            />
          </div>
        </template>
      </van-cell>
    </van-list>

    <van-empty
      v-if="!loading && entries.length === 0"
      :description="emptyStateMessage"
      image="search"
    />
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { showToast, showLoadingToast, closeToast } from 'vant'
import { journalAPI } from '../services/api'
import { syncAPI } from '../services/sync'

export default {
  name: 'JournalList',
  props: {
    date: {
      type: String,
      default: null,
    },
  },
  emits: ['enter-selection-mode', 'exit-selection-mode'],
  setup(props, { emit }) {
    const router = useRouter()
    const entries = ref([])
    const loading = ref(false)
    const finished = ref(false)
    const total = ref(0)
    const offset = ref(0)
    const limit = 20
    const selectionMode = ref(false)
    const selectedEntries = ref([])

    const formatDate = (dateString) => {
      if (!dateString) return ''
      const date = new Date(dateString)
      return date.toLocaleDateString('zh-CN', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
      })
    }

    const truncateContent = (content) => {
      if (!content) return ''
      return content.length > 50 ? content.substring(0, 50) + '...' : content
    }

    const emptyStateMessage = computed(() => {
      if (props.date) {
        const date = new Date(props.date)
        const dateStr = date.toLocaleDateString('zh-CN', {
          year: 'numeric',
          month: 'long',
          day: 'numeric',
        })
        return `${dateStr} 暂无日志条目`
      }
      return '暂无日志条目'
    })

    const getSyncStatusIcon = (status) => {
      const statusMap = {
        synced: 'success',
        sync_pending: 'clock-o',
        sync_conflict: 'warning-o',
        not_synced: 'circle',
      }
      return statusMap[status] || 'circle'
    }

    const getSyncStatusColor = (status) => {
      const colorMap = {
        synced: '#07c160',
        sync_pending: '#ff976a',
        sync_conflict: '#ee0a24',
        not_synced: '#969799',
      }
      return colorMap[status] || '#969799'
    }

    const loadEntries = async () => {
      if (loading.value || finished.value) return

      loading.value = true
      try {
        const response = await journalAPI.listEntries({
          date: props.date,
          limit,
          offset: offset.value,
        })

        if (response.entries) {
          entries.value.push(...response.entries)
          total.value = response.total
          offset.value += response.entries.length

          if (entries.value.length >= total.value) {
            finished.value = true
          }
        }
      } catch (error) {
        console.error('Error loading entries:', error)
        if (error.message && error.message.includes('Authentication')) {
          // Redirect to login if authentication error
          router.push('/login')
        }
      } finally {
        loading.value = false
      }
    }

    const onLoad = () => {
      loadEntries()
    }

    const handleEntryClick = (entryId, inSelectionMode) => {
      if (inSelectionMode) {
        toggleSelection(entryId)
      } else {
        router.push(`/entry/${entryId}`)
      }
    }

    const toggleSelection = (entryId) => {
      const index = selectedEntries.value.indexOf(entryId)
      if (index > -1) {
        selectedEntries.value.splice(index, 1)
      } else {
        selectedEntries.value.push(entryId)
      }
    }

    const isSelected = (entryId) => {
      return selectedEntries.value.includes(entryId)
    }

    const enterSelectionMode = () => {
      selectionMode.value = true
      selectedEntries.value = []
      emit('enter-selection-mode')
    }

    const exitSelectionMode = () => {
      selectionMode.value = false
      selectedEntries.value = []
      emit('exit-selection-mode')
    }

    const handleBatchExport = async () => {
      if (selectedEntries.value.length === 0) {
        showToast('Please select at least one entry')
        return
      }

      try {
        showLoadingToast({
          message: 'Exporting entries...',
          forbidClick: true,
        })

        const shortcutsUrl = await syncAPI.exportEntries(selectedEntries.value)

        closeToast()

        // Open Shortcuts URL
        window.location.href = shortcutsUrl

        showToast({
          message: `Exporting ${selectedEntries.value.length} entries`,
          type: 'success',
        })

        // Exit selection mode after export
        exitSelectionMode()
      } catch (error) {
        closeToast()
        console.error('Error exporting entries:', error)
        showToast({
          message: error.message || 'Failed to export entries',
          type: 'fail',
        })
      }
    }

    const refresh = () => {
      entries.value = []
      offset.value = 0
      finished.value = false
      loadEntries()
    }

    // Watch for date changes and reload entries
    watch(() => props.date, () => {
      entries.value = []
      offset.value = 0
      finished.value = false
      loadEntries()
    })

    onMounted(() => {
      loadEntries()
    })

    return {
      entries,
      loading,
      finished,
      selectionMode,
      selectedEntries,
      formatDate,
      truncateContent,
      emptyStateMessage,
      getSyncStatusIcon,
      getSyncStatusColor,
      onLoad,
      handleEntryClick,
      toggleSelection,
      isSelected,
      enterSelectionMode,
      exitSelectionMode,
      handleBatchExport,
      refresh,
    }
  },
}
</script>

<style scoped>
.journal-list {
  padding: 0;
}

.entry-preview {
  color: #969799;
  font-size: 12px;
  margin-top: 4px;
}

.sync-status {
  margin-top: 4px;
  display: flex;
  align-items: center;
}

.van-cell__icon {
  margin-right: 8px;
}
</style>

