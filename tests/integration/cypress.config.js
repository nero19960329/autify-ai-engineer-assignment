const { defineConfig } = require("cypress");

module.exports = defineConfig({
  e2e: {
    baseUrl: "http://localhost:8000",
    specPattern: "**/*.spec.js",
    supportFile: false,
    video: true,
  },
});
