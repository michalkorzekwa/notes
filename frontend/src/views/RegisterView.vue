<template>
  <div class="form-container">
    <h2>Rejestracja</h2>
    <form @submit.prevent="register">
      <div class="form-group">
        <label>Nazwa użytkownika</label>
        <input v-model="username" required>
        <div v-if="errors.username" class="error">{{ errors.username }}</div>
      </div>

      <div class="form-group">
        <label>Hasło</label>
        <input v-model="password" type="password" required>
        <div v-if="errors.password" class="error">{{ errors.password }}</div>
      </div>

      <div v-if="errors.general" class="error mb-2">{{ errors.general }}</div>
      <button type="submit">Zarejestruj</button>
      <router-link to="/login">Masz już konto? Zaloguj się</router-link>
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
      errors: {}
    }
  },
  methods: {
    async register() {
      this.errors = {}
      try {
        await api.register({
          username: this.username,
          password: this.password
        })
        this.$router.push('/login')
      } catch (error) {
        if (error.response.data.username) {
          this.errors.username = error.response.data.username
        } else {
          this.errors.general = 'Wystąpił błąd podczas rejestracji'
        }
      }
    }
  }
}
</script>