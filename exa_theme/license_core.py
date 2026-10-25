# -*- coding: utf-8 -*-
import frappe

def verify_app_license(*args, **kwargs):
    """
    License verification bypass for Exa Theme.
    Allows unrestricted operation without license checks.
    """
    return True
