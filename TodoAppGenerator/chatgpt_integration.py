import ast
import json
from collections import deque
from typing import List, Dict, Tuple, Deque, Union

import openai


openai.api_key = '<openai_api_key>'


MAX_RETRIES = 3


class ChatMemory:
    def __init__(self, max_length: int = 10):
        """Initialize with a maximum number of stored messages."""
        self.messages: Deque[Dict] = deque(maxlen=max_length)

    def add_message(self, role: str = None, content: str = None, messages: List[Dict] = None):
        """
        Add either a single message or a list of messages.

        Args:
        - role: "user" or "assistant".
        - content: Message text.
        - messages: List of message dicts.
        """
        if messages:
            for message in messages:
                if not message.get("content") or not message.get("role"):
                    raise ValueError("Both 'role' and 'content' fields must be provided in the message.")
                self.messages.append(message)
        else:
            if not role or not content:
                raise ValueError("Both 'role' and 'content' fields must be provided.")
            self.messages.append({"role": role, "content": content})

    def get_messages(self) -> List[Dict]:
        """Return the list of stored messages."""
        return list(self.messages)


chat_memory = ChatMemory()


def send_gpt_message(
    messages: List[Dict] = None,
    content: str = None,
    add_history: bool = True,
    model: str = "gpt-4",
) -> str:
    # Handling chat history
    chat_history = chat_memory.get_messages()
    gpt_message = chat_history

    if add_history:
        chat_memory.add_message(messages=messages, content=content, role="user")

    # Finding the right gpt_message to send
    if content:
        gpt_message += [{"role": "user", "content": content}]
    elif messages:
        gpt_message += messages
    else:
        raise Exception("No gpt message was given, failed to send gpt message.")

    print(f"Sending gpt_message: {gpt_message}")

    retry_counter = 0
    while retry_counter < MAX_RETRIES:
        try:
            response = openai.chat.completions.create(
                model=model,
                messages=gpt_message,
            )

            user_response = response.choices[0].message.content

            if add_history:
                chat_memory.add_message(role="system", content=user_response)

            # print(f"User response is: {user_response}")
            return user_response
        except Exception as exc:
            retry_counter += 1
            print(f"""
                Failed to send request to gpt api: {gpt_message}. \n 
                The reason is: {exc}. \n
                Retrying #{retry_counter}...
            """)

