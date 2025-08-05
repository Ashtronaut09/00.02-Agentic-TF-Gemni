# Agentic Terraform Framework

A multi-agent system for collaborative Terraform infrastructure development with specialized AI agents for architecture design, development, platform engineering, security compliance, and cost optimization. It was originally for Gemini but I couldn't get Gemini CLI to work consistently so I switched back to Claude. Run it with other LLMs are your own risk!

## 🏗️ System Overview

This framework uses multiple AI agents working together to design, develop, test, and deploy infrastructure code through a coordinated workflow. Each agent specializes in a specific domain:

- **ORCHESTRATOR**: Coordinates tasks and manages workflow between agents
- **ARCHITECT**: Designs system architecture and creates technical blueprints  
- **TERRAFORM_DEVELOPER**: Writes and tests infrastructure code
- **PLATFORM_ENGINEER**: Reviews for scalability and operational excellence
- **COMPLIANCE_ADMIN**: Ensures security and compliance requirements
- **FINOPS**: Optimizes costs and implements financial governance

## 📋 Prerequisites

### Required Software
- **Claude Code CLI** - AI-powered coding assistant with terminal access
- **Python 3.7+** - For agent helper scripts and MCP server
- **Terraform** - Infrastructure as code tool (for actual deployment)
- **Git** - Version control (recommended)

### Required Python Packages
```bash
pip install json datetime time re
```

### Optional Dependencies
- **AWS CLI** - For AWS provider authentication
- **Terraform Cloud Account** - For remote state management
- **VS Code** - For file editing (or any preferred editor)

## 🚀 Quick Start Guide

### Step 1: Initialize the Orchestrator (Terminal 1)

Open Claude Code in your first terminal and navigate to the project directory:

```bash
cd "/path/to/Agentic-TF-Framework"
```

Initialize the orchestrator by saying:
```
Initialize as orchestrator
```

This will:
- Resume from current state (preserves existing work)
- Import orchestrator helper functions
- Claim the ORCHESTRATOR role
- Show current progress and available commands

### Step 2: Initialize Agents (Terminal 2+)

For each additional agent you want to run, open a new Claude Code terminal and run:

```bash
python3 -c "import sys; sys.path.append('agents'); from agent_helper import initialize_agent; initialize_agent()"
```

This will:
- Check for pending tasks
- Auto-assign to an available role that has pending work
- Show role-specific instructions and available tasks
- Import agent helper functions

## 🔄 Standard Workflow

### Phase 0: Architecture Planning (Recommended)
1. **Orchestrator** sends `architecture_planning` task to **ARCHITECT**
2. **ARCHITECT** creates system design and technical blueprints

### Phase 1: Initial Development & Testing  
3. **Orchestrator** sends `generate_terraform` task to **TERRAFORM_DEVELOPER**
4. **TERRAFORM_DEVELOPER** writes infrastructure code
5. **Orchestrator** sends `test_terraform` task to same **TERRAFORM_DEVELOPER**
6. **TERRAFORM_DEVELOPER** validates and tests the code

### Phase 2: Platform Validation
7. **Orchestrator** sends `plan_and_validate_terraform` task to **PLATFORM_ENGINEER** 
8. **PLATFORM_ENGINEER** reviews for scalability and best practices
9. **User Approval** - Orchestrator presents plan for user approval

### Phase 3: Compliance Review
10. **Orchestrator** sends `security_review` task to **COMPLIANCE_ADMIN**
11. **COMPLIANCE_ADMIN** reviews for security and compliance
12. **TERRAFORM_DEVELOPER** implements any required fixes

### Phase 4: Cost Optimization (Optional)
13. **Orchestrator** sends `cost_review` task to **FINOPS**
14. **FINOPS** analyzes and optimizes costs

### Phase 5: Final Deployment
15. User instructs **Orchestrator** to proceed with deployment

## 🎯 Role-Specific Commands

### Orchestrator Commands
```python
# Send tasks to agents
send_task('architecture_planning', 'Design web app infrastructure', {
    'target_role': 'ARCHITECT', 
    'project_name': 'webapp',
    'requirements': 'EC2, S3, RDS'
})

# Monitor progress
get_orchestration_status()
check_results()
get_status()

# Manage orchestration
start_new_orchestration()  # Clear everything and start fresh
resume_orchestration()     # Resume from current state
```

### Agent Commands
```python
# Check for work
get_pending_tasks()

# Start working
start_task('task_id_here')

# Complete work
complete_task('task_id_here', 'Task description', 'Detailed output')

# Check current status
get_current_task()
```

## 📁 File Structure

```
agents/
├── AGENT_INSTRUCTIONS.md     # Role definitions and workflows
├── orchestrator_helper.py    # Orchestrator utility functions  
├── agent_helper.py          # Agent utility functions
├── tasks.json              # Task queue and history
├── status.json             # Current system status
├── results.json            # Completed task results
├── terraform_mcp_server.py # MCP server for Terraform operations
└── requirements.txt        # Python dependencies
```

## 🔧 Common Task Types

### Architecture Tasks
- `architecture_planning` - Create system architecture
- `requirements_analysis` - Analyze business requirements
- `solution_design` - Design technical solutions

### Development Tasks  
- `generate_terraform` - Write infrastructure code
- `test_terraform` - Test and validate code
- `implement_changes` - Apply feedback and fixes
- `debug_terraform_error` - Fix infrastructure issues

### Platform Tasks
- `plan_and_validate_terraform` - Review and validate infrastructure
- `design_architecture` - Create scalable designs
- `optimize_performance` - Improve efficiency

### Security Tasks
- `security_review` - Review for security compliance
- `compliance_check` - Validate against frameworks
- `implement_security_controls` - Add security features

### FinOps Tasks
- `cost_optimization` - Analyze and optimize costs
- `budget_analysis` - Create budget forecasts
- `cost_review` - Review code for cost efficiency

## 🌟 Example Usage Session

### 1. Start Orchestrator
```
Terminal 1 (Claude Code):
> Initialize as orchestrator

🎯 READY FOR TASKS
System is ready to receive new tasks.
```

### 2. Request Architecture
```
Terminal 1:
> Please design a video streaming platform for 10TB storage and thousands of users

✅ Task sent: Design video streaming platform infrastructure  
📋 Task ID: 1234567890
```

### 3. Initialize Architect Agent
```
Terminal 2 (Claude Code):
> python3 -c "import sys; sys.path.append('agents'); from agent_helper import initialize_agent; initialize_agent()"

✅ ROLE ASSIGNED: ARCHITECT
🎯 MY TASKS (ARCHITECT):
  ✅ Design video streaming platform infrastructure (ID: 1234567890)
```

### 4. Continue Workflow
The system automatically progresses through development, testing, platform review, security review, and deployment phases as agents complete their tasks.

## 🛠️ Advanced Features

### Dynamic Role Assignment
- Agents automatically assign to roles based on pending work
- No manual role configuration required
- Prevents role conflicts and ensures efficient task distribution

### Intelligent State Management
- Preserves work across terminal sessions
- Supports resuming from any point in the workflow
- Tracks task history and results

### Multi-Environment Support
- Variable-driven environment configuration
- Support for dev/staging/production deployments
- Environment-specific validation and testing

### Error Handling
- Role-specific error routing (syntax → TERRAFORM_DEVELOPER, security → COMPLIANCE_ADMIN)
- Automatic retry and recovery mechanisms
- Detailed error reporting and resolution guidance

## 📊 Monitoring and Status

### Check Overall Progress
```python
get_orchestration_status()  # Shows current stage and task counts
```

### Monitor Agent Activity
```python
get_status()  # Shows orchestrator and agent status
```

### View Results
```python
check_results()  # Shows latest completed work
```

## 🔄 Workflow States

The system tracks different orchestration stages:

- **🚀 ready_for_tasks** - Ready to receive new work
- **⏳ tasks_pending** - Tasks waiting for agents  
- **🔄 work_in_progress** - Tasks being worked on
- **🎉 orchestration_complete** - All work finished
- **🧹 needs_initialization** - First-time setup required

## 🔐 Security Considerations

- All infrastructure follows security best practices
- Encryption at rest and in transit
- Least privilege IAM policies
- VPC isolation and network security
- Compliance framework validation

## 💰 Cost Management

- Built-in cost optimization recommendations
- Resource right-sizing suggestions
- Lifecycle policies for storage optimization
- Reserved instance planning
- Budget monitoring and alerts

## 🤝 Contributing

1. Follow the established role patterns in AGENT_INSTRUCTIONS.md
2. Test workflows end-to-end before submitting changes
3. Update documentation for new task types or roles
4. Ensure security and cost optimization remain priorities

## 📄 License

[Add your license information here]

## 🆘 Troubleshooting

### Common Issues

**Agent won't initialize:**
- Check that tasks.json, status.json, and results.json exist
- Verify Python path includes 'agents' directory
- Ensure no pending tasks exist for unavailable roles

**Tasks not being claimed:**  
- Verify agent has correct role assignment in AGENT_INSTRUCTIONS.md
- Check that target_role in task data matches available agents
- Confirm agent is running initialize_agent() correctly

**Orchestrator not responding:**
- Ensure orchestrator is initialized: "Initialize as orchestrator"  
- Check orchestrator status with get_status()
- Verify file permissions for JSON files

**State management issues:**
- Use start_new_orchestration() to completely reset
- Check file contents of tasks.json, status.json, results.json
- Ensure proper file write permissions

### Getting Help

1. Check agent status and current tasks
2. Review AGENT_INSTRUCTIONS.md for role-specific guidance  
3. Examine JSON files for state information
4. Use clean slate initialization if needed: start_new_orchestration()

---

*This framework enables collaborative AI-driven infrastructure development with built-in best practices for security, scalability, and cost optimization.*