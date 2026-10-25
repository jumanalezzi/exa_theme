import json
import frappe
import os
import subprocess
import shutil

def after_install():
    print("Starting Madar post-installation tasks...")
    
    bench_path = frappe.utils.get_bench_path()
    site_name = frappe.local.site
    
    # 1. Ensure POS Awesome is installed
    installed_apps = frappe.get_installed_apps()
    if "posawesome" not in installed_apps:
        print("POS Awesome is not installed. Installing it now...")
        try:
            # Check if it's already downloaded in apps folder
            posawesome_app_path = os.path.join(bench_path, "apps", "posawesome")
            if not os.path.exists(posawesome_app_path):
                print("Fetching POS Awesome from GitHub...")
                subprocess.run(["bench", "get-app", "https://github.com/Chabari/POS-Awesome-V15"], cwd=bench_path, check=True)
            
            print("Installing POS Awesome on site...")
            lock_path = os.path.join(frappe.get_site_path(), "locks", "install_app.lock")
            if os.path.exists(lock_path):
                os.remove(lock_path)
            subprocess.run(["bench", "--site", site_name, "install-app", "posawesome"], cwd=bench_path, check=True)
            print("POS Awesome installed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to install POS Awesome: {e}")
            return
            
    # 2. Apply modifications to POS Awesome
    print("Applying custom modifications to POS Awesome...")
    
    admin_app_path = frappe.get_app_path("admin")
    mods_path = os.path.abspath(os.path.join(admin_app_path, "..", "posawesome_modifications"))
    
    posawesome_path = frappe.get_app_path("posawesome")
    frontend_components_path = os.path.abspath(os.path.join(posawesome_path, "..", "frontend", "src", "posapp", "components", "pos"))
    
    if os.path.exists(mods_path) and os.path.exists(frontend_components_path):
        modified = False
        for file_name in os.listdir(mods_path):
            src = os.path.join(mods_path, file_name)
            dst = os.path.join(frontend_components_path, file_name)
            if os.path.isfile(src):
                shutil.copy2(src, dst)
                print(f"Copied {file_name} to POS Awesome.")
                modified = True
                
        
        if shutil.which('yarn') is None:
            frappe.throw("أداة yarn غير مثبتة في هذا الخادم وهي مطلوبة لبناء POS Awesome. يرجى تثبيتها أولاً.")
            
        if modified:
            frontend_path = os.path.abspath(os.path.join(posawesome_path, "..", "frontend"))
            print("Building POS Awesome frontend... This might take a minute or two.")
            try:
                subprocess.run(["yarn", "build"], cwd=frontend_path, check=True, capture_output=True)
                print("POS Awesome frontend built successfully.")
            except subprocess.CalledProcessError as e:
                print(f"Failed to build POS Awesome frontend: {e.stderr.decode('utf-8') if e.stderr else str(e)}")
    else:
        print(f"Modifications path or frontend path not found. {mods_path} / {frontend_components_path}")
    # import_default_data()  # Removed default data import
    print("Madar post-installation tasks completed.")


def import_default_data():
    pass
