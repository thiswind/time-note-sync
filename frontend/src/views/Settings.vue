<template>
  <div class="settings">
    <van-nav-bar title="设置" left-arrow @click-left="handleBack" />
    <div class="settings-content">
      <van-cell-group inset>
        <van-cell title="账户信息" is-link @click="handleAccountInfo" />
        <van-cell title="关于" is-link @click="handleAbout" />
      </van-cell-group>

      <CalendarSync />

      <div class="logout-section">
        <van-button
          round
          type="danger"
          block
          :loading="loggingOut"
          @click="handleLogout"
        >
          退出登录
        </van-button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { showToast, showConfirmDialog } from 'vant'
import { logout } from '../services/auth'
import CalendarSync from '../components/CalendarSync.vue'

export default {
  name: 'Settings',
  components: {
    CalendarSync,
  },
  setup() {
    const router = useRouter()
    const loggingOut = ref(false)

    const handleBack = () => {
      router.back()
    }

    const handleAccountInfo = () => {
      showToast('账户信息功能开发中')
    }

    const handleAbout = () => {
      showToast('关于功能开发中')
    }

    const handleLogout = async () => {
      try {
        await showConfirmDialog({
          title: '确认退出',
          message: '确定要退出登录吗？',
        })

        loggingOut.value = true
        await logout()
        showToast.success('已退出登录')
        router.push('/login')
      } catch (error) {
        if (error !== 'cancel') {
          showToast.fail('退出登录失败: ' + (error.message || '未知错误'))
        }
      } finally {
        loggingOut.value = false
      }
    }

    return {
      loggingOut,
      handleBack,
      handleAccountInfo,
      handleCalendarSync,
      handleAbout,
      handleLogout,
    }
  },
}
</script>

<style scoped>
.settings {
  min-height: 100vh;
  background-color: #f5f5f5;
}

.settings-content {
  padding: 16px;
}

.logout-section {
  margin-top: 32px;
  padding: 0 16px;
}
</style>

