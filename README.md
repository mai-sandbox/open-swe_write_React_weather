# open-swe_write_React_weather

A simple AI assistant built with LangGraph that can chat with you and check the weather when needed.

## Overview

This is a basic chatbot that focuses on two things: having conversations and helping you check the weather. It's designed to be as simple as possible while demonstrating core LangGraph concepts.

## What It Can Do

### 🌤️ Weather Lookup
- Get current weather for any city you ask about
- Understands natural weather questions
- Provides helpful weather information

### 💬 Natural Conversation
- Chat about various topics
- Responds naturally to greetings and questions
- Maintains a friendly, helpful tone

## How It Works

The assistant automatically knows when you're asking about weather vs. just wanting to chat. It's smart enough to:
- Detect weather-related questions
- Use the weather tool when needed
- Have normal conversations otherwise

The agent should be able to talk to user and answer any question related to weather using the weather tool.

## Technical Details

- Built with LangGraph for workflow management
- One simple weather tool
- Basic state management for conversation flow
- Clean, straightforward implementation


## Success Criteria

The assistant should:
- Start without errors
- Check weather when asked
- Have normal conversations otherwise
- Route correctly between chat and weather lookup
- Be friendly and helpful
