# Assessment 4 — Goals, Business Rules & Models

---

## 1. Clarified Goal Statement

> A ticket management system allowing verified tenants in NT remote communities to log housing repair requests against one or more of their registered dwellings. Administrators can view, prioritise, and update ticket status across all tenants, organised by location. Third-party contractors are contacted outside the application to address tenant requests. This system exists solely to track and manage repair requests so issues are easier to address for the NT government.

---

## 2. Business Rules

These are the rules the application must enforce. Each one should eventually map to either an ADR entry or a direct code enforcement.

### Authentication & Identity

1. All tenant-facing pages require login. Unauthenticated users are redirected to the login page.
2. MyGov integration is the ideal, but for this MVP Django's built-in authentication with `LoginRequiredMixin` is used. The ADR must document this as a deliberate pragmatic choice.
3. Each authenticated user has one `TenantProfile` (linked one-to-one with their account) that stores contact information only (phone number). A tenant may have **one or more registered `Dwelling` records**, each representing a distinct property they occupy.
4. Dwellings are registered and managed by an administrator — tenants cannot add, modify, or remove their own dwelling records. This is the primary mechanism preventing misattribution of tickets to incorrect properties.
5. A tenant may have one dwelling marked as their **primary** residence. This is pre-selected by default when submitting a ticket.

### Ticket Creation

6. When submitting a ticket, a tenant selects which of their registered dwellings the request relates to. If they have only one dwelling it is pre-selected. The address is never a free-text field on the ticket form.
7. A tenant cannot have more than **3 active tickets per dwelling** at the same time. This is the primary anti-spam mechanism. Active means any status except Resolved or Cancelled. A tenant with multiple dwellings receives this limit independently for each — it is not a global cap per person.
8. Each ticket requires a **title** and **description**. Attaching a **photo** is optional.
9. Staff and administrator accounts cannot submit tickets. They manage tickets; they do not create them.

### Ticket Visibility

10. Tenants can only see their own tickets. There is no public ticket list.
11. Attempting to view another tenant's ticket by guessing a URL must be blocked and return a 403 Forbidden response.
12. Staff can see all tickets across all tenants and all dwellings.

### Ticket Status

13. Valid statuses, in order of progression:
    - **Submitted** — ticket has been lodged, no action taken yet.
    - **Under Review** — staff have acknowledged and are assessing the request.
    - **Being Resolved** — a contractor or resolution action is in progress.
    - **Resolved** — the issue has been addressed.
    - **Cancelled** — the request has been voided (by the tenant or an admin).

14. Only administrators/staff can move a ticket between statuses — **except** that a tenant may cancel their own ticket while it is still in the *Submitted* state.

15. Every status change automatically records the time it was last updated.

### Admin View

16. The admin list is organised by **Dwelling**, sorted first by postal code, then by address alphabetically within each postal code. A tenant with dwellings in multiple postal codes appears in each relevant grouping.
17. Each dwelling entry in the admin list shows a visual indicator if it has active tickets (tickets that are not Resolved or Cancelled). Visual indicators will then vary for tickets that are yet to be reviewed and those that are being resolved.
18. Clicking a dwelling in the admin list shows all tickets submitted for that dwelling.

---

## 3. Required Models (This content has been made redundant and can be ignored)

Three models are needed. Everything below is the agreed data structure.

### `TenantProfile`
Extends a standard user account with contact information only. Location data has been moved to `Dwelling`.

| Field | Type | Notes |
|---|---|---|
| `user` | OneToOneField → User | Auto-linked; deleted if user is deleted |
| `phone` | CharField(20) | Optional contact number |

### `Dwelling`
Represents a single property registered to a tenant. A tenant may have more than one.

| Field | Type | Notes |
|---|---|---|
| `tenant` | ForeignKey → User | SET_NULL if user is deleted; `related_name='dwellings'` |
| `address` | CharField(200) | Street address of the property |
| `postal_code` | CharField(10) | Used for admin sorting |
| `community` | CharField(100) | e.g. "Yuendumu", "Tennant Creek" |
| `is_primary` | BooleanField | Marks the tenant's main residence; pre-selected on ticket forms |

### `Ticket`
The core repair request, linked to a specific dwelling rather than to a user directly.

| Field | Type | Notes |
|---|---|---|
| `title` | CharField(200) | Short summary of the issue |
| `description` | TextField | Full description |
| `photo` | ImageField | Optional — attached evidence |
| `dwelling` | ForeignKey → Dwelling | SET_NULL if dwelling is removed; preserves history |
| `created_by` | ForeignKey → User | SET_NULL if user is deleted; kept for audit trail |
| `created_at` | DateTimeField | Set automatically on creation |
| `updated_at` | DateTimeField | Updated automatically on every save |
| `status` | CharField (choices) | See status list above; default: Submitted |
| `priority` | CharField (choices) | Low / Medium / High; default: Low |

**Key design decisions:**

- Address and postal code are never stored on the ticket itself. They live on `Dwelling`. If an address record is corrected, the correction propagates to all associated tickets without any data migration.
- The ticket links to `Dwelling`, not directly to `TenantProfile`. This is what makes the per-dwelling spam limit (rule 7) possible — the service checks active ticket counts scoped to a specific dwelling, not to the tenant as a whole.
- `created_by` is kept on `Ticket` as a separate field from `dwelling.tenant`. If a dwelling is reassigned to a different tenant, the original submitter is still on record.

---

## 4. Architecture for Assessment 4

Assessment 4 explicitly requires three structural additions: a service layer, class-based views, and a test suite. Below is what each means in practice.

### 4.1 Service Layer (`services.py`)

Business logic must live in a dedicated `services.py` file, not inside views. Views should only handle HTTP — receiving requests and returning responses. All rules about *what is allowed* belong in services.

```
TicketService
  ├── create_ticket(user, dwelling, validated_data)  — checks per-dwelling active ticket limit, then creates
  ├── cancel_ticket(ticket, user)                    — validates ownership and Submitted status
  └── update_status(ticket, new_status, staff_user)  — validates staff permission, saves

AdminService
  └── get_dwellings_by_location()          — returns Dwelling queryset sorted by postal_code, then
                                             tenant last name; annotated with active ticket count
```

**Why this matters for the assessment:** The marker is specifically looking for separation of business logic from views. A view that contains an `if active_tickets >= 3` check fails this. A view that calls `TicketService.create_ticket()` and handles a `TicketLimitError` passes it.

### 4.2 Class-Based Views

All views need to be converted to class-based views using Django's built-in generic views and mixins. This is both a Django philosophy requirement and explicitly called out in the brief.

| Page | View Class | Mixins Applied |
|---|---|---|
| Tenant dashboard (own tickets) | `ListView` | `LoginRequiredMixin` |
| Create ticket | `CreateView` | `LoginRequiredMixin` |
| Ticket detail | `DetailView` | `LoginRequiredMixin` |
| Admin tenant list | `ListView` | `LoginRequiredMixin`, `UserPassesTestMixin` |
| Admin update ticket status | `UpdateView` | `LoginRequiredMixin`, `UserPassesTestMixin` |

`UserPassesTestMixin` on admin views checks `request.user.is_staff` — any non-staff user hitting an admin URL gets a 403.

### 4.3 Exception Handling

- Use `get_object_or_404` everywhere instead of bare `.get()` — prevents unhandled `DoesNotExist` crashes.
- Raise `PermissionDenied` when a tenant attempts to access another tenant's ticket.
- Define a custom `ServiceError` exception class in `services.py` for business rule violations (e.g. ticket limit exceeded). Views catch this and display a user-friendly message.
- Add a custom 403 and 404 template so error pages match the site's look.

### 4.4 Test Suite

The assessment brief is explicit: *"AI-generated test suites that merely assert trivial conditions or mirror implementation details without testing meaningful behaviour will not earn credit."*

Tests must verify what users **can** and **cannot** do. The priority is permission boundary testing.

**Model tests**
- A `TenantProfile` is created automatically when a `User` is created.
- `Ticket.__str__` returns the title.
- Default ticket status is `Submitted`.
- `priority` defaults to `Low`.
- A `Dwelling` with `is_primary=True` can be retrieved via `user.dwellings.filter(is_primary=True)`.

**Service tests**
- Creating a 4th ticket on a single dwelling when 3 are already active raises `TicketLimitError`.
- A tenant with 3 active tickets on Dwelling A can still create a ticket for Dwelling B — the limit is per dwelling, not per person.
- A tenant cannot cancel a ticket that is `Under Review` or later.
- A non-staff user calling `update_status` raises `PermissionDenied`.
- A resolved ticket does not count toward the active ticket limit for that dwelling.

**View / permission boundary tests**
- An unauthenticated GET to the tenant dashboard redirects to login (HTTP 302).
- A tenant cannot GET another tenant's ticket detail — returns 403.
- A non-staff user cannot access the admin dwelling list — returns 403.
- A staff user can access the admin dwelling list — returns 200.
- A tenant can cancel their own `Submitted` ticket.
- A tenant cannot change a ticket to `Under Review` (only staff can).
- A tenant cannot submit a ticket against a dwelling that is not registered to them.

---

## 5. ADR Folder and Template

Each significant design decision must have its own Architectural Decision Record. ADRs should be stored in a dedicated `ADR(s)/` folder within the repository. A blank template matching the required structure is already present in that folder — all new and updated entries must follow it exactly.

### ADR Guide

This is the template that should be followed when producting an ADR:

# Content Title

## --/--/2026 Revision:

### Status:
Denied/Approved/Superceded

### Context
...

### Alternative Solutions Considered
1. ...
  - Pros
    - ...
  - Cons
    - ...
2.	...
  - Pros
    - ...
  - Cons
    - ...

### Solution Decided Upon:
...

### Consequences:
...

### Code Reference:
...

When an ADR is relavent to an in-use configuration, it should be marked as 'Approved'. When content is changed that an ADR has linked to, the origional ADR is to be marked as 'Superceded' and a new ADR is to be written using the same template. 

All ADR files must be kept in their own folder, seperate to the code. Titled in a way relevant to the content it describes and with proper reference to the section of code it is related to.

---
