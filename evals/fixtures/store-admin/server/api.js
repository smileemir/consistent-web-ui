// Kestrel Supply admin API (stub). Backend: not part of the frontend work.
const express = require("express");
const router = express.Router();

let settings = {
  storeName: "Kestrel Supply",
  supportEmail: "help@kestrel-supply.example",
  currency: "EUR",
  guestCheckout: true,
  reserveStock: true,
  reservationWindow: 15,
  autoFulfilDigital: true,
  holdHighRisk: true,
  lowStockThreshold: 5,
  allowBackorders: false,
  smartRanking: true,
};

router.get("/settings", (req, res) => res.json(settings));
router.put("/settings", (req, res) => { settings = { ...settings, ...req.body }; res.json(settings); });
router.post("/settings/reset", (req, res) => {
  const keep = { storeName: settings.storeName, supportEmail: settings.supportEmail, currency: settings.currency };
  settings = { ...keep, guestCheckout: true, reserveStock: true, reservationWindow: 15, autoFulfilDigital: true, holdHighRisk: true, lowStockThreshold: 5, allowBackorders: false, smartRanking: true };
  res.json(settings);
});
router.post("/search/rebuild", (req, res) => res.status(202).json({ status: "started" }));

module.exports = router;
