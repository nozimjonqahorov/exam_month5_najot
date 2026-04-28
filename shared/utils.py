import requests
from decimal import Decimal  # SHU QATORNI QO'SHING

def get_exchange_rates():
    api_key = "9499b02b139f4c1987e58f15"
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/UZS"
    
    try:
        response = requests.get(url)  # SUROV junatadi api-ga
        data = response.json()               #dictionary qilib olamiz apidan kelgan javobni
        if data["result"] == "success":       # agar request succes bolib malumot olib kelsa,
            return data["conversion_rates"]    #dictionarydan  bizga keraklirates qismini ratesni olamiz masalan 1$ = 12.340 
    except Exception as e:                              
        print(f"API xatosi: {e}") 
    
    return {"USD": 0.000079, "UZS": 1.0}  #default qiymat api ishlamasa

def convert_currency(amount, from_curr, to_curr, rates):
    if from_curr.upper() == to_curr.upper():
        return amount
    
    
    from_rate = Decimal(str(rates.get(from_curr.upper(), 1)))   #Kurslarni Decimal turiga o'tkazamiz
    to_rate = Decimal(str(rates.get(to_curr.upper(), 1)))
    
    # Hisoblash mantiqi
    if from_curr.upper() == "UZS":
        return amount * to_rate
    else:
        # Avval UZSga o'tkazib, keyin maqsadli valyutaga o'giramiz
        amount_in_uzs = amount / from_rate
        return amount_in_uzs * to_rate