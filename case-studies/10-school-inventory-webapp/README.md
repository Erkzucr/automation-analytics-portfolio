# School Inventory Web App

A small React app I built to solve a real, unglamorous problem: a school kept track of its musical instruments and supplies in a spreadsheet that only one person could edit at a time, with no history of what got repaired or when. This replaces that with a shared web app that any coordinator can update, with a running repair/maintenance log per item.

## What this really solves

A school was tracking instruments and supplies in a spreadsheet only one person could edit at a time, with no record of what had ever actually been repaired.

## Business impact

Now anyone on the team can update it safely, and there's a real history behind every item — the difference between "we think we still have that" and knowing for sure.

## What it does

- Lists instruments and supplies with quantity, location, status (good / needs repair / out of service), and who they're assigned to
- Search and filter by category and status, plus a quick stats row (total items, how many need attention)
- Add, edit, and delete items through a form
- A repair history log on each item — free-text notes with a date and who logged it, so there's an actual record instead of "someone fixed it at some point"
- Asks for the coordinator's name once (stored locally) so changes are attributed to a person, without building a full login system for something this small

## Stack

React (function components, hooks — no external state library, `useState` was enough at this size), Tailwind for styling, [lucide-react](https://lucide.dev) for icons.

## About the data layer

The version in this repo talks to storage through a small abstraction (`window.storage.get/set`) rather than calling the Firestore SDK directly in the component. In production this is backed by Firebase — I kept the actual Firebase config and initialization code out of this repo since it's tied to a live project (API keys, real school data). If you want to run this yourself, swap `window.storage` for calls to Firestore, or wire it to `localStorage` for a quick local demo.

## What I'd do differently next

Multi-user editing is currently "last write wins" — fine for a small coordinator team, but I'd add optimistic locking or at least a conflict warning if this grew past a handful of users. The name-based attribution is also intentionally lightweight; real auth would be the next step if this needed to scale beyond one school.
