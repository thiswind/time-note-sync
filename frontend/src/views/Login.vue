<template>
  <div class="login">
    <van-nav-bar title="登录" />
    <div class="login-content">
      <van-form @submit="handleLogin">
        <van-cell-group inset>
          <van-field
            v-model="formData.username"
            name="username"
            label="用户名"
            placeholder="请输入用户名"
            :rules="[{ required: true, message: '请输入用户名' }]"
          />
          <van-field
            v-model="formData.password"
            type="password"
            name="password"
            label="密码"
            placeholder="请输入密码"
            :rules="[{ required: true, message: '请输入密码' }]"
          />
        </van-cell-group>

        <div class="button-group">
          <van-button
            round
            type="primary"
            native-type="submit"
            block
            :loading="loading"
          >
            登录
          </van-button>
        </div>
      </van-form>
    </div>
  </div>
</template>

<script>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { showToast } from 'vant'
import { login } from '../services/auth'

export default {
  name: 'Login',
  setup() {
    const router = useRouter()
    const loading = ref(false)

    const formData = reactive({
      username: '',
      password: '',
    })

    const handleLogin = async () => {
      loading.value = true

      try {
        await login(formData.username, formData.password)
        showToast.success('登录成功')
        router.push('/')
      } catch (error) {
        showToast.fail(error.message || '登录失败，请检查用户名和密码')
      } finally {
        loading.value = false
      }
    }

    return {
      formData,
      loading,
      handleLogin,
    }
  },
}
</script>

<style scoped>
.login {
  min-height: 100vh;
  background-color: #f5f5f5;
}

.login-content {
  padding: 24px 16px;
}

.button-group {
  margin-top: 24px;
  padding: 0 16px;
}
</style>

