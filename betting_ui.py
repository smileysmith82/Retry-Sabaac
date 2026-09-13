import ui_buttons as ub
import ui_helper as uh
import styles as st
import betting as btg


raise_button = ub.Button(
    "Raise",
    st.WIDTH - 200,
    st.HEIGHT - 100,
    150,
    50,
    st.DARK_BLUE,
    st.WHITE
)
change_button = btg.set_button_text()

no_change_button = ub.Button(
    change_button,
    st.WIDTH - 400,
    st.HEIGHT - 100,
    150,
    50,
    st.DARK_BLUE,
    st.WHITE
)
    