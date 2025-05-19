import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  timeout: 5000
})

api.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

api.interceptors.response.use(
  response => response,
  error => {
    if (!error.response) {
      error.response = { data: { detail: 'Brak połączenia z serwerem' } }
    }
    return Promise.reject(error)
  }
)

export default {
  login: (credentials) => api.post('/login/', credentials),
  register: (data) => api.post('/register/', data),
  getNotes: () => api.get('/notes/'),
  createNote: (note) => api.post('/notes/', note),
  updateNote: (id, note) => api.put(`/notes/${id}/`, note),
  deleteNote: (id) => api.delete(`/notes/${id}/`)
}