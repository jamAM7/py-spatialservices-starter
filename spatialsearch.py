from flows.lot_plan_flow import lot_plan_section_flow
from flows.survey_mark_flow import survey_mark_flow
from flows.navigation import prompt_menu

while (True):
        choice = prompt_menu (
            title="Home Menu",
            options={
                "1": "Lot/Plan/Section",
                "2": "Survey Mark",
                "x": "Exit",
            }
        )
        if choice is None:
            break
        elif choice == '1':
            lot_plan_section_flow()
        elif choice == '2':
            survey_mark_flow()
