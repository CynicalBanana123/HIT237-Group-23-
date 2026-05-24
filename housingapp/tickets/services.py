"""Business logic services for ticket workflows.

Services in this module encapsulate creation, deletion, and status
transitions for tickets, and centralise permission checks so views
remain thin controllers.
"""

from django.db import transaction

from .models import Ticket


class TicketPermissionError(Exception):
    """Raised when a user attempts an action they are not permitted to perform."""


class TicketStatusError(Exception):
    """Raised when attempting to set an invalid ticket status or illegal transition."""


def _get_role(user):
    """Return the role string for a user (e.g. 'owner' or 'tenant')."""
    return getattr(user, 'profile', None) and user.profile.role


def user_can_view_ticket(user, ticket):
    """Return True when the given `user` may view `ticket`.

    Owners can view any ticket; tenant users can only view tickets they created.
    """
    role = _get_role(user)
    return role == 'owner' or ticket.created_by == user


def user_can_modify_ticket(user, ticket):
    """Return True when the given `user` may modify or delete `ticket`.

    Owners and creators are allowed to modify tickets.
    """
    role = _get_role(user)
    return role == 'owner' or ticket.created_by == user


@transaction.atomic
def create_ticket(user, form):
    """Create and persist a Ticket from a validated `form` and set its owner.

    The function runs inside a transaction to allow future expansion where
    related objects must be created atomically alongside the ticket.
    """
    ticket = form.save(commit=False)
    ticket.created_by = user
    ticket.save()
    return ticket


def delete_ticket(user, ticket):
    """Delete `ticket` if `user` has permission, else raise TicketPermissionError."""
    if not user_can_modify_ticket(user, ticket):
        raise TicketPermissionError("You do not have permission to delete this ticket.")
    ticket.delete()


@transaction.atomic
def update_ticket_status(user, ticket, new_status):
    """Change `ticket.status` to `new_status` enforcing business rules.

    Only owners are allowed to change status in the current app design. The
    function validates the new status and raises `TicketStatusError` for
    invalid values.
    """
    role = _get_role(user)
    if role != 'owner':
        raise TicketPermissionError('Only owners may change ticket status.')
    if new_status not in (Ticket.STATUS_OPEN, Ticket.STATUS_CLOSED):
        raise TicketStatusError('Invalid status value.')
    ticket.status = new_status
    ticket.save()
    return ticket
