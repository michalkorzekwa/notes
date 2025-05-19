<template>
  <div class="form-container">
    <h2>Logowanie</h2>
    <form @submit.prevent="handleLogin">
      <div class="form-group">
        <label>Nazwa użytkownika</label>
        <input v-model="username" required>
      </div>
      
      <div class="form-group">
        <label>Hasło</label>
        <input v-model="password" type="password" required>
      </div>

      <button type="submit" :disabled="loading">
        {{ loading ? 'Ładowanie...' : 'Zaloguj' }}
      </button>
      <p v-if="error" class="error">{{ error }}</p>
    </form>
  </div>
</template>

<script>
import api from '@/services/api'

export default {
  data() {
    return {
      username: '',
      password: '',
      loading: false,
      error: ''
    }
  },
  methods: {
    async handleLogin() {
      this.loading = true
      this.error = ''
      try {
        const response = await api.login({
          username: this.username,
          password: this.password
        })
        localStorage.setItem('token', response.data.access)
        this.$router.push('/dashboard')
      } catch (error) {
        this.error = 'Błędne dane logowania'
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.form-container {
  max-width: 400px;
  margin: 2rem auto;
  padding: 20px;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
}

button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.error {
  color: red;
}
</style>