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

## Example Interactions

**Weather Questions:**
```
You: "What's the weather like in Seattle?"
Assistant: "Let me check the weather in Seattle for you..." *uses weather tool*

You: "Is it raining in London?"
Assistant: "I'll look up the current weather in London..." *uses weather tool*
```

**Regular Chat:**
```
You: "Hello!"
Assistant: "Hi there! How can I help you today?"

You: "How are you?"
Assistant: "I'm doing great, thanks for asking! Need any weather info or just want to chat?"
```

## Technical Details

- Built with LangGraph for workflow management
- One simple weather tool
- Basic state management for conversation flow
- Clean, straightforward implementation

## File Structure
```
weather_assistant/
├── assistant.py       # Main LangGraph implementation
├── tools.py          # Weather tool
├── requirements.txt  # Dependencies
└── README.md         # This file
```

## Success Criteria

The assistant should:
- Start without errors
- Check weather when asked
- Have normal conversations otherwise
- Route correctly between chat and weather lookup
- Be friendly and helpful
