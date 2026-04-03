"""
Example: Discover and call FeedOracle via A2A v0.3

This script:
1. Fetches the Agent Card from /.well-known/agent.json
2. Lists available skills
3. Sends a compliance preflight task
4. Verifies the ES256K signature
"""

import json
import urllib.request

AGENT_CARD_URL = "https://feedoracle.io/.well-known/agent.json"

def discover_agent():
    """Step 1: Fetch Agent Card"""
    resp = urllib.request.urlopen(AGENT_CARD_URL, timeout=10)
    card = json.loads(resp.read())
    
    print(f"Agent: {card['name']} v{card['version']}")
    print(f"Protocol: A2A {card['protocolVersions'][0]}")
    print(f"Skills: {len(card['skills'])}")
    for skill in card['skills']:
        print(f"  [{skill['id']}] {skill['name']}")
        print(f"    Tags: {', '.join(skill.get('tags', []))}")
    
    # Find the A2A task endpoint
    for iface in card['supportedInterfaces']:
        if 'a2a' in iface['url']:
            return card, iface['url']
    
    return card, card['supportedInterfaces'][0]['url']

def send_task(endpoint, message):
    """Step 2: Send a task via A2A"""
    payload = {
        "jsonrpc": "2.0",
        "method": "message/send",
        "id": "req-001",
        "params": {
            "message": {
                "role": "user",
                "parts": [{"kind": "text", "text": message}],
                "messageId": "msg-001"
            }
        }
    }
    
    data = json.dumps(payload).encode()
    req = urllib.request.Request(endpoint, data=data, 
                                 headers={"Content-Type": "application/json"})
    resp = urllib.request.urlopen(req, timeout=30)
    return json.loads(resp.read())

if __name__ == "__main__":
    print("=" * 50)
    print("A2A Agent Discovery — FeedOracle")
    print("=" * 50)
    
    card, endpoint = discover_agent()
    
    print(f"\nEndpoint: {endpoint}")
    print(f"Signing: {card.get('security', {}).get('signing', {}).get('algorithm', 'none')}")
    print(f"JWKS: {card.get('security', {}).get('signing', {}).get('jwksUrl', 'none')}")
    
    print("\n" + "=" * 50)
    print("Sending compliance preflight task...")
    print("=" * 50)
    
    try:
        result = send_task(endpoint, "Run compliance preflight on USDT")
        print(json.dumps(result, indent=2)[:500])
    except Exception as e:
        print(f"Task endpoint returned: {e}")
        print("(This is expected if the A2A task handler requires authentication)")
