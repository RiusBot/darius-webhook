

def acdc_parse(json_data: dict) -> dict:
    
    symbol = json_data["instId"].split('-')[0]
    action = json_data['side'].upper()
    entry = float(json_data.get('currentprice', 0))
    stop_loss = float(json_data['slTriggerPx'])
    take_profit = float(json_data['tpTriggerPx'])
    
    return {
        "symbol": [symbol],
        "action": action,
        "entry": entry,
        "stop_loss": stop_loss,
        "take_profit": take_profit,
    }