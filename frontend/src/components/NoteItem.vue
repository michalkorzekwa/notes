<template>
  <div 
    class="note" 
    :style="noteStyle"
    draggable="true"
    @dragstart="handleDragStart"
    @dragend="handleDragEnd"
    @click.stop
  >
    <input 
      v-model="localNote.title" 
      @input="handleInput"
      placeholder="Tytuł"
    >
    <textarea 
      v-model="localNote.content" 
      @input="handleInput"
      placeholder="Treść..."
    ></textarea>
    <select v-model="localNote.color" @change="handleInput">
      <option value="#ffeb3b">Żółty</option>
      <option value="#90caf9">Niebieski</option>
      <option value="#a5d6a7">Zielony</option>
    </select>
    <button @click="handleDelete" class="delete-btn">×</button>
  </div>
</template>

<script>
export default {
  props: ['note'],
  data() {
    return {
      localNote: JSON.parse(JSON.stringify(this.note)),
      dragOffset: { x: 0, y: 0 }
    }
  },
  computed: {
    noteStyle() {
      return {
        backgroundColor: this.localNote.color,
        left: `${this.localNote.position.x}px`,
        top: `${this.localNote.position.y}px`,
        position: 'absolute',
        cursor: 'move'
      }
    }
  },
  watch: {
    note: {
      handler(newVal) {
        this.localNote = JSON.parse(JSON.stringify(newVal))
      },
      deep: true
    }
  },
  methods: {
    handleInput() {
      this.$emit('update', { ...this.localNote })
    },
    handleDragStart(e) {
      this.dragOffset = {
        x: e.clientX - this.localNote.position.x,
        y: e.clientY - this.localNote.position.y
      }
      e.dataTransfer.setDragImage(new Image(), 0, 0)
    },
    handleDragEnd(e) {
      if (e.clientX === 0 && e.clientY === 0) return
      
      const newPosition = {
        x: e.clientX - this.dragOffset.x,
        y: e.clientY - this.dragOffset.y
      }
      
      this.localNote.position = newPosition
      this.$emit('update-position', {
        id: this.localNote.id,
        position: newPosition
      })
    },
    handleDelete() {
      this.$emit('delete', this.localNote.id)
    }
  }
}
</script>

<style scoped>
.note {
  width: 250px;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0,0,0,0.2);
  user-select: none;
}

input, textarea, select {
  width: 100%;
  margin-bottom: 10px;
  padding: 5px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background: rgba(255,255,255,0.8);
}

.delete-btn {
  position: absolute;
  top: 5px;
  right: 5px;
  background: transparent;
  border: none;
  font-size: 1.2rem;
  cursor: pointer;
}
</style>