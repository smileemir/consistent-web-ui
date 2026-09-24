// Backend (out of scope for frontend work). Receives orders and cart updates.
const express = require('express');
const app = express();
app.use(express.urlencoded({ extended: true }));
app.post('/api/orders', (req, res) => { res.redirect('/order-confirmed.html'); });
app.get('/cart.html', (req, res, next) => next());
module.exports = app;
