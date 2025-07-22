#!/usr/bin/env python3
"""
Terraform MCP Server for Agentic System
Provides Terraform operations to Claude agents via MCP protocol
"""

import asyncio
import json
import os
import subprocess
import sys
from typing import Any, Dict, List, Optional

from mcp.server import Server
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
    LoggingLevel
)
import mcp.server.stdio

# Server instance
server = Server("terraform-agent")

# Get the terraform directory from environment or use current directory
TERRAFORM_DIR = os.getenv("TERRAFORM_DIR", os.getcwd())

@server.list_resources()
async def list_resources() -> List[Resource]:
    """List available Terraform resources"""
    resources = []
    
    # List terraform files
    for file in os.listdir(TERRAFORM_DIR):
        if file.endswith('.tf'):
            resources.append(
                Resource(
                    uri=f"file://{TERRAFORM_DIR}/{file}",
                    name=f"Terraform Config: {file}",
                    mimeType="text/plain",
                    description=f"Terraform configuration file: {file}"
                )
            )
    
    # List tfvars files
    for file in os.listdir(TERRAFORM_DIR):
        if file.endswith('.tfvars'):
            resources.append(
                Resource(
                    uri=f"file://{TERRAFORM_DIR}/{file}",
                    name=f"Terraform Variables: {file}",
                    mimeType="text/plain",
                    description=f"Terraform variables file: {file}"
                )
            )
    
    return resources

@server.read_resource()
async def read_resource(uri: str) -> str:
    """Read a terraform resource file"""
    if not uri.startswith("file://"):
        raise ValueError(f"Unsupported URI scheme: {uri}")
    
    path = uri[7:]  # Remove "file://" prefix
    
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")
    
    with open(path, 'r') as f:
        content = f.read()
    
    return content

@server.list_tools()
async def list_tools() -> List[Tool]:
    """List available Terraform tools"""
    return [
        Tool(
            name="terraform_init",
            description="Initialize Terraform working directory",
            inputSchema={
                "type": "object",
                "properties": {
                    "working_dir": {
                        "type": "string",
                        "description": "Working directory for Terraform (optional)",
                        "default": TERRAFORM_DIR
                    }
                }
            }
        ),
        Tool(
            name="terraform_plan",
            description="Create Terraform execution plan",
            inputSchema={
                "type": "object",
                "properties": {
                    "working_dir": {
                        "type": "string",
                        "description": "Working directory for Terraform (optional)",
                        "default": TERRAFORM_DIR
                    },
                    "var_file": {
                        "type": "string",
                        "description": "Variable file to use (optional)"
                    },
                    "target": {
                        "type": "string",
                        "description": "Target specific resources (optional)"
                    }
                }
            }
        ),
        Tool(
            name="terraform_apply",
            description="Apply Terraform changes",
            inputSchema={
                "type": "object",
                "properties": {
                    "working_dir": {
                        "type": "string",
                        "description": "Working directory for Terraform (optional)",
                        "default": TERRAFORM_DIR
                    },
                    "var_file": {
                        "type": "string",
                        "description": "Variable file to use (optional)"
                    },
                    "auto_approve": {
                        "type": "boolean",
                        "description": "Auto-approve the apply",
                        "default": False
                    }
                }
            }
        ),
        Tool(
            name="terraform_destroy",
            description="Destroy Terraform-managed infrastructure",
            inputSchema={
                "type": "object",
                "properties": {
                    "working_dir": {
                        "type": "string",
                        "description": "Working directory for Terraform (optional)",
                        "default": TERRAFORM_DIR
                    },
                    "var_file": {
                        "type": "string",
                        "description": "Variable file to use (optional)"
                    },
                    "auto_approve": {
                        "type": "boolean",
                        "description": "Auto-approve the destroy",
                        "default": False
                    }
                }
            }
        ),
        Tool(
            name="terraform_validate",
            description="Validate Terraform configuration",
            inputSchema={
                "type": "object",
                "properties": {
                    "working_dir": {
                        "type": "string",
                        "description": "Working directory for Terraform (optional)",
                        "default": TERRAFORM_DIR
                    }
                }
            }
        ),
        Tool(
            name="terraform_fmt",
            description="Format Terraform configuration files",
            inputSchema={
                "type": "object",
                "properties": {
                    "working_dir": {
                        "type": "string",
                        "description": "Working directory for Terraform (optional)",
                        "default": TERRAFORM_DIR
                    },
                    "check": {
                        "type": "boolean",
                        "description": "Check if formatting is needed without making changes",
                        "default": False
                    }
                }
            }
        ),
        Tool(
            name="terraform_show",
            description="Show Terraform state or plan",
            inputSchema={
                "type": "object",
                "properties": {
                    "working_dir": {
                        "type": "string",
                        "description": "Working directory for Terraform (optional)",
                        "default": TERRAFORM_DIR
                    },
                    "format": {
                        "type": "string",
                        "description": "Output format (json, text)",
                        "default": "text"
                    }
                }
            }
        ),
        Tool(
            name="terraform_state_list",
            description="List resources in Terraform state",
            inputSchema={
                "type": "object",
                "properties": {
                    "working_dir": {
                        "type": "string",
                        "description": "Working directory for Terraform (optional)",
                        "default": TERRAFORM_DIR
                    }
                }
            }
        )
    ]

async def run_terraform_command(cmd: List[str], working_dir: str = None) -> Dict[str, Any]:
    """Run a terraform command and return result"""
    if working_dir is None:
        working_dir = TERRAFORM_DIR
    
    try:
        result = subprocess.run(
            cmd,
            cwd=working_dir,
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        return {
            "success": result.returncode == 0,
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "command": " ".join(cmd)
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "returncode": -1,
            "stdout": "",
            "stderr": "Command timed out after 5 minutes",
            "command": " ".join(cmd)
        }
    except Exception as e:
        return {
            "success": False,
            "returncode": -1,
            "stdout": "",
            "stderr": str(e),
            "command": " ".join(cmd)
        }

@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """Handle tool calls"""
    working_dir = arguments.get("working_dir", TERRAFORM_DIR)
    
    if name == "terraform_init":
        cmd = ["terraform", "init"]
        result = await run_terraform_command(cmd, working_dir)
        
    elif name == "terraform_plan":
        cmd = ["terraform", "plan"]
        if arguments.get("var_file"):
            cmd.extend(["-var-file", arguments["var_file"]])
        if arguments.get("target"):
            cmd.extend(["-target", arguments["target"]])
        result = await run_terraform_command(cmd, working_dir)
        
    elif name == "terraform_apply":
        cmd = ["terraform", "apply"]
        if arguments.get("var_file"):
            cmd.extend(["-var-file", arguments["var_file"]])
        if arguments.get("auto_approve", False):
            cmd.append("-auto-approve")
        result = await run_terraform_command(cmd, working_dir)
        
    elif name == "terraform_destroy":
        cmd = ["terraform", "destroy"]
        if arguments.get("var_file"):
            cmd.extend(["-var-file", arguments["var_file"]])
        if arguments.get("auto_approve", False):
            cmd.append("-auto-approve")
        result = await run_terraform_command(cmd, working_dir)
        
    elif name == "terraform_validate":
        cmd = ["terraform", "validate"]
        result = await run_terraform_command(cmd, working_dir)
        
    elif name == "terraform_fmt":
        cmd = ["terraform", "fmt"]
        if arguments.get("check", False):
            cmd.append("-check")
        result = await run_terraform_command(cmd, working_dir)
        
    elif name == "terraform_show":
        cmd = ["terraform", "show"]
        if arguments.get("format") == "json":
            cmd.append("-json")
        result = await run_terraform_command(cmd, working_dir)
        
    elif name == "terraform_state_list":
        cmd = ["terraform", "state", "list"]
        result = await run_terraform_command(cmd, working_dir)
        
    else:
        raise ValueError(f"Unknown tool: {name}")
    
    # Format the response
    if result["success"]:
        response = f"✅ Command executed successfully:\n{result['command']}\n\n"
        if result["stdout"]:
            response += f"Output:\n{result['stdout']}\n"
        if result["stderr"]:
            response += f"Warnings:\n{result['stderr']}\n"
    else:
        response = f"❌ Command failed:\n{result['command']}\n\n"
        response += f"Exit code: {result['returncode']}\n"
        if result["stderr"]:
            response += f"Error:\n{result['stderr']}\n"
        if result["stdout"]:
            response += f"Output:\n{result['stdout']}\n"
    
    return [TextContent(type="text", text=response)]

async def main():
    """Main entry point"""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"Server error: {e}")
        sys.exit(1)