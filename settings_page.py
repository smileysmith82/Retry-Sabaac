import ui_slider as us
import ui_helpers as uh

volume_slider = us.Slider(
    x = 400,
    y = 300,
    width = 300,
    min_value= 0,
    max_value= 100,
    value= 75,
    step=5

)


ai_turn_speed = us.Slider(
    x=400,
    y=400,
    width= 300,
    min_value= 10,
    max_value=1000,
    value=750,
    step=50 
)

