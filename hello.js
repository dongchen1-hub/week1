const readline = require("node:readline");

const terminal = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

terminal.question("Enter a word: ", (word) => {
    const letters = Array.from(word);
    console.log(letters.reverse().join(""));
    terminal.close();
});
