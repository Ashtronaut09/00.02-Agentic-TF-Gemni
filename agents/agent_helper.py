#!/usr/bin/env python3
"""
Agent Helper - Use this in Terminal 2 (Claude Code Agent)
"""

import json
import time
from datetime import datetime
import re

def auto_assign_role():
    """Automatically assign to first available role"""
    # Read current role assignments
    with open("agents/AGENT_INSTRUCTIONS.md", "r") as f:
        content = f.read()
    
    # Find role assignments section
    roles = ['ARCHITECT', 'TERRAFORM_DEVELOPER', 'PLATFORM_ENGINEER', 'COMPLIANCE_ADMIN', 'FINOPS']
    
    for role in roles:
        if f"{role}: AVAILABLE" in content:
            # Generate terminal ID
            terminal_id = f"claude-terminal-{int(time.time() % 10000)}"
            
            # Update role assignment
            updated_content = content.replace(f"{role}: AVAILABLE", f"{role}: {terminal_id}")
            
            with open("agents/AGENT_INSTRUCTIONS.md", "w") as f:
                f.write(updated_content)
            
            print(f"✅ ROLE ASSIGNED: {role}")
            print(f"🆔 Terminal ID: {terminal_id}")
            return role, terminal_id
    
    print("❌ No available roles found")
    return None, None

def get_pending_tasks():
    """Get all pending tasks"""
    with open("agents/tasks.json", "r") as f:
        tasks = json.load(f)
    return tasks["pending_tasks"]

def initialize_agent():
    """Complete agent initialization process"""
    print("🤖 INITIALIZING AGENT...")
    print()
    
    # Step 1: Self-assign role
    role, terminal_id = auto_assign_role()
    
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
    print("🤖 Agent Helper - Terminal 2")
    print("Commands:")
    print("  check_for_tasks()")
    print("  start_task('task_id')")
    print("  complete_task('task_id', 'Generated terraform config', 'output_here')")
    print("  get_current_task()")