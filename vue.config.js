const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  lintOnSave: false,
  pages: {
    'login': {
      // 入口文件，相当于单页面的 main.js
      entry: 'src/pages/login.js',
      // 模板文件
      template: 'src/pages/login.html',
      // 编译后 dist 目录下输出的文件，可以包含子目录
      filename: 'index.html'
    },
    'forgetpws': {
      // 入口文件，相当于单页面的 main.js
      entry: 'src/pages/forgetpws.js',
      // 模板文件
      template: 'src/pages/forgetpws.html',
      // 编译后 dist 目录下输出的文件，可以包含子目录
      filename: 'forget-password/index.html'
    },
    'changepassword': {
      // 入口文件，相当于单页面的 main.js
      entry: 'src/pages/changepassword.js',
      // 模板文件
      template: 'src/pages/changepassword.html',
      // 编译后 dist 目录下输出的文件，可以包含子目录
      filename: 'change-password/index.html'
    },
  }
})
