#!/usr/bin/env python3
"""
Orchestrator Helper - Use this in Terminal 1 (Gemini Code Orchestrator)
"""

import json
import time
from datetime import datetime

def get_orchestration_status():
    """Get current orchestration status and determine next steps"""
    try:
        with open("agents/status.json", "r") as f:
            status = json.load(f)
        
        with open("agents/tasks.json", "r") as f:
            tasks = json.load(f)
        
        with open("agents/results.json", "r") as f:
            results = json.load(f)
        
        # Determine orchestration stage
        pending_tasks = [t for t in tasks["pending_tasks"] if t["status"] == "pending"]
        in_progress_tasks = [t for t in tasks["pending_tasks"] if t["status"] == "in_progress"]
        completed_tasks = [t for t in tasks["task_history"] if t["status"] == "completed"]
        
        if not pending_tasks and not in_progress_tasks and completed_tasks:
            stage = "orchestration_complete"
        elif in_progress_tasks:
            stage = "work_in_progress"
        elif pending_tasks:
            stage = "tasks_pending"
        else:
            stage = "ready_for_tasks"
        
        return {
            "stage": stage,
            "pending_tasks": len(pending_tasks),
            "in_progress_tasks": len(in_progress_tasks),
            "completed_tasks": len(completed_tasks),
            "latest_result": results.get("latest_result"),
            "orchestrator_status": status.get("orchestrator_status", "unknown")
        }
    except FileNotFoundError:
        return {"stage": "needs_initialization", "error": "JSON files not found"}

def resume_orchestration():
    """Resume orchestration from current state without clearing data"""
    print("🔄 RESUMING ORCHESTRATION FROM CURRENT STATE...")
    print()
    
    # Get current status
    status = get_orchestration_status()
    
    print(f"📊 Current Stage: {status['stage']}")
    print(f"⏳ Pending Tasks: {status['pending_tasks']}")
    print(f"🔄 In Progress: {status['in_progress_tasks']}")
    print(f"✅ Completed: {status['completed_tasks']}")
    print()
    
    # Handle different orchestration stages
    if status["stage"] == "needs_initialization":
        print("🚀 FIRST-TIME INITIALIZATION")
        print("Creating clean JSON files for new orchestration...")
        initialize_clean_slate()
        
    elif status["stage"] == "orchestration_complete":
        print("🎉 ORCHESTRATION COMPLETE!")
        print("All tasks have been completed successfully.")
        if status["latest_result"]:
            print(f"📥 Latest result: {status['latest_result']['description']}")
        print()
        print("🔧 Available actions:")
        print("  • check_results() - View all completed work")
        print("  • start_new_orchestration() - Begin new project")
        print("  • send_task() - Add additional tasks")
        
    elif status["stage"] == "work_in_progress":
        print("🔄 WORK IN PROGRESS")
        print("Some tasks are currently being worked on by agents.")
        print("💡 Use get_status() and check_results() to monitor progress")
        
    elif status["stage"] == "tasks_pending":
        print("⏳ TASKS PENDING")
        print("Tasks are waiting for agents to claim and complete them.")
        print("💡 Agents can run initialize_agent() to claim available tasks")
        
    elif status["stage"] == "ready_for_tasks":
        print("🎯 READY FOR TASKS")
        print("System is ready to receive new tasks.")
        print("💡 Use send_task() to add work for agents")
    
    # Update orchestrator status
    update_orchestrator_status("resumed")
    
    print()
    print("🔧 Available Commands:")
    print("  get_orchestration_status() - Check current progress")
    print("  send_task(type, description, data) - Add new tasks")
    print("  check_results() - View completed work")
    print("  get_status() - Check agent status")
    print("  start_new_orchestration() - Begin fresh project")
    
    return status

def initialize_clean_slate():
    """Initialize clean slate for new orchestration"""
    print("🧹 INITIALIZING CLEAN SLATE...")
    
    # Clear tasks
    with open("agents/tasks.json", "w") as f:
        json.dump({
            "current_task": None,
            "pending_tasks": [],
            "task_history": []
        }, f, indent=2)
    
    # Clear results  
    with open("agents/results.json", "w") as f:
        json.dump({
            "latest_result": None,
            "results_history": []
        }, f, indent=2)
    
    # Clear status
    with open("agents/status.json", "w") as f:
        json.dump({
            "orchestrator_status": "initialized",
            "agent_status": "idle",
            "last_update": datetime.now().isoformat(),
            "current_task_id": None
        }, f, indent=2)
    
    print("✅ Clean slate initialized")

def start_new_orchestration():
    """Start completely new orchestration (clears everything)"""
    print("🚀 STARTING NEW ORCHESTRATION...")
    print("⚠️  This will clear all previous work and start fresh.")
    
    # Initialize clean slate
    initialize_clean_slate()
    
    # Reset role assignments to AVAILABLE
    with open("agents/AGENT_INSTRUCTIONS.md", "r") as f:
        content = f.read()
    
    # Reset all roles to AVAILABLE
    roles = ['ORCHESTRATOR', 'ARCHITECT', 'TERRAFORM_DEVELOPER', 'PLATFORM_ENGINEER', 'COMPLIANCE_ADMIN', 'FINOPS']
    
    import re
    for role in roles:
        # This regex finds the role and whatever it is assigned to, and replaces it with AVAILABLE
        content = re.sub(f"({role}: ).*", f"\\1AVAILABLE", content)
    
    with open("agents/AGENT_INSTRUCTIONS.md", "w") as f:
        f.write(content)
    
    print("✅ New orchestration started - all roles reset to AVAILABLE")
    print("🎯 System ready for new project")

def update_orchestrator_status(status_value):
    """Update orchestrator status"""
    try:
        with open("agents/status.json", "r") as f:
            status = json.load(f)
    except FileNotFoundError:
        status = {}
    
    status["orchestrator_status"] = status_value
    status["last_update"] = datetime.now().isoformat()
    
    with open("agents/status.json", "w") as f:
        json.dump(status, f, indent=2)

def send_task(task_type, description, data=None):
    """Send a task to the agent"""
    task = {
        "id": str(int(time.time())),
        "type": task_type,
        "description": description,
        "data": data or {},
        "timestamp": datetime.now().isoformat(),
        "status": "pending"
    }
    
    # Read current tasks
    with open("agents/tasks.json", "r") as f:
        tasks = json.load(f)
    
    # Add new task
    tasks["current_task"] = task
    tasks["pending_tasks"].append(task)
    
    # Write back
    with open("agents/tasks.json", "w") as f:
        json.dump(tasks, f, indent=2)
    
    # Update status
    with open("agents/status.json", "r") as f:
        status = json.load(f)
    
    status["orchestrator_status"] = "task_sent"
    status["current_task_id"] = task["id"]
    status["last_update"] = datetime.now().isoformat()
    
    with open("agents/status.json", "w") as f:
        json.dump(status, f, indent=2)
    
    print(f"✅ Task sent: {task['description']}")
    print(f"📋 Task ID: {task['id']}")
    return task["id"]

def check_results():
    """Check for results from the agent"""
    with open("agents/results.json", "r") as f:
        results = json.load(f)
    
    if results["latest_result"]:
        print(f"📥 Latest result: {results['latest_result']['description']}")
        print(f"🔧 Status: {results['latest_result']['status']}")
        if results["latest_result"]["output"]:
            print(f"📄 Output: {results['latest_result']['output']}")
        return results["latest_result"]
    else:
        print("⏳ No results yet")
        return None

def get_status():
    """Get current status of both agents"""
    with open("agents/status.json", "r") as f:
        status = json.load(f)
    
    print(f"🎯 Orchestrator: {status['orchestrator_status']}")
    print(f"🤖 Agent: {status['agent_status']}")
    print(f"📊 Current Task ID: {status['current_task_id']}")
    print(f"⏰ Last Update: {status['last_update']}")
    return status

if __name__ == "__main__":
    print("🎯 Orchestrator Helper - Terminal 1")
    print("Commands:")
    print("  send_task(task_type, description, data)")
    print("  check_results()")
    print("  get_status()")