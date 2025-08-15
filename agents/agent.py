#!/usr/bin/env python3
"""
Agent Entry Point
"""

import sys
from agent_helper import initialize_agent

if __name__ == "__main__":
    role_to_assign = None
    if len(sys.argv) > 1:
        role_to_assign = sys.argv[1]

    initialize_agent(role_to_assign)
