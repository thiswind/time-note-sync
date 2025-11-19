<template>
  <div class="entry-detail">
    <van-nav-bar
      :title="entryId ? '编辑日志' : '新建日志'"
      left-arrow
      @click-left="handleBack"
    />

    <JournalEntry />
  </div>
</template>

<script>
import { useRoute, useRouter } from 'vue-router'
import JournalEntry from '../components/JournalEntry.vue'

export default {
  name: 'EntryDetail',
  components: {
    JournalEntry,
  },
  setup() {
    const route = useRoute()
    const router = useRouter()
    const entryId = route.params.id

    const handleBack = () => {
      router.back()
    }

    return {
      entryId,
      handleBack,
    }
  },
}
</script>

<style scoped>
.entry-detail {
  min-height: 100vh;
  background-color: #f5f5f5;
}
</style>
