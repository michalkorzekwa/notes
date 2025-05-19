const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true
})
module.exports = {
  devServer: {
    proxy: 'http://localhost:8000'
  }
}
module.exports = {
  devServer: {
    host: 'localhost',
    client: {
      webSocketURL: 'ws://localhost:8080/ws'
    }
  }
}
