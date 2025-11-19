<template>
  <div class="journal-entry">
    <van-form @submit="handleSubmit">
      <van-cell-group inset>
        <van-field
          v-model="formData.title"
          name="title"
          label="标题"
          placeholder="输入标题（可选）"
          :rules="[]"
        />
        <van-field
          v-model="formData.date"
          name="date"
          label="日期"
          placeholder="选择日期"
          readonly
          is-link
          @click="showDatePicker = true"
        />
        <van-field
          v-model="formData.content"
          name="content"
          label="内容"
          type="textarea"
          placeholder="输入日志内容"
          rows="10"
          :rules="[{ required: true, message: '内容不能为空' }]"
        />
      </van-cell-group>

      <div class="button-group">
        <van-button
          round
          type="primary"
          native-type="submit"
          block
          :loading="saving"
        >
          {{ entryId ? '保存' : '创建' }}
        </van-button>
        <div v-if="entryId" class="action-buttons">
          <van-button
            round
            type="danger"
            block
            @click="handleDelete"
            :loading="deleting"
            style="margin-bottom: 8px;"
          >
            删除
          </van-button>
          <van-button
            round
            type="primary"
            plain
            block
            @click="handleExport"
            style="margin-bottom: 8px;"
          >
            导出到备忘录
          </van-button>
          <van-button
            round
            type="default"
            plain
            block
            @click="handleOpenCalendar"
            style="margin-bottom: 8px;"
          >
            在日历中打开
          </van-button>
          <van-button
            round
            type="default"
            plain
            block
            @click="handleOpenNotes"
          >
            打开备忘录
          </van-button>
        </div>
      </div>
    </van-form>

    <van-popup v-model:show="showDatePicker" position="bottom">
      <van-date-picker
        v-model="currentDate"
        @confirm="onDateConfirm"
        @cancel="showDatePicker = false"
      />
    </van-popup>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { showToast, showConfirmDialog } from 'vant'
import { journalAPI } from '../services/api'
import { syncAPI } from '../services/sync'
import { openCalendar, openNotes } from '../services/native_app'

export default {
  name: 'JournalEntry',
  setup() {
    const route = useRoute()
    const router = useRouter()
    const entryId = ref(route.params.id ? parseInt(route.params.id) : null)
    const saving = ref(false)
    const deleting = ref(false)
    const showDatePicker = ref(false)

    const formData = reactive({
      title: '',
      content: '',
      date: new Date().toISOString().split('T')[0],
    })

    const currentDate = ref([new Date().getFullYear(), new Date().getMonth() + 1, new Date().getDate()])

    const loadEntry = async () => {
      if (!entryId.value) return

      try {
        const entry = await journalAPI.getEntry(entryId.value)
        formData.title = entry.title || ''
        formData.content = entry.content || ''
        formData.date = entry.date || formData.date
      } catch (error) {
        console.error('Error loading entry:', error)
      }
    }

    const handleSubmit = async () => {
      if (!formData.content.trim()) {
        return
      }

      saving.value = true
      try {
        const entryData = {
          title: formData.title,
          content: formData.content,
          date: formData.date,
        }

        if (entryId.value) {
          await journalAPI.updateEntry(entryId.value, entryData)
        } else {
          await journalAPI.createEntry(entryData)
        }

        showToast.success('保存成功')
        router.push('/')
      } catch (error) {
        console.error('Error saving entry:', error)
        showToast.fail('保存失败: ' + (error.message || '未知错误'))
      } finally {
        saving.value = false
      }
    }

    const handleDelete = async () => {
      if (!entryId.value) return

      try {
        await showConfirmDialog({
          title: '确认删除',
          message: '确定要删除这条日志吗？',
        })
      } catch {
        // User cancelled
        return
      }

      deleting.value = true
      try {
        await journalAPI.deleteEntry(entryId.value)
        showToast.success('删除成功')
        router.push('/')
      } catch (error) {
        console.error('Error deleting entry:', error)
        showToast.fail('删除失败: ' + (error.message || '未知错误'))
      } finally {
        deleting.value = false
      }
    }

    const handleExport = async () => {
      if (!entryId.value) return

      try {
        const shortcutsUrl = await syncAPI.exportEntry(entryId.value)
        // Open Shortcuts URL
        window.location.href = shortcutsUrl
        showToast.success('正在导出到备忘录...')
      } catch (error) {
        console.error('Error exporting entry:', error)
        showToast.fail('导出失败: ' + (error.message || '未知错误'))
      }
    }

    const handleOpenCalendar = async () => {
      try {
        const success = await openCalendar(formData.date)
        if (!success) {
          showToast.fail('无法打开日历应用')
        }
      } catch (error) {
        console.error('Error opening calendar:', error)
        showToast.fail('打开日历失败')
      }
    }

    const handleOpenNotes = async () => {
      try {
        const success = await openNotes()
        if (!success) {
          showToast.fail('无法打开备忘录应用')
        }
      } catch (error) {
        console.error('Error opening notes:', error)
        showToast.fail('打开备忘录失败')
      }
    }

    const onDateConfirm = ({ selectedValues }) => {
      const [year, month, day] = selectedValues
      formData.date = `${year}-${String(month).padStart(2, '0')}-${String(day).padStart(2, '0')}`
      showDatePicker.value = false
    }

    onMounted(() => {
      loadEntry()
    })

    return {
      entryId,
      formData,
      saving,
      deleting,
      showDatePicker,
      currentDate,
      handleSubmit,
      handleDelete,
      handleExport,
      handleOpenCalendar,
      handleOpenNotes,
      onDateConfirm,
    }
  },
}
</script>

<style scoped>
.journal-entry {
  padding: 16px;
}

.button-group {
  margin-top: 24px;
  padding: 0 16px;
}

.button-group .van-button {
  margin-bottom: 12px;
}
</style>

