import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  timeout: 10000
})

api.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

api.interceptors.response.use(
  response => {
    return response
  },
  error => {
    return Promise.reject(error)
  }
)

export default {
  createNote: (note) => {
    
    return api.post('/notes/', note)
  },
  login: (credentials) => api.post('/login/', credentials),
  register: (data) => api.post('/register/', data),
  getNotes: () => api.get('/notes/'),
  updateNote: (id, note) => api.put(`/notes/${id}/`, note),
  deleteNote: (id) => api.delete(`/notes/${id}/`)
}