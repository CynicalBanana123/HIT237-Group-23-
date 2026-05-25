# ADR () - Updated Supplementary Diagrams

## 25/05/2026 Revision:

### Status:
Approved

### Context
From Assessment 2, the supplementary materials only included a bare bones simple ERD, containing a User and Ticket entity. This diagram did not fully reflect the current projects codebase. 
The diagram did not document the object oriented architecture that was introduced in Assessment 4, with class based views, mixins and the overall service layer.

To improve this technical dcoumentation and better represent the implemented architecture, the supplementary materials were updated.
### Alternative Solutions Considered

1. Keep Existing Diagrams Unchanged
  - Pros
    - No additional documentation work required
    - Existing ERD already represented basic entities
  - Cons
    - Did not reflect the current projects work
    - Missing authentication relationships, such as the Profile
    - No class diagram documenting any form of OO structure
    - No documentation of service layer architecture

2. Update ERD and Add Class Diagram (Chosen Solution)
  - Pros
    - Reflects current Django models and relationships
    - Documents service layer architecture
    - Documents class based views, mixins, etc
    - Improves maintainability and understanding for developers
  - Cons
    - Additional time required to maintain documentation, constantly needing updates

### Solution Decided Upon:
The ERD was updated to include the Profile entity and current authentication
relationships using Crow's Foot notation.

A new class diagram was also added. This was done to properly document the applications object oriented structure. 
This ranged from models, views, mixins and service layer interactions.

### Consequences:
The supplementary materials should now better represent the overall project and implemented Django architecture. 
The goal is to provide clearer technical documentation for future development and progression throughout the project.

However, maintaining accurate information displayed from these diagrams will require additional updates whenever any architecture is changed.

### Code Reference:

```python
# supplementary/
ERDUpdated.png
ClassDiagram.png
