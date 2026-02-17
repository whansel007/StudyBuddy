# Shared LLM brain for all pets
import requests
import json

def get_ollama_response(system_prompt, user_message, model="phi3"):
    """
    Sends a request to the local Ollama API and returns the text response.
    """
    url = "http://localhost:11434/api/chat"
    
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        "stream": False
    }
    
    try:
        # Send a POST request to it
        response = requests.post(url, json=payload, timeout=60)
        
        #The status will raise an error if response status is other than 200 OK
        response.raise_for_status()
        
        # Recieve the response
        data = response.json()
        
        #Get the message (if not, return {}) and from that get the content (if not, return "*is speechless")
        return data.get("message", {}).get("content", "*is speechless*")
    
    except requests.exceptions.ConnectionError:
        return "ERROR: Ollama is not running. Please start Ollama."
    except requests.exceptions.Timeout:
        return "ERROR: The pet is thinking too hard... (Request timed out)"
    except Exception as e:
        return f"ERROR: Something went wrong ({str(e)})"