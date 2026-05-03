import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
st.set_page_config(page_title="Momen Động Lượng", layout="wide")
st.markdown("<h1 style='text-align: center;'>Khảo sát Quỹ đạo và Momen động lượng</h1>", unsafe_allow_html=True)

# Khai báo biến hình thức t
t, m = sp.symbols('t m')

def calc_with_time():
    cols_params = st.columns([1.3, 1, 0.5, 0.5, 1.4, 2.3, 0.4], vertical_alignment="center")
    t_value = 0.0
    with cols_params[0]: 
        st.subheader("**Thời gian t =**")
    with cols_params[1]: 
        t_value = st.number_input("Thời gian t (s)", value=0.0, step=0.5, label_visibility="collapsed")
    with cols_params[2]: 
        st.subheader("**s**")
    
    return t_value

    

def get_polynomial_coefficients(axis_name):
    st.subheader(f"Nhập phương trình {axis_name}(t):")
    # Tạo các cột để xếp hàng ngang: Nhãn -> Ô nhập -> Nhãn -> Ô nhập...
    # Tỷ lệ cột: [nhãn đầu, ô, nhãn, ô, nhãn, ô, nhãn, ô, nhãn, ô]
    cols = st.columns([0.6, 1, 0.6, 1, 0.6, 1, 0.6, 1, 0.6, 1], vertical_alignment="center")
    
    with cols[0]: st.markdown(f"### {axis_name}(t) = ")
    with cols[1]: c4 = st.number_input("t^4", value=0.0, step=0.1, key=f"{axis_name}4", label_visibility="collapsed")
    with cols[2]: st.markdown("### $t^4 +$")
    with cols[3]: c3 = st.number_input("t^3", value=0.0, step=0.1, key=f"{axis_name}3", label_visibility="collapsed")
    with cols[4]: st.markdown("### $t^3 +$")
    with cols[5]: c2 = st.number_input("t^2", value=0.0, step=0.1, key=f"{axis_name}2", label_visibility="collapsed")
    with cols[6]: st.markdown("### $t^2 +$")
    with cols[7]: c1 = st.number_input("t^1", value=0.0, step=0.1, key=f"{axis_name}1", label_visibility="collapsed")
    with cols[8]: st.markdown("### $t +$")
    with cols[9]: c0 = st.number_input("t^0", value=0.0, step=0.1, key=f"{axis_name}0", label_visibility="collapsed")
    
    return c4*t**4 + c3*t**3 + c2*t**2 + c1*t + c0

def main():

    x_expr = get_polynomial_coefficients("x")
    st.write("")
    y_expr = get_polynomial_coefficients("y")

    st.divider()
    cols_params = st.columns([1.3, 1, 0.5, 0.5, 1.8, 2.3, 0.4], vertical_alignment="center")
    with cols_params[0]: 
        st.subheader("**Khối lượng m =**")
    with cols_params[1]: 
        m_value = st.number_input("Khối lượng m", value=4.0, step=1.0, label_visibility="collapsed")
    with cols_params[2]: 
        st.subheader("**kg**")
    with cols_params[4]: 
        st.subheader("**Khảo sát thời gian t:**")
    with cols_params[5]: 
        t_max = st.slider("Khảo sát thời gian t:", min_value=1.0, max_value=20.0, value=5.0, step=0.5, label_visibility="collapsed")
    with cols_params[6]: 
        st.subheader("**s**")

    st.divider()
    t_value = calc_with_time()
    col_left, col_center, col_right = st.columns([2, 1.1, 2])
    btnSolve = col_center.button("Giải và Vẽ Đồ Thị", type="primary", use_container_width=True)
    if btnSolve:
    
        # Tính vận tốc vx(t) và vy(t) bằng đạo hàm (diff)
        vx_expr = sp.diff(x_expr, t)
        vy_expr = sp.diff(y_expr, t)

        L_expr = m*(x_expr*vy_expr - y_expr*vx_expr)

        L_expr = sp.simplify(L_expr)
        

        xfunc = sp.lambdify(t, x_expr, 'numpy')
        yfunc = sp.lambdify(t, y_expr, 'numpy')
        vxfunc = sp.lambdify(t, vx_expr, 'numpy')
        vyfunc = sp.lambdify(t, vy_expr, 'numpy')
        Lfunc = sp.lambdify((t, m), L_expr, 'numpy')

        
    
        print(f"Vận tốc: vx = {vx_expr}, vy = {vy_expr}")
        st.success(f"**Vận tốc:** $v_x = {sp.latex(vx_expr)}$, $v_y = {sp.latex(vy_expr)}$")
        print(f"Động lượng L = {L_expr}")
        st.success(f"**Động lượng:** $L = {sp.latex(L_expr)}$")
        print(f"Phuong trinh duong di: x = {x_expr}, y = {y_expr}")
        tvalues = np.linspace(0, t_max, 100)
        
        if t_value > 0:
            vx_at_t = vxfunc(t_value)
            vy_at_t = vyfunc(t_value)
            L_at_t = Lfunc(t_value, m_value)

            st.success(f"""
            **Tại thời điểm t = {t_value} s:**
            * Vận tốc: $v_x = {vx_at_t:.2f}$ m/s,  $v_y = {vy_at_t:.2f}$ m/s
            * Momen động lượng: $L = {L_at_t:.2f}$ $kg.m^2/s$
            """)

        xvalues = xfunc(tvalues)
        yvalues = yfunc(tvalues)    
        Lvalues = Lfunc(tvalues, m_value)

        if np.isscalar(Lvalues):
            print("Động lượng góc L là hằng số.")
            Lvalues = np.full_like(tvalues, Lvalues)

        fig1, ax1 = plt.subplots(figsize=(12, 5))

        # Đồ thị 1: Quỹ đạo chuyển động (y theo x)
        ax1.plot(xvalues, yvalues, 'b-', linewidth=2)
        ax1.set_title("Quỹ đạo chuyển động y = y(x)")
        ax1.set_xlabel("x(t) (m)")
        ax1.set_ylabel("y(t) (m)")
        ax1.grid(True)
        st.pyplot(fig1)

        # Đồ thị 2: Biến thiên Momen động lượng theo thời gian
        fig2, ax2 = plt.subplots(figsize=(12, 5))
        ax2.plot(tvalues, Lvalues, 'r-', linewidth=2)
        ax2.set_title("Sự biến thiên của Momen động lượng $L_z$ theo t")
        ax2.set_xlabel("Thời gian t (s)")
        ax2.set_ylabel("$L_z$ (kg.m^2/s)")
        ax2.grid(True)
        st.pyplot(fig2)
        

main()