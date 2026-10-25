# -*- coding: utf-8 -*-
import frappe

def verify_app_license(*args, **kwargs):
    """
    License verification bypass for Etqan.
    Allows unrestricted operation without license checks.
    """
    return True
