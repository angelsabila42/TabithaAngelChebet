#Order Processing
sub_total = 110000
location = 'Gulu'
input_coupon_code = input("Enter coupon code if applicable: \n").strip()

coupon_codes = {
    'E-COMM-56-CUST-01-11062026': 10,
    'E-COMM-65-CUST-01-09062026': 5,
    'E-COMM-57-CUST-01-07062026': 20
}


#Applying discounts as per subTotal price and coupon code if applicable
if sub_total >= 100000 and sub_total < 150000:
    tiered_discount_rate = 10
    if input_coupon_code in coupon_codes:
        coupon_discount_rate = coupon_codes[input_coupon_code]
    elif input_coupon_code == '':
        coupon_discount_rate = 0
    else:
        print("Invalid Coupon Code. Proceeding without applying coupon code...\n")
        coupon_discount_rate = 0
           
elif sub_total >= 150000:
    tiered_discount_rate = 20
    if input_coupon_code in coupon_codes:
        coupon_discount_rate = coupon_codes[input_coupon_code]
    elif input_coupon_code == '':
        coupon_discount_rate = 0
    else:
        print("Invalid Coupon Code. Proceeding without applying coupon code...\n")
        coupon_discount_rate = 0

else:
    tiered_discount_rate = 0
    if input_coupon_code in coupon_codes:
        coupon_discount_rate = coupon_codes[input_coupon_code]
    elif input_coupon_code == '':
        coupon_discount_rate = 0
    else:
        print("Invalid Coupon Code. Proceeding without applying coupon code...\n")
        coupon_discount_rate = 0
        


#Calculations 
tiered_discount = sub_total * tiered_discount_rate/100
sub_total_after_tiered_discount = sub_total - tiered_discount

coupon_discount = sub_total_after_tiered_discount * coupon_discount_rate/100
discount = tiered_discount + coupon_discount
taxable_amount = sub_total - discount

#Finding tax based on location 
match location:
    case 'Kampala':
        tax_rate = 5
    case 'Mbale':
        tax_rate = 3
    case 'Kabale':
        tax_rate = 2
    case _:
        tax_rate = 4

#Applying taxes on taxable amount       
tax = taxable_amount * tax_rate/100
final_price = taxable_amount + tax

#Generating a Receipt            
print("---------------Payment Summary---------------")
print(f"SubTotal:    UGX {sub_total:,}")
print(f"Tiered Discount ({tiered_discount_rate}%):    UGX {tiered_discount:,.0f}")

if coupon_discount_rate > 0:
    print(f"Coupon Discount ({coupon_discount_rate}%):    UGX {coupon_discount:,.0f}")

print("---------------------------------------------")
print(f"Taxable Amount:    UGX {taxable_amount:,.0f}")
print(f"Tax {tax_rate}%:   UGX {tax:,.0f}")
print("---------------------------------------------")
print(f"Final Amount:    UGX {final_price:,.0f}")
    





