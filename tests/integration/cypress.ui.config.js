const { defineConfig } = require("cypress");

module.exports = defineConfig({
  e2e: {
    baseUrl: "http://localhost:8001",
    specPattern: "ui/*.spec.js",
    supportFile: false,
    video: true,
  },
});
