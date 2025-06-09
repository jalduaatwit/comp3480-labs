const express = require('express');
const app = express();
const PORT = 8080;

app.use(express.json());

const API_KEY = "mysecretkey";

// 1. Root route (HTML)
app.get('/', (req, res) => {
    res.send('<h1>Welcome to Lab 3 Express Service!</h1>');
});

// 2. Query string: /greet?name=Aniket (HTML + Query)
app.get('/greet', (req, res) => {
    const name = req.query.name || 'Guest';
    res.send(`<h2>Hello, ${name}!</h2>`);
});

// 3. Path param: /cube/3 (HTML)
app.get('/cube/:number', (req, res) => {
    const num = parseInt(req.params.number);
    res.send(`<h3>Number: ${num}</h3><p>Cube: ${num ** 3}</p>`);
});

// 4. Query string math: /add?a=5&b=7 (JSON + Query)
app.get('/add', (req, res) => {
    const a = parseInt(req.query.a);
    const b = parseInt(req.query.b);
    res.json({ sum: a + b });
});

// 5. Path param with query: /factorial/5?format=html (HTML + Query)
app.get('/factorial/:n', (req, res) => {
    let n = parseInt(req.params.n);
    let result = 1;
    for (let i = 2; i <= n; i++) result *= i;
    
    const format = req.query.format || 'json';
    if (format === 'html') {
        res.send(`<h3>Factorial of ${n}</h3><p>Result: ${result}</p>`);
    } else {
        res.json({ n: n, factorial: result });
    }
});

// 6. POST with body: /person (JSON + Body)
app.post('/person', (req, res) => {
    const { name, age } = req.body;
    const status = age < 18 ? 'minor' : 'adult';
    res.json({ message: `${name} is ${age} years old and is an ${status}.` });
});

// 7. Path route with query: /city/Boston?details=true (HTML + Query)
app.get('/city/:city_name', (req, res) => {
    const city = req.params.city_name.toLowerCase();
    const details = req.query.details === 'true';
    
    const facts = {
        boston: "Boston is a city that experiences all four seasons.",
        newyork: "New York is a very busy place with lots of tall buildings.",
        seattle: "Seattle gets a fair amount of rain each year.",
        miami: "Miami is known for being warm and having many beaches.",
        dallas: "Dallas is located in Texas and is pretty big."
    };
    const info = facts[city] || "No info for this city.";
    
    if (details) {
        res.send(`<h3>${req.params.city_name}</h3><p><strong>Details:</strong> ${info}</p><p><em>Population data and weather info would go here.</em></p>`);
    } else {
        res.send(`<h3>${req.params.city_name}</h3><p>${info}</p>`);
    }
});

// 8. POST area calc: /area/rectangle (JSON + Body)
app.post('/area/rectangle', (req, res) => {
    const { width, height } = req.body;
    const area = width * height;
    res.json({ width, height, area });
});

// 9. Path + query: /power/2?exp=8 (HTML + Query)
app.get('/power/:base', (req, res) => {
    const base = parseInt(req.params.base);
    const exp = parseInt(req.query.exp) || 2;
    const result = base ** exp;
    res.send(`<h3>Power Calculation</h3><p>${base}<sup>${exp}</sup> = ${result}</p>`);
});

// 10. GET list: /colors (JSON)
app.get('/colors', (req, res) => {
    res.json({ colors: ["red", "blue", "green", "yellow"] });
});

// 11. Header: /protected-data (JSON + Header)
app.get('/protected-data', (req, res) => {
    const key = req.headers['api-key'];
    if (key !== API_KEY) {
        return res.status(401).json({ error: "Invalid or missing API key." });
    }
    res.json({ data: "This is protected data." });
});

app.listen(PORT, () => {
    console.log(`Server running at http://localhost:${PORT}`);
});
