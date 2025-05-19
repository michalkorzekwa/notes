<template>
  <div class="dashboard">
    <div class="toolbar">
      <button @click="createNote">+ Nowa notatka</button>
      <button @click="logout">Wyloguj</button>
    </div>
    <div class="notes-container">
      <NoteItem 
        v-for="note in notes" 
        :key="note.id"
        :note="note"
        @update="handleUpdate"
        @update-position="handlePosition"
        @delete="handleDelete"
      />
    </div>
  </div>
</template>

<script>
import api from '@/services/api'
import NoteItem from '@/components/NoteItem.vue'

export default {
  components: { NoteItem },
  data() {
    return {
      notes: []
    }
  },
  async mounted() {
    await this.loadNotes()
  },
  methods: {
    async loadNotes() {
      try {
        const response = await api.getNotes()
        this.notes = response.data
      } catch (error) {
        console.error(error)
      }
    },
    async createNote() {
      const newNote = {
        title: 'Nowa notatka',
        content: '',
        color: '#ffeb3b',
        position: { x: 100, y: 100 }
      }
      try {
        const response = await api.createNote(newNote)
        this.notes.push(response.data)
      } catch (error) {
        console.error('Błąd tworzenia:', error.response.data)
        alert('Nie udało się utworzyć notatki: ' + error.response.data.detail)
      }
    },
    async handleUpdate(updatedNote) {
    try {
      await api.updateNote(updatedNote.id, updatedNote)
      const index = this.notes.findIndex(n => n.id === updatedNote.id)
      this.notes = [
        ...this.notes.slice(0, index),
        updatedNote,
        ...this.notes.slice(index + 1)
      ]
    } catch (error) {
      console.error(error)
    }
  },
    async handlePosition({ id, position }) {
      try {
        await api.updateNote(id, { position })
      } catch (error) {
        console.error(error)
      }
    },
    async handleDelete(id) {
      try {
        await api.deleteNote(id)
        this.notes = this.notes.filter(note => note.id !== id)
      } catch (error) {
        console.error(error)
      }
    },
    logout() {
      localStorage.removeItem('token')
      this.$router.push('/login')
    }
  }
}
</script>

<style>
.dashboard {
  padding: 20px;
}

.toolbar {
  margin-bottom: 20px;
}

.notes-container {
  position: relative;
  min-height: 500px;
}
</style>