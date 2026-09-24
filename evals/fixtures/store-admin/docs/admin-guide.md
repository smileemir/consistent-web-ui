# Admin guide (internal)

Notes for staff. Ask the owner before changing any setting you are unsure about.

## Products list

- **Stock**: units on the shelf, from the last warehouse sync.
- **Reserved**: units held for customers who are in checkout. A hold lasts for the reservation window (Settings, Checkout; default 15 minutes) and is released if the customer does not pay in time.
- **Available**: Stock minus Reserved. This is the number customers can still buy.
- **Sell-through (30 days)**: units sold in the last 30 days divided by (units sold in the last 30 days + current stock). Below 20% means the product is moving slowly; consider a promotion or a smaller reorder.
- **Low stock**: a product whose Available is at or below the low-stock threshold (Settings, Inventory; default 5). Only staff see this flag.
- **Statuses**:
  - Active: on sale.
  - Draft: never published; only staff can see it.
  - Paused: hidden from the shop and from search, but its link still works and shows "Currently unavailable".
  - Archived: hidden everywhere and left out of the default admin list; find it with the Archived filter and restore it from there.

## Settings

### Store

- **Currency**: the currency customers see. Changing it does not convert prices; update the prices yourself after a change.

### Checkout

- **Guest checkout**: customers can buy without an account. They still get an email receipt and can create an account from it later.
- **Reserve stock at checkout**: when on, starting checkout holds the units for the reservation window (see Reserved). When off, stock is only taken at payment, so two customers can pay for the last unit; the second order then has to be refunded.
- **Reservation window**: how many minutes a hold lasts, from 5 to 60.

### Orders

- **Auto-fulfil digital orders**: when on, digital plans are emailed as soon as the payment is captured. When off, paid digital orders wait in Orders, To fulfil, until someone sends them.
- **Hold high-risk orders**: when on, orders with a risk score of 70 or more wait in Orders, Review, and are not fulfilled until someone approves them. The customer sees "Payment under review". When off, they are fulfilled like any other order.

### Inventory

- **Low-stock threshold**: see Low stock. It does not change what customers see.
- **Allow backorders**: when on, customers can buy products with 0 available; the product page says "Back in stock soon, ships when it arrives". When off, the buy button is replaced with "Sold out".

### Search and maintenance

- **Rebuild search index**: re-reads every product so search matches recent edits. It takes up to 10 minutes; the shop stays online and search keeps using the old index until the new one is ready.
- **Reset to defaults**: sets every setting on the Settings page back to its default. Store name, support email and currency are kept. It cannot be undone.
