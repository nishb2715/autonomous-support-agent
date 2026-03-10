#tool execution layer 

def execute_tool(tool_name, tool_args, ticket_text=None):

    if tool_name == "process_refund":
        return process_refund(tool_args, ticket_text)

    elif tool_name == "issue_partial_refund":
        return issue_partial_refund(tool_args)

    elif tool_name == "reset_password":
        return reset_password(tool_args)

    elif tool_name == "lock_account":
        return lock_account(tool_args)

    elif tool_name == "unlock_account":
        return unlock_account(tool_args)

    elif tool_name == "cancel_subscription":
        return cancel_subscription(tool_args)

    elif tool_name == "check_order_status":
        return check_order_status(tool_args)

    elif tool_name == "resend_invoice":
        return resend_invoice(tool_args)

    elif tool_name == "apply_discount":
        return apply_discount(tool_args)

    elif tool_name == "update_shipping_address":
        return update_shipping_address(tool_args)

    elif tool_name == "escalate_ticket":
        return escalate_ticket(tool_args)

    else:
        return {"status": "no_tool_executed"}


#tool implementations
import re 
def process_refund(args, ticket_text=None):

    amount = args.get("amount")
    order_id = args.get("order_id")

    #extracting order id if missing
    if not order_id and ticket_text:
        match = re.search(r'order\s*(\d+)', ticket_text.lower())
        if match:
            order_id = match.group(1)

    if not amount:
        amount = "the duplicate charge"

    if order_id:
        return {
            "status": "success",
            "message": f"A refund for order {order_id} has been initiated and will reflect within 3–5 business days."
        }

    return {
        "status": "success",
        "message": f"A refund has been initiated and will reflect within 3–5 business days."
    }


def issue_partial_refund(args):

    amount = args.get("amount", "unknown")

    return {
        "status": "success",
        "message": f"A partial refund of ₹{amount} has been issued."
    }


def reset_password(args):

    return {
        "status": "success",
        "message": "A password reset link has been sent to your registered email."
    }


def lock_account(args):

    return {
        "status": "success",
        "message": "Your account has been temporarily locked for security reasons."
    }


def unlock_account(args):

    return {
        "status": "success",
        "message": "Your account has been successfully unlocked."
    }


def cancel_subscription(args):

    return {
        "status": "success",
        "message": "Your subscription has been cancelled."
    }


def check_order_status(args):

    order_id = args.get("order_id", "unknown")

    return {
        "status": "success",
        "message": f"Order {order_id} is currently in transit and will arrive within 2 days."
    }


def resend_invoice(args):

    return {
        "status": "success",
        "message": "The invoice has been resent to your email."
    }


def apply_discount(args):

    code = args.get("code", "WELCOME10")

    return {
        "status": "success",
        "message": f"A discount code {code} has been applied to your account."
    }


def update_shipping_address(args):

    return {
        "status": "success",
        "message": "Your shipping address has been successfully updated."
    }


def escalate_ticket(args):

    return {
        "status": "success",
        "message": "Your ticket has been escalated to a human support agent."
    }