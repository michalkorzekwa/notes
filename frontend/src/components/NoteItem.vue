<template>
  <div 
    class="note"
    :style="noteStyles"
    @mousedown="startDrag"
    :class="{ 'dragging': isDragging }"
  >
    <div class="note-header">
      <input 
        v-model="localNote.title" 
        class="note-title"
        placeholder="Tytuł"
        @input="handleInput"
      >
      <button @click="deleteNote" class="delete-btn">×</button>
    </div>
    <textarea
      v-model="localNote.content"
      class="note-content"
      placeholder="Treść..."
      @input="handleInput"
    ></textarea>
    <select 
      v-model="localNote.color" 
      class="note-color"
      @change="handleInput"
    >
      <option value="#ffeb3b">Żółty</option>
      <option value="#90caf9">Niebieski</option>
      <option value="#a5d6a7">Zielony</option>
    </select>
  </div>
</template>

<script>
export default {
  props: ['note'],
  data() {
    return {
      localNote: {...this.note},
      isDragging: false,
      startPos: { x: 0, y: 0 },
      currentPos: {...this.note.position},
      hasMoved: false
    }
  },
  computed: {
    noteStyles() {
      return {
        transform: `translate(${this.currentPos.x}px, ${this.currentPos.y}px)`,
        backgroundColor: this.localNote.color,
        zIndex: this.isDragging ? 1000 : 1
      }
    }
  },
  watch: {
    note: {
      handler(newVal) {
        if (!this.hasMoved && (
          this.note.position.x !== this.currentPos.x ||
          this.note.position.y !== this.currentPos.y
        )) {
          this.currentPos = {...newVal.position}
        }
        this.localNote = {...newVal}
      },
      deep: true
    }
  },
  methods: {
    startDrag(e) {
      if (e.target.tagName === 'INPUT' || 
          e.target.tagName === 'TEXTAREA' || 
          e.target.tagName === 'SELECT') return
      
      this.isDragging = true
      this.hasMoved = false
      this.startPos = {
        x: e.clientX - this.currentPos.x,
        y: e.clientY - this.currentPos.y
      }
      
      document.addEventListener('mousemove', this.handleDrag)
      document.addEventListener('mouseup', this.stopDrag)
    },
    handleDrag(e) {
      if (!this.isDragging) return
      
      this.hasMoved = true
      this.currentPos = {
        x: e.clientX - this.startPos.x,
        y: e.clientY - this.startPos.y
      }
    },
    stopDrag() {
      this.isDragging = false
      document.removeEventListener('mousemove', this.handleDrag)
      document.removeEventListener('mouseup', this.stopDrag)
      
      if (this.hasMoved) {
        this.$emit('update-position', {
          id: this.localNote.id,
          position: this.currentPos
        })
      }
    },
    handleInput() {
      this.$emit('update', {...this.localNote})
    },
    deleteNote() {
      this.$emit('delete', this.localNote.id)
    }
  }
}
</script>

<style scoped>
.note {
  position: absolute;
  width: 280px;
  min-height: 200px;
  border-radius: 12px;
  padding: 16px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  cursor: grab;
  transition: transform 0.2s ease-out, box-shadow 0.3s;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.note.dragging {
  cursor: grabbing;
  box-shadow: 0 8px 24px rgba(0,0,0,0.2);
  transition: none;
  z-index: 1000;
}

.note-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  width: 100%;
}

.note-title {
  flex: 1;
  border: none;
  background: rgba(255,255,255,0.9);
  font-size: 16px;
  padding: 8px 12px;
  border-radius: 6px;
  text-align: center;
  margin-right: 8px;
}

.note-content {
  width: 100%;
  height: 120px;
  border: none;
  background: rgba(255,255,255,0.9);
  border-radius: 6px;
  padding: 12px;
  resize: vertical;
  margin: 12px 0;
  text-align: center;
}

.note-color {
  width: 100%;
  padding: 8px;
  border-radius: 6px;
  border: 1px solid rgba(0,0,0,0.1);
  background: white;
  text-align: center;
}

.delete-btn {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  opacity: 0.5;
  padding: 0 5px;
}

.delete-btn:hover {
  opacity: 1;
}
</style>