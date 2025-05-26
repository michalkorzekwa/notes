<template>
  <div class="dashboard">
    <div class="toolbar">
      <button @click="createNote" class="toolbar-button">+ Nowa notatka</button>
      <button @click="logout" class="toolbar-button">Wyloguj</button>
    </div>
    
    <div class="board">
      <div 
        v-for="status in statuses" 
        :key="status" 
        class="status-column"
        @dragover.prevent
        @drop="onDrop($event, status)"
      >
        <h3 class="status-title">{{ statusLabels[status] }}</h3>
        <div class="notes-container">
          <NoteItem
            v-for="(note, index) in filteredNotes(status)"
            :key="note.id"
            :note="note"
            :style="getNoteStyle(index)"
            @update="handleUpdate"
            @update-position="handlePosition"
            @delete="handleDelete"
          />
        </div>
      </div>
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
      notes: [],
      statuses: ['todo', 'in_progress', 'done'],
      statusLabels: {
        todo: 'Do zrobienia',
        in_progress: 'W trakcie',
        done: 'Zrobione'
      }
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
        position: { x: 20, y: 20 },
        status: 'todo'
      }
      try {
        const response = await api.createNote(newNote)
        this.notes = [...this.notes, response.data]
      } catch (error) {
        console.error(error)
      }
    },
    getNoteStyle(index) {
      return {
        top: `${index * 220}px`,
        left: '20px'
      }
    },
    async handleUpdate(updatedNote) {
      try {
        await api.updateNote(updatedNote.id, updatedNote)
        const index = this.notes.findIndex(n => n.id === updatedNote.id)
        this.notes.splice(index, 1, updatedNote)
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
    },
    filteredNotes(status) {
      return this.notes.filter(note => note.status === status)
    },
    onDrop(event, newStatus) {
      const noteId = event.dataTransfer.getData('noteId')
      const note = this.notes.find(n => n.id == noteId)
      if (note) {
        this.handleUpdate({...note, status: newStatus})
      }
    }
  }
}
</script>

<style>
.dashboard {
  padding: 20px;
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: #f0f2f5;
}

.toolbar {
  margin-bottom: 20px;
  display: flex;
  gap: 10px;
}

.toolbar-button {
  padding: 10px 20px;
  border: none;
  border-radius: 6px;
  background: #42b983;
  color: white;
  cursor: pointer;
  transition: background 0.3s;
}

.toolbar-button:hover {
  background: #3aa876;
}

.board {
  flex: 1;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  overflow: hidden;
}

.status-column {
  background: white;
  border-radius: 12px;
  padding: 15px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.status-title {
  margin: 0 0 15px 0;
  color: #333;
  text-align: center;
  padding-bottom: 10px;
  border-bottom: 2px solid #eee;
}

.notes-container {
  position: relative;
  min-height: 200px;
}
</style>