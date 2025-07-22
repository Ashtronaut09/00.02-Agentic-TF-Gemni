#!/usr/bin/env python3
"""
Agent Helper - Use this in Terminal 2 (Code Agent)
"""

import json
import time
from datetime import datetime
import re

def auto_assign_role(role_to_assign=None):
    """Automatically assign to a role that has pending tasks."""
    # 1. Get pending tasks
    try:
        with open("agents/tasks.json", "r") as f:
            tasks = json.load(f)
        pending_tasks = tasks.get("pending_tasks", [])
        if not pending_tasks:
            print("⏳ No pending tasks. No role will be assigned.")
            return None, None
    except FileNotFoundError:
        print("❌ tasks.json not found. No role will be assigned.")
        return None, None

    # 2. Get required roles from tasks that are pending
    required_roles = {
        task.get("data", {}).get("target_role")
        for task in pending_tasks
        if task.get("status") == "pending" and task.get("data", {}).get("target_role")
    }
    if not required_roles:
        print("⏳ No tasks with specific target roles are pending. No role will be assigned.")
        return None, None
    
    print(f"📋 Roles required by pending tasks: {list(required_roles)}")

    # 3. Read current role assignments from instructions
    with open("agents/AGENT_INSTRUCTIONS.md", "r") as f:
        content = f.read()

    # 4. Find an available role that is also a required role
    if role_to_assign:
        roles_to_check = [role_to_assign]
    else:
        roles_to_check = ['ARCHITECT', 'TERRAFORM_DEVELOPER', 'PLATFORM_ENGINEER', 'COMPLIANCE_ADMIN', 'FINOPS']

    for role in roles_to_check:
        # Check if the role is both required and available
        if role in required_roles and f"{role}: AVAILABLE" in content:
            # Assign this role
            terminal_id = f"terminal-{int(time.time() % 10000)}"
            updated_content = content.replace(f"{role}: AVAILABLE", f"{role}: {terminal_id}", 1)
            
            with open("agents/AGENT_INSTRUCTIONS.md", "w") as f:
                f.write(updated_content)
            
            print(f"✅ ROLE ASSIGNED (based on pending tasks): {role}")
            print(f"🆔 Terminal ID: {terminal_id}")
            return role, terminal_id

    if role_to_assign:
        print(f"❌ Role {role_to_assign} is not available or not required for any pending tasks.")
    else:
        print("❌ No available roles match the roles required for pending tasks.")
    return None, None

def get_pending_tasks():
    """Get all pending tasks"""
    with open("agents/tasks.json", "r") as f:
        tasks = json.load(f)
    return tasks["pending_tasks"]

def initialize_agent(role_to_assign=None):
    """Complete agent initialization process"""
    print("🤖 INITIALIZING AGENT...")
    print()
    
    # Step 1: Self-assign role
    role, terminal_id = auto_assign_role(role_to_assign)
    
    if not role:
        print("❌ Agent initialization failed - no available roles")
        return
    
    print()
    print(f"✅ AGENT INITIALIZED")
    print(f"🎭 I am a {role}")
    print(f"🆔 Terminal ID: {terminal_id}")
    print()
    
    # Step 2: Show persona description
    role_descriptions = {
        'ARCHITECT': 'I design high-level system architecture and create technical blueprints.',
        'TERRAFORM_DEVELOPER': 'I write terraform infrastructure code and implement technical solutions.',
        'PLATFORM_ENGINEER': 'I design for scale, reliability, and operational excellence.',
        'COMPLIANCE_ADMIN': 'I ensure security and compliance requirements are met.',
        'FINOPS': 'I optimize cloud costs and implement financial governance policies.'
    }
    
    if role in role_descriptions:
        print(f"🎯 My role: {role_descriptions[role]}")
        print()
    
    # Step 3: Check ALL tasks first
    print("📋 Checking all pending tasks in system...")
    all_tasks = get_pending_tasks()
    
    if all_tasks:
        print(f"📊 Found {len(all_tasks)} total pending task(s) in system:")
        for task in all_tasks:
            target_role = task.get('data', {}).get('target_role', 'NO TARGET ROLE')
            is_mine = target_role == role
            marker = "✅" if is_mine else "⏳"
            print(f"  {marker} {task['description']} (ID: {task['id']}) → {target_role}")
    else:
        print("📊 No pending tasks in system")
    
    print()
    
    # Step 4: Check MY tasks specifically
    my_tasks = [t for t in all_tasks if t.get('data', {}).get('target_role') == role]
    
    if my_tasks:
        print(f"🎯 MY TASKS ({role}):")
        for task in my_tasks:
            print(f"  ✅ {task['description']} (ID: {task['id']})")
            print(f"      Status: {task.get('status', 'unknown')}")
        print()
        print("🚀 Ready to start working! Use start_task(task_id) to begin.")
    else:
        print(f"⏳ No tasks currently assigned to {role}")
        print("💡 Waiting for orchestrator to send tasks for my role...")
    
    print()
    print("🔧 Available Commands:")
    print("  get_pending_tasks() - Get all pending tasks")
    print("  start_task(task_id) - Start working on a task")
    print("  complete_task(task_id, description, output) - Complete a task")
    print()
    
    return role, terminal_id

def check_for_tasks():
    """Check for new tasks from orchestrator"""
    with open("agents/tasks.json", "r") as f:
        tasks = json.load(f)
    
    current_task = tasks["current_task"]
    if current_task and current_task["status"] == "pending":
        print(f"📋 New task received: {current_task['description']}")
        print(f"🔧 Type: {current_task['type']}")
        print(f"📊 Task ID: {current_task['id']}")
        print(f"📄 Data: {current_task.get('data', {})}")
        return current_task
    else:
        print("⏳ No pending tasks")
        return None

def start_task(task_id):
    """Mark a task as started"""
    # Update task status
    with open("agents/tasks.json", "r") as f:
        tasks = json.load(f)
    
    if tasks["current_task"] and tasks["current_task"]["id"] == task_id:
        tasks["current_task"]["status"] = "in_progress"
        tasks["current_task"]["started_at"] = datetime.now().isoformat()
    
    with open("agents/tasks.json", "w") as f:
        json.dump(tasks, f, indent=2)
    
    # Update status
    with open("agents/status.json", "r") as f:
        status = json.load(f)
    
    status["agent_status"] = "working"
    status["last_update"] = datetime.now().isoformat()
    
    with open("agents/status.json", "w") as f:
        json.dump(status, f, indent=2)
    
    print(f"▶️ Started working on task: {task_id}")

def complete_task(task_id, result_description, output=None, success=True):
    """Mark a task as completed and send results"""
    result = {
        "task_id": task_id,
        "description": result_description,
        "output": output,
        "status": "completed" if success else "failed",
        "timestamp": datetime.now().isoformat()
    }
    
    # Update results
    with open("agents/results.json", "r") as f:
        results = json.load(f)
    
    results["latest_result"] = result
    results["results_history"].append(result)
    
    with open("agents/results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    # Update task status
    with open("agents/tasks.json", "r") as f:
        tasks = json.load(f)
    
    if tasks["current_task"] and tasks["current_task"]["id"] == task_id:
        tasks["current_task"]["status"] = "completed" if success else "failed"
        tasks["current_task"]["completed_at"] = datetime.now().isoformat()
        tasks["task_history"].append(tasks["current_task"])
        tasks["current_task"] = None
    
    with open("agents/tasks.json", "w") as f:
        json.dump(tasks, f, indent=2)
    
    # Update status
    with open("agents/status.json", "r") as f:
        status = json.load(f)
    
    status["agent_status"] = "idle"
    status["current_task_id"] = None
    status["last_update"] = datetime.now().isoformat()
    
    with open("agents/status.json", "w") as f:
        json.dump(status, f, indent=2)
    
    print(f"✅ Task completed: {result_description}")

def get_current_task():
    """Get the current task details"""
    with open("agents/tasks.json", "r") as f:
        tasks = json.load(f)
    
    if tasks["current_task"]:
        print(f"📋 Current task: {tasks['current_task']['description']}")
        print(f"🔧 Status: {tasks['current_task']['status']}")
        print(f"📊 ID: {tasks['current_task']['id']}")
        return tasks["current_task"]
    else:
        print("📭 No current task")
        return None

if __name__ == "__main__":
    import sys
    role_to_assign = None
    if len(sys.argv) > 1:
        role_to_assign = sys.argv[1]
    
    print("🤖 Agent Helper - Terminal 2")
    print("Commands:")
    print("  check_for_tasks()")
    print("  start_task('task_id')")
    print("  complete_task('task_id', 'Generated terraform config', 'output_here')")
    print("  get_current_task()")

    initialize_agent(role_to_assign)