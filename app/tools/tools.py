# app/tools/tools.py

def lock_account(user_id):
    return f"Account {user_id} locked due to suspicious activity."

def unlock_account(user_id):
    return f"Account {user_id} has been unlocked."

def reset_password(user_id):
    return f"Password reset link sent to user {user_id}."

def verify_identity(user_id):
    return f"Identity verification process started for {user_id}."

def process_refund(order_id):
    return f"Refund initiated for order {order_id}."

def issue_partial_refund(order_id):
    return f"Partial refund issued for order {order_id}."

def cancel_subscription(user_id):
    return f"Subscription cancelled for user {user_id}."

def check_subscription_status(user_id):
    return f"Subscription for {user_id} is active."

def apply_discount(user_id, percent):
    return f"{percent}% discount applied to user {user_id}'s account."

def check_order_status(order_id):
    return f"Order {order_id} is currently in transit."

def resend_invoice(order_id):
    return f"Invoice resent for order {order_id}."

def update_shipping_address(order_id):
    return f"Shipping address updated for order {order_id}."

def flag_suspicious_activity(user_id):
    return f"Suspicious activity flagged for user {user_id}."

def temporarily_suspend_account(user_id):
    return f"Account {user_id} temporarily suspended."

def mark_case_high_priority(ticket_id):
    return f"Ticket {ticket_id} marked as high priority."

def escalate_ticket(ticket_id):
    return f"Ticket {ticket_id} escalated to human support."