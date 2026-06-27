# Spec Driven Development Guide

A simple guide for building a web app using **Cursor Agentic Coding**, a lightweight `AGENTS.md` file, and **ngrok** for local demo deployment.

---

## 1. Useful Links

### Cursor Desktop
Download Cursor Desktop here:

https://cursor.com/download

Cursor Desktop is available for macOS, Windows, and Linux.

### ngrok
ngrok website:

https://ngrok.com/
---

Retrieve Your Auth Token:

https://dashboard.ngrok.com/get-started/your-authtoken


---

## 2. What You Are Trying To Do

You want to build a simple web app without over-engineering the process.

The goal is to use **spec-driven development**:

1. Write the app idea first.
2. Convert the idea into simple specs.
3. Ask Cursor to implement one small task at a time.
4. Keep track of changes.
5. Run the app locally.
6. Expose the app using ngrok for demo/testing.

The key principle:

> Do not ask Cursor to build everything at once. Ask Cursor to read the specs and implement one small task at a time.

---

## 3. Recommended Simple Project Structure

For a simple app, this structure is enough:

```txt
my-simple-app/
├── README.md
├── AGENTS.md
├── specs/
│   ├── product-spec.md
│   ├── implementation-plan.md
│   ├── test-plan.md
│   └── change-log.md
├── frontend/
└── backend/
```

For an even simpler single-app project:

```txt
my-simple-app/
├── README.md
├── AGENTS.md
├── specs/
│   ├── product-spec.md
│   ├── implementation-plan.md
│   └── change-log.md
└── src/
```

---

## 4. Role of Each File

| File | Purpose |
|---|---|
| `README.md` | Explains how to install, run, and demo the app |
| `AGENTS.md` | Tells Cursor Agent how to behave while coding |
| `specs/product-spec.md` | Defines the app goal, users, features, and acceptance criteria |
| `specs/implementation-plan.md` | Breaks the app into small implementation tasks |
| `specs/test-plan.md` | Defines how to test the app |
| `specs/change-log.md` | Records what changed after each Cursor implementation |

---

## 5. Step-by-Step Workflow Summary

| Step | What You Do | Prompt to Input to Cursor | Expected Outcome |
|---|---|---|---|
| 1 | Create the project idea | Ask Cursor to turn your app idea into specs, without coding yet | Cursor creates initial spec files |
| 2 | Review the spec | Ask Cursor to check if the spec is clear, simple, and MVP-focused | Cursor improves the product spec |
| 3 | Create `AGENTS.md` | Ask Cursor to create simple instructions for the coding agent | Cursor creates coding behavior rules |
| 4 | Initialize the app | Ask Cursor to implement only project setup | App structure is created |
| 5 | Build first feature | Ask Cursor to implement only the first unchecked task | First feature is implemented |
| 6 | Test feature | Ask Cursor to test against acceptance criteria | Bugs are found and fixed |
| 7 | Repeat | Ask Cursor to continue with the next unchecked task | App grows step by step |
| 8 | Add local run guide | Ask Cursor to update `README.md` with local commands | README becomes usable |
| 9 | Add ngrok guide | Ask Cursor to add ngrok demo instructions | App can be exposed for demo |
| 10 | Final review | Ask Cursor to review the app against the spec | Final MVP status report is created |

---

# 6. Detailed Instructions and Cursor Prompts

## Step 1: Create the Specs

### What You Do
Open Cursor and describe your app idea.

### Prompt to Cursor

```txt
I want to build a simple web app using spec-driven development.

App idea:
[Describe the app here]

Before writing any code, create these files:
- README.md
- AGENTS.md
- specs/product-spec.md
- specs/implementation-plan.md
- specs/test-plan.md
- specs/change-log.md

Keep everything simple and MVP-focused.
Do not implement the app yet.
```

### Expected Outcome
Cursor creates the basic documentation and spec structure.

---

## Step 2: Improve the Product Spec

### What You Do
Ask Cursor to make the spec clearer before coding.

### Prompt to Cursor

```txt
Review specs/product-spec.md.

Improve it so it clearly includes:
- app goal
- target users
- core user flow
- features in scope
- features out of scope
- acceptance criteria

Keep it simple.
Do not write code yet.
```

### Expected Outcome
You get a clean MVP product spec.

---

## Step 3: Improve the Implementation Plan

### What You Do
Break the app into small buildable tasks.

### Prompt to Cursor

```txt
Review specs/implementation-plan.md.

Rewrite it into small phases:
1. Project setup
2. Core UI
3. Core backend or data logic
4. Connect UI to data
5. Validation and error states
6. Local run instructions
7. ngrok demo setup

Each phase should have clear checklist items.
Do not write code yet.
```

### Expected Outcome
Cursor creates a checklist that can be implemented one task at a time.

---

## Step 4: Create Simple AGENTS.md

### What You Do
Tell Cursor how to behave while coding.

### Prompt to Cursor

```txt
Create or update AGENTS.md.

The agent should follow these rules:
- Always read the specs before coding.
- Implement only one phase or task at a time.
- Keep the app simple.
- Do not add unnecessary libraries.
- Do not change architecture unless the spec is updated.
- After each implementation, update specs/change-log.md.
- After each implementation, explain how to test the change.

Keep AGENTS.md short and practical.
```

### Expected Outcome
Cursor has enough instructions to behave consistently without `.cursor/rules`.

---

## Step 5: Implement Project Setup

### What You Do
Start coding, but only the initial structure.

### Prompt to Cursor

```txt
Read AGENTS.md and all files in specs/.

Implement only Phase 1 from specs/implementation-plan.md: project setup.

Do not implement any business features yet.

After implementation:
- explain what files were created or changed
- provide commands to run the app
- update specs/change-log.md
```

### Expected Outcome
Cursor initializes your app, for example with React, Next.js, FastAPI, Express, or another stack you specified.

---

## Step 6: Implement the First Feature

### What You Do
Build only the first real feature.

### Prompt to Cursor

```txt
Read AGENTS.md and specs/.

Implement only the first unchecked feature in specs/implementation-plan.md.

Before coding, summarize:
- what you will build
- which files you will edit
- how you will test it

After coding:
- update specs/change-log.md
- tell me the exact test steps
```

### Expected Outcome
Cursor builds one feature without accidentally building the whole app.

---

## Step 7: Test Against Acceptance Criteria

### What You Do
Ask Cursor to verify the feature.

### Prompt to Cursor

```txt
Review the feature you just implemented against the acceptance criteria in specs/product-spec.md and specs/test-plan.md.

Check:
- what passes
- what fails
- what is missing

Fix only issues related to this feature.
Do not add new features.
Update specs/change-log.md after fixing.
```

### Expected Outcome
Cursor tests and fixes the current feature only.

---

## Step 8: Repeat for the Next Feature

### What You Do
Continue one task at a time.

### Prompt to Cursor

```txt
Continue with the next unchecked item in specs/implementation-plan.md.

Implement only that item.
Do not modify unrelated files unless necessary.

After implementation:
- mark the task as completed
- update specs/change-log.md
- provide manual test steps
```

### Expected Outcome
Your app grows feature-by-feature in a controlled way.

---

## Step 9: Add Local Run Instructions

### What You Do
Make sure the app can run on your machine.

### Prompt to Cursor

```txt
Update README.md with clear local development instructions.

Include:
- prerequisites
- install commands
- environment variables
- frontend run command
- backend run command if applicable
- local URLs
- troubleshooting notes

Do not change app logic.
```

### Expected Outcome
Anyone can run the app locally from the README.

---

## Step 10: Prepare ngrok Demo

### What You Do
Expose your local app to the internet for demo/testing.

### Prompt to Cursor

```txt
Update README.md with a section called "Demo with ngrok".

Explain how to:
- start the frontend locally
- start the backend locally if applicable
- expose the frontend using ngrok
- expose the backend using ngrok if needed
- configure frontend API base URL to use the ngrok backend URL

Use the actual ports used in this project.
Do not change app logic.
```

### Expected Outcome
README contains ngrok demo commands.

Example frontend command:

```bash
npm run dev
ngrok http 5173
```

Example backend command:

```bash
uvicorn main:app --reload --port 8000
ngrok http 8000
```

---

## Step 11: Final Review Before Demo

### What You Do
Ask Cursor to check whether the MVP is ready.

### Prompt to Cursor

```txt
Review the entire app against specs/product-spec.md and specs/implementation-plan.md.

Create a final MVP status report with:
- completed features
- missing features
- known bugs
- how to run locally
- how to demo with ngrok
- recommended next improvements

Do not write code unless there is a critical bug.
```

### Expected Outcome
You get a clear final checklist before showing the app.

---

# 7. Example AGENTS.md

Use this as your default `AGENTS.md` for simple apps:

```md
# AGENTS.md

This project follows simple spec-driven development.

## Main Rule
Always read the files in `/specs` before coding.

## Workflow
For every task:
1. Read the relevant spec files.
2. Implement only one task or phase at a time.
3. Keep the solution simple.
4. Avoid unnecessary libraries.
5. Do not change the architecture unless the spec is updated.
6. After implementation, update `specs/change-log.md`.
7. Explain how to test the change.

## Coding Style
- Prefer simple, readable code.
- Do not over-engineer.
- Do not add unrelated features.
- Keep changes small and reviewable.

## Testing
Before saying the task is complete, provide:
- commands to run the app
- manual test steps
- any known issues
```

---

# 8. Example Product Spec Template

Create this as `specs/product-spec.md`:

```md
# Product Spec

## App Name
[App name]

## Goal
[What problem does this app solve?]

## Target Users
- [User type 1]
- [User type 2]

## Core User Flow
1. User opens the app.
2. User performs the main action.
3. App shows the result.
4. User can continue or reset.

## Features In Scope
- [Feature 1]
- [Feature 2]
- [Feature 3]

## Features Out of Scope
- Authentication
- Payments
- Admin dashboard
- Production cloud deployment

## Acceptance Criteria
- User can run the app locally.
- User can complete the main flow.
- User sees clear success/error states.
- App can be demoed with ngrok.
```

---

# 9. Example Implementation Plan Template

Create this as `specs/implementation-plan.md`:

```md
# Implementation Plan

## Phase 1: Project Setup
- [ ] Initialize project structure
- [ ] Install required dependencies
- [ ] Add basic README
- [ ] Confirm app runs locally

## Phase 2: Core UI
- [ ] Create main page
- [ ] Add input form
- [ ] Add result/display section
- [ ] Add basic styling

## Phase 3: Core Logic
- [ ] Implement main app logic
- [ ] Add validation
- [ ] Add error handling

## Phase 4: Connect UI to Logic
- [ ] Connect form to logic
- [ ] Show loading state if needed
- [ ] Show success/error result

## Phase 5: Testing
- [ ] Test happy path
- [ ] Test empty input
- [ ] Test invalid input
- [ ] Test refresh/reload behavior

## Phase 6: Local Run Guide
- [ ] Update README with install command
- [ ] Update README with run command
- [ ] Add local URL

## Phase 7: ngrok Demo
- [ ] Add ngrok setup instructions
- [ ] Add frontend tunnel command
- [ ] Add backend tunnel command if needed
- [ ] Add demo checklist
```

---

# 10. Example Change Log Template

Create this as `specs/change-log.md`:

```md
# Change Log

## YYYY-MM-DD

### Added
- 

### Changed
- 

### Fixed
- 

### Notes
- 
```

---

# 11. ngrok Demo Commands

## Frontend Only

If your app only has a frontend:

```bash
npm run dev
ngrok http 5173
```

Open the HTTPS forwarding URL from ngrok.

## Frontend + Backend

Terminal 1: start backend

```bash
cd backend
uvicorn main:app --reload --port 8000
```

Terminal 2: expose backend

```bash
ngrok http 8000
```

Terminal 3: configure frontend environment

```env
VITE_API_BASE_URL=https://your-backend-ngrok-url.ngrok-free.app
```

Terminal 4: start frontend

```bash
cd frontend
npm run dev
```

Terminal 5: expose frontend

```bash
ngrok http 5173
```

Share the frontend ngrok HTTPS URL.

---

# 12. The Three Most Important Cursor Prompts

## Start Next Task

```txt
Read AGENTS.md and specs/.

Implement only the next unchecked task in specs/implementation-plan.md.
Keep the change small.
Update specs/change-log.md after implementation.
```

## Fix a Bug

```txt
This feature has a bug:

[Describe bug]

Read the relevant spec first.
Find the root cause.
Fix only this bug.
Do not add unrelated features.
Update specs/change-log.md.
```

## Prepare Demo

```txt
Prepare this project for a local ngrok demo.

Update README.md with exact commands to run the app locally and expose it with ngrok.
Use the actual project ports.
Do not change app logic.
```

---

# 13. Final Mental Model

You are the product owner.

Cursor is the junior developer.

The specs are the contract.

The change log is the memory.

ngrok is the demo tunnel, not production deployment.

