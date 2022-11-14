function beautifyJSON(jsonString) {
    return JSON.stringify(JSON.parse(jsonString), null, 2)
}