# life-schema.md

This document defines the required structure of the `life.json` data used in the Life Management System.

## Top-Level Structure

```json
{
  "areas_of_responsibility": [...]
}
```

Only the `areas_of_responsibility` field is allowed at the top level.

---

## `areas_of_responsibility`

An array of objects. Each object represents an Area of Responsibility (AoR).

### Each AoR object:

```json
{
  "name": "String",
  "projects": [...]
}
```

- `name`: (string) Name of the AoR (e.g., "Wellbeing", "Customer Interactions").
- `projects`: (array) List of associated projects.

---

## Projects

Each AoR can contain multiple projects.

### Each project object:

```json
{
  "title": "String",
  "notes": "String (optional)",
  "tasks": [...]
}
```

- `title`: (string) Title of the project.
- `notes`: (optional string) Additional context or background info.
- `tasks`: (array) List of associated tasks.

---

## Tasks

Each project can contain multiple tasks.

### Each task object:

```json
{
  "description": "String",
  "due": "YYYY-MM-DD (optional)",
  "start": "YYYY-MM-DD (optional)",
  "done": "Boolean (optional)",
  "customer_id": "String (optional)"
}
```

- `description`: (string) Description of the task.
- `due`: (optional string) Date the task is due.
- `start`: (optional string) Start date.
- `done`: (optional boolean) If the task is completed.
- `customer_id`: (optional string) Links to a CRM customer (if applicable).

---

## Notes

- All fields are case-sensitive.
- Unknown fields at any level will be rejected.
- Dates must be in `YYYY-MM-DD` format.