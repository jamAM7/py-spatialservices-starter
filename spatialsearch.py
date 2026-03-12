from api.address import get_address_info
from api.lot import get_lot_info
from api.survey_marks import get_survey_mark_info


while (True):
    print("Enter 'x' to exit")
    address = input("Enter an address: ")
    if (address == "x" or address == "X"):
        break

    address_result = get_address_info(address.upper())
    print ("Address Results: \n" + str(address_result) + "\n")

    lot_result = get_lot_info(address_result["x"], address_result["y"])
    print ("Lot Results: \n" + str(lot_result) + "\n")

    # survey_mark_result = get_survey_mark_info(float(address_result["x"]), float(address_result["y"]))
    survey_mark_result = get_survey_mark_info(address_result["x"], address_result["y"])
    print ("Survey Mark Results: \n" + str(survey_mark_result) + "\n")

    # 87a bunarba road gymea bay