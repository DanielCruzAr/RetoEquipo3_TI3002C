import streamlit as st

def main():
    st.title("My Streamlit App")
    
    #  Add sidebar
    st.sidebar.header("Calor y Control")
    option = st.sidebar.selectbox("Menu", ["Home", "Ventas", "Compras"])

    if option == "Home":
        st.subheader("Home")
    elif option == "Ventas":
        st.subheader("Ventas")
    elif option == "Compras":
        st.subheader("Compras")

if __name__ == "__main__":
    main()
