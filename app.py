import streamlit as st

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Mini Amazon Demo",
    page_icon="🛒",
    layout="wide"
)

st.title("🛒 Mini Amazon Demo")
st.write("A simple Amazon-style product demo built with Streamlit.")

# ---------- SAMPLE DATA ----------
products = [
    {
        "id": 1,
        "name": "Wireless Mouse",
        "category": "Electronics",
        "price": 599,
        "rating": 4.3,
        "description": "Comfortable wireless mouse with 2.4 GHz connectivity."
    },
    {
        "id": 2,
        "name": "Mechanical Keyboard",
        "category": "Electronics",
        "price": 2499,
        "rating": 4.7,
        "description": "RGB backlit mechanical keyboard for gaming and typing."
    },
    {
        "id": 3,
        "name": "Water Bottle 1L",
        "category": "Home & Kitchen",
        "price": 299,
        "rating": 4.1,
        "description": "BPA-free plastic bottle, perfect for daily use."
    },
    {
        "id": 4,
        "name": "Running Shoes",
        "category": "Fashion",
        "price": 1999,
        "rating": 4.5,
        "description": "Lightweight running shoes with good cushioning."
    },
    {
        "id": 5,
        "name": "Coffee Mug",
        "category": "Home & Kitchen",
        "price": 199,
        "rating": 4.0,
        "description": "Ceramic mug, microwave and dishwasher safe."
    },
]

# ---------- SESSION STATE FOR CART ----------
if "cart" not in st.session_state:
    st.session_state.cart = {}  # {product_id: quantity}


def add_to_cart(prod_id):
    if prod_id in st.session_state.cart:
        st.session_state.cart[prod_id] += 1
    else:
        st.session_state.cart[prod_id] = 1


def get_product_by_id(pid):
    for p in products:
        if p["id"] == pid:
            return p
    return None


# ---------- SIDEBAR: FILTERS + CART ----------
st.sidebar.header("Filters")

# Category filter
categories = ["All"] + sorted(list({p["category"] for p in products}))
selected_category = st.sidebar.selectbox("Category", categories)

# Search bar
search_query = st.sidebar.text_input("Search products")

# Sort options
sort_by = st.sidebar.selectbox(
    "Sort by",
    ["Relevance", "Price: Low to High", "Price: High to Low", "Rating: High to Low"]
)

st.sidebar.markdown("---")
st.sidebar.header("🛍 Your Cart")

cart_items = st.session_state.cart
if not cart_items:
    st.sidebar.write("Cart is empty.")
else:
    total_amount = 0
    for pid, qty in cart_items.items():
        p = get_product_by_id(pid)
        if p:
            line_total = p["price"] * qty
            total_amount += line_total
            st.sidebar.write(f"{p['name']} x {qty}  — ₹{line_total}")
    st.sidebar.markdown(f"**Total: ₹{total_amount}**")
    if st.sidebar.button("Clear Cart"):
        st.session_state.cart = {}


# ---------- FILTER + SORT PRODUCTS ----------
filtered = products

# Category filter
if selected_category != "All":
    filtered = [p for p in filtered if p["category"] == selected_category]

# Search filter
if search_query:
    q = search_query.lower()
    filtered = [
        p for p in filtered
        if q in p["name"].lower() or q in p["description"].lower()
    ]

# Sorting
if sort_by == "Price: Low to High":
    filtered = sorted(filtered, key=lambda x: x["price"])
elif sort_by == "Price: High to Low":
    filtered = sorted(filtered, key=lambda x: x["price"], reverse=True)
elif sort_by == "Rating: High to Low":
    filtered = sorted(filtered, key=lambda x: x["rating"], reverse=True)
# "Relevance" -> no extra sorting


# ---------- MAIN AREA: PRODUCT GRID ----------
st.subheader("Products")

if not filtered:
    st.write("No products found. Try changing filters or search query.")
else:
    # Show products in a simple grid (3 per row)
    cols_per_row = 3
    for i in range(0, len(filtered), cols_per_row):
        row_products = filtered[i:i + cols_per_row]
        cols = st.columns(len(row_products))
        for col, product in zip(cols, row_products):
            with col:
                st.markdown(f"### {product['name']}")
                st.markdown(f"**₹{product['price']}**")
                st.markdown(f"⭐ {product['rating']}")
                st.caption(product["category"])
                st.write(product["description"])
                if st.button("Add to Cart", key=f"add_{product['id']}"):
                    add_to_cart(product["id"])
                    st.success("Added to cart!")


# ---------- FOOTER ----------
st.markdown("---")
st.caption("This is a demo app and not an official Amazon website.")
