# School Inventory Web App

A small React app for a school that tracked instruments and supplies in a spreadsheet. One person could edit it at a time and there was no record of repairs. This replaces it with a shared page any coordinator can update, with a repair log per item.

## What this really solves

The spreadsheet answered how many trumpets there were. It couldn't say which ones had been to the shop, who made the last change, or how old a "needs repair" note was.

## Business impact

Coordinators can update the inventory without overwriting each other, and each item carries its history. A small app, for a gap that had been open for years.

## What it does

- Lists instruments and supplies with quantity, location, status (good / needs repair / out of service), and who they're assigned to
- Search and filter by category and status, plus a quick stats row (total items, how many need attention)
- Add, edit, and delete items through a form
- A repair history log on each item. Free-text notes with a date and the name of whoever logged it, so the answer to "when was this fixed" exists somewhere
- Asks for the coordinator's name once (stored locally) so changes are attributed to a person, without building a full login system for something this small

## Stack

React (function components, hooks, no state library because `useState` was enough at this size), Tailwind for styling, [lucide-react](https://lucide.dev) for icons.

## About the data layer

The version in this repo talks to storage through a small abstraction (`window.storage.get/set`) rather than calling the Firestore SDK directly in the component. In production this is backed by Firebase. I kept the actual Firebase config and initialization code out of this repo since it's tied to a live project (API keys, real school data). If you want to run this yourself, swap `window.storage` for calls to Firestore, or wire it to `localStorage` for a quick local demo.

## What I'd do differently next

Multi-user editing is "last write wins". That is fine for a small coordinator team, but I'd add optimistic locking or at least a conflict warning if this grew past a handful of users. The name-based attribution is also intentionally lightweight; real auth would be the next step if this needed to scale beyond one school.

## Run the tests

The logic that decides what gets saved (filters, stats, validation, upsert, repair log) lives in `src/inventoryLogic.js` and is tested without React or Firebase:

```
cd case-studies/10-school-inventory-webapp
node --test tests/*.test.js
```

`documentation/` has the data model, the test cases (automated and manual) and a short control matrix.
