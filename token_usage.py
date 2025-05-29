# token_usage.py

def extract_token_usage(response):
    usage = response.get("usage", {})
    return {
        "prompt_tokens": usage.get("prompt_tokens", 0),
        "completion_tokens": usage.get("completion_tokens", 0),
        "total_tokens": usage.get("total_tokens", 0)
    }

def estimate_cost(prompt_tokens, completion_tokens, model="gpt-3.5-turbo"):
    # Prices are in USD per 1K tokens
    pricing = {
        "gpt-3.5-turbo": {
            "prompt": 0.0005,
            "completion": 0.0015
        }
    }

    model_pricing = pricing.get(model, {"prompt": 0.0, "completion": 0.0})
    cost = (prompt_tokens * model_pricing["prompt"] + completion_tokens * model_pricing["completion"]) / 1000
    return round(cost, 6)
