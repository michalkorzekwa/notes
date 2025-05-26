<template>
  <div class="auth-container">
    <div class="auth-card">
      <h1 class="auth-title">Notes App</h1>
      <div class="auth-form">
        <h2>Rejestracja</h2>
        <form @submit.prevent="handleRegister">
          <div class="form-group">
            <label>Nazwa użytkownika</label>
            <input 
              v-model="username" 
              class="form-input"
              :class="{ 'input-error': errors.username }"
              @input="clearError('username')"
            >
            <div v-if="errors.username" class="error-message">{{ errors.username }}</div>
          </div>

          <div class="form-group">
            <label>Hasło</label>
            <input 
              v-model="password" 
              type="password" 
              class="form-input"
              :class="{ 'input-error': errors.password }"
              @input="clearError('password')"
            >
            <div v-if="errors.password" class="error-message">{{ errors.password }}</div>
          </div>

          <div v-if="errors.general" class="error-message general-error">
            {{ errors.general }}
          </div>

          <button 
            type="submit" 
            class="auth-button"
            :disabled="loading"
          >
            <span v-if="loading">Rejestrowanie...</span>
            <span v-else>Zarejestruj się</span>
          </button>
        </form>
        
        <div class="auth-footer">
          Masz już konto? 
          <router-link to="/login" class="auth-link">Zaloguj się</router-link>
        </div>
      </div>
    </div>
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
      errors: {
        username: '',
        password: '',
        general: ''
      }
    }
  },
  methods: {
    async handleRegister() {
      this.loading = true
      this.clearErrors()
      
      try {
        await api.register({
          username: this.username,
          password: this.password
        })
        this.$router.push('/login')
      } catch (error) {
        if (error.response) {
          const { status, data } = error.response
          
          if (status === 400) {
            for (const field in data) {
              const errorContent = data[field]
              let errorMessage = ''

              const processError = (content) => {
                if (Array.isArray(content)) {
                  return content.map(item => processError(item)).join(' ')
                } else if (typeof content === 'object' && content !== null) {
                  return Object.values(content).map(val => processError(val)).join(' ')
                }
                return String(content).replace(/[[\]{}'"\\]+/g, '')
              }

              errorMessage = processError(errorContent)
              
              errorMessage = errorMessage
                .replace(/^[^:]+:\s*/g, '') 
                .replace(/\s{2,}/g, ' ')

              if (field in this.errors) {
                this.errors[field] = errorMessage
              } else {
                this.errors.general = errorMessage
              }
            }
          } else {
            this.errors.general = 'Wystąpił błąd podczas rejestracji'
          }
        } else {
          this.errors.general = 'Brak połączenia z serwerem'
        }
      } finally {
        this.loading = false
      }
    },
    clearError(field) {
      this.errors[field] = ''
    },
    clearErrors() {
      this.errors = {
        username: '',
        password: '',
        general: ''
      }
    }
  }
}
</script>

<style scoped>
.auth-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #42b983 0%, #3aa876 100%);
}

.auth-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.1);
  width: 100%;
  max-width: 400px;
  overflow: hidden;
}

.auth-title {
  background: #42b983;
  color: white;
  margin: 0;
  padding: 1.5rem;
  text-align: center;
  font-size: 1.8rem;
}

.auth-form {
  padding: 2rem;
}

.auth-form h2 {
  margin: 0 0 2rem 0;
  color: #333;
  text-align: center;
  font-size: 1.5rem;
}

.form-group {
  margin-bottom: 1.5rem;
  width: 100%;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #666;
  font-size: 0.9rem;
  text-align: left;
}

.form-input {
  width: 100%;
  padding: 0.8rem 1rem;
  border: 2px solid #eee;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s;
  box-sizing: border-box;
}

.form-input:focus {
  outline: none;
  border-color: #42b983;
}

.input-error {
  border-color: #ff4444;
}

.error-message {
  color: #ff4444;
  font-size: 0.8rem;
  margin-top: 0.3rem;
  text-align: left;
}

.general-error {
  text-align: center;
  margin: 1rem 0;
  font-size: 0.9rem;
}

.auth-button {
  width: 100%;
  padding: 1rem;
  background: #42b983;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.3s;
  margin-top: 1rem;
}

.auth-button:disabled {
  background: #a0dbb8;
  cursor: not-allowed;
}

.auth-footer {
  text-align: center;
  margin-top: 1.5rem;
  color: #666;
  font-size: 0.9rem;
}

.auth-link {
  color: #42b983;
  text-decoration: none;
  font-weight: 600;
  margin-left: 0.3rem;
}

.auth-link:hover {
  text-decoration: underline;
}
</style>