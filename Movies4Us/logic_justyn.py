import backend

#def generate_sales_report():
       # TODO: Compile stats for the staff dashboard and report log
        #return {"total_sales": 10, "revenue": 150.00}

def calculate_revenue():
       total = 0
       for sale in backend.SALES_HISTORY:
           price = backend.PRICES[sale["type"]]
           total += price * sale["amount"]      
       return total
print(calculate_revenue())