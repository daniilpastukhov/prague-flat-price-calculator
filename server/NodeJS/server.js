const express = require('express')
const app = express()
const PORT = 8888

app.get('/', (request, response) => {
    console.log("+")
})

app.listen(PORT, 'localhost', () => {
    console.log("Server is running on port " + PORT)
})