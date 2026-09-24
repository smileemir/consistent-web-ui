// Tidewell API (stub). Owned by the backend team: not part of the frontend work.
const express = require("express");
const router = express.Router();

let settings = {
  workspaceName: "Northwind Studio",
  timezone: "Europe/Berlin",
  dataRetentionDays: 365,
  weeklyDigest: true,
  require2fa: false,
};

router.get("/settings", (req, res) => res.json(settings));
router.put("/settings", (req, res) => { settings = { ...settings, ...req.body }; res.json(settings); });
router.post("/api-key/regenerate", (req, res) => res.json({ key: "tw_live_" + Math.random().toString(36).slice(2) }));
router.delete("/workspace", (req, res) => res.status(202).json({ status: "scheduled", cancellableForDays: 7 }));

module.exports = router;
