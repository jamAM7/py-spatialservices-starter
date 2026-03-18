from api.address import get_address_info
from api.lot import get_lot_info
from api.survey_marks import get_survey_mark_info
from api.plan import get_plan_info


while (True):
    print("Enter 'x' to exit")
    address = input("Enter an address: ")
    if (address == "x" or address == "X"):
        break

    address_result = get_address_info(address.upper())
    print ("Address Results: \n" + str(address_result) + "\n")

    lot_result = get_lot_info(address_result["x"], address_result["y"])
    print("Lot Results: \n")
    for result in lot_result:
        print(str(result) + "\n")
    #print ("Lot Results: \n" + str(lot_result) + "\n")

    # survey_mark_result = get_survey_mark_info(float(address_result["x"]), float(address_result["y"]))
    survey_mark_result = get_survey_mark_info(address_result["x"], address_result["y"])
    print("Survey Mark Results: \n" )
    for mark in survey_mark_result:
        print (str(mark) + "\n")

    print("Press enter to skip")
    plan_number = input("Enter an plannumber to find its metadata: ")
    if (plan_number != ''):
        # plan_result = get_plan_info(plan_number)
        # for plan in plan_result:
        #     print (str(plan) + "\n")
        plan_result = get_plan_info(plan_number)
        if plan_result:
            for key, value in plan_result.items():
                print(f"{key}: {value}")
        print("\n")