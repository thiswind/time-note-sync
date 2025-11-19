<template>
  <div class="calendar-sync">
    <van-cell-group inset>
      <van-cell title="日历同步" :value="syncStatusText" />
      <van-cell title="同步模式">
        <template #value>
          <van-radio-group v-model="syncMode" direction="horizontal" @change="handleSyncModeChange">
            <van-radio name="manual">手动</van-radio>
            <van-radio name="automatic">自动</van-radio>
          </van-radio-group>
        </template>
      </van-cell>
      <van-cell>
        <van-button
          type="primary"
          block
          :loading="syncing"
          @click="handleSync"
        >
          立即同步
        </van-button>
      </van-cell>
    </van-cell-group>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import { showToast } from 'vant'
import { syncAPI } from '../services/sync'

export default {
  name: 'CalendarSync',
  setup() {
    const syncing = ref(false)
    const syncMode = ref('manual')
    const lastSyncTime = ref(null)

    const syncStatusText = computed(() => {
      if (lastSyncTime.value) {
        return `最后同步: ${new Date(lastSyncTime.value).toLocaleString('zh-CN')}`
      }
      return '未同步'
    })

    const handleSync = async () => {
      syncing.value = true
      try {
        const result = await syncAPI.syncAll()
        lastSyncTime.value = new Date().toISOString()
        showToast.success(`同步完成: 成功 ${result.success}, 失败 ${result.failed}`)
      } catch (error) {
        showToast.fail('同步失败: ' + (error.message || '未知错误'))
      } finally {
        syncing.value = false
      }
    }

    const handleSyncModeChange = (value) => {
      // TODO: Update sync mode in backend
      showToast('同步模式已更新')
    }

    return {
      syncing,
      syncMode,
      syncStatusText,
      handleSync,
      handleSyncModeChange,
    }
  },
}
</script>

<style scoped>
.calendar-sync {
  padding: 16px;
}
</style>





