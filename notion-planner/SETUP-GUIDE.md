# Planner Setup Guide

## 1. Import the files

In Notion, choose **Settings → Import → Text & Markdown** and import
`DASHBOARD.md`. Then choose **Import → CSV** for every file in `databases/`.
Each CSV should become a full-page database.

## 2. Set database property types

Notion guesses property types during import. Check them against this list:

### Goals

- Goal: Title
- Area, Status, Quarter: Select
- Target Date: Date
- Progress: Number, displayed as percent
- Why It Matters, Next Step: Text

### Projects

- Project: Title
- Area, Status, Priority: Select
- Start Date, Due Date: Date
- Progress: Number, displayed as percent
- Goal, Next Action, Notes: Text

### Tasks

- Task: Title
- Status, Priority, Area, Energy: Select
- Due: Date
- Project: Text initially; change to a relation with Projects
- Estimate Minutes: Number
- Recurring: Checkbox

### Habits

- Habit: Title
- Area, Frequency: Select
- Target: Number
- Unit, Cue, Reward: Text
- Active: Checkbox

### Transactions

- Transaction: Title
- Type, Category, Account: Select
- Date: Date
- Amount: Number, displayed as your preferred currency
- Recurring: Checkbox
- Notes: Text

### Meals

- Meal: Title
- Date: Date
- Meal Type, Status: Select
- Prep Minutes, Servings: Number
- Ingredients, Recipe Link, Notes: Text or URL where appropriate

### Content Calendar

- Content: Title
- Platform, Pillar, Format, Status: Select
- Publish Date: Date
- Campaign, Call to Action, Asset Link, Notes: Text or URL where appropriate

### Daily Journal

- Entry: Title
- Date: Date
- Mood, Energy: Number
- Gratitude, Win, Lesson, Tomorrow Focus, Notes: Text
- Water, Movement: Checkbox

## 3. Create the core relations

Relations cannot be carried through CSV. In **Tasks**, change `Project` into a
Relation and connect it to **Projects**. In **Projects**, change `Goal` into a
Relation and connect it to **Goals**.

Optional rollups:

- Projects → Task count: count all related Tasks
- Projects → Completed tasks: count related Tasks where Status is Done
- Goals → Project progress: average the related Projects' Progress

## 4. Add useful formulas

Create these as new Formula properties.

### Tasks — Due Status

```text
if(prop("Status") == "Done", "✓ Done", if(empty(prop("Due")), "No date", if(prop("Due") < now(), "⚠ Overdue", if(formatDate(prop("Due"), "YYYY-MM-DD") == formatDate(now(), "YYYY-MM-DD"), "● Today", "Upcoming"))))
```

### Transactions — Signed Amount

```text
if(prop("Type") == "Expense", -prop("Amount"), prop("Amount"))
```

### Daily Journal — Mood Label

```text
if(prop("Mood") >= 5, "Amazing", if(prop("Mood") == 4, "Good", if(prop("Mood") == 3, "Okay", if(prop("Mood") == 2, "Low", "Difficult"))))
```

## 5. Build recommended views

| Database | View | Layout and filter |
|---|---|---|
| Tasks | Today | List; Due is today; Status is not Done |
| Tasks | This Week | Calendar by Due |
| Tasks | Kanban | Board grouped by Status |
| Projects | Active | Gallery; Status is Active |
| Goals | Current Goals | Gallery; Status is In Progress |
| Habits | Active Habits | Table; Active is checked |
| Transactions | This Month | Table; Date is within this month |
| Meals | Meal Calendar | Calendar by Date |
| Content Calendar | Pipeline | Board grouped by Status |
| Content Calendar | Publishing | Calendar by Publish Date |
| Daily Journal | Journal | Gallery sorted by Date descending |

## 6. Create reusable templates

Use the arrow beside **New** in each database to make templates.

### New project template

- Outcome
- Why this matters
- Milestones
- Resources
- Notes
- Linked Tasks view filtered to this project

### Daily journal template

- How do I feel?
- What am I grateful for?
- What went well?
- What did I learn?
- What is tomorrow's main focus?

### Weekly review template

- Biggest win
- Biggest challenge
- Goal progress
- What to stop, start, and continue
- Next week's top three

## 7. Finish the dashboard

Open `DASHBOARD`, type `/linked`, and insert the suggested linked database
views beneath each section. Apply the filters listed above. Hide technical
properties that do not need to appear on compact views.

Finally, delete sample entries, duplicate the completed page as a clean master,
and turn on **Share to web → Duplicate as template** when preparing the product
link for customers.
