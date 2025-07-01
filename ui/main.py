import asyncio

import streamlit as st
from api_client import create_product, get_product

st.set_page_config(
    page_title="商品管理UI",
    page_icon="🧊",
    layout="centered",
    initial_sidebar_state="auto",
)

st.title("商品管理UI")

# --- 商品検索フォーム ---
st.header("1. 商品をIDで検索")
with st.container(border=True):
    search_product_id = st.number_input(
        label="商品ID",
        min_value=1,
        step=1,
        placeholder="検索したい商品IDを入力してください",
        key="search_product_id",
    )
    search_button = st.button("検索", key="search_button")

    if search_button:
        product_id = search_product_id
        if product_id:
            result = asyncio.run(get_product(product_id))
            if result:
                st.success("商品が見つかりました。")
                st.json(result.model_dump_json(indent=2))
            else:
                st.error(f"商品ID: {product_id} の商品は見つかりませんでした。")
        else:
            st.warning("商品IDを入力してください。")


# --- 商品登録フォーム ---
st.header("2. 新しい商品を登録")
with st.container(border=True):
    create_product_name = st.text_input(
        label="商品名",
        placeholder="商品名を入力してください",
        key="create_product_name",
    )
    create_product_price = st.number_input(
        label="価格（円）",
        min_value=0.0,
        step=100.0,
        placeholder="価格を入力してください",
        key="create_product_price",
        format="%.2f",
    )
    create_button = st.button("登録", key="create_button")

    if create_button:
        name = create_product_name
        price = create_product_price
        if not name:
            st.warning("商品名を入力してください。")
        else:
            result = asyncio.run(create_product(name, price))
            if result:
                st.success("商品を登録しました。")
                st.json(result.model_dump_json(indent=2))
            else:
                st.error("商品の登録に失敗しました。APIサーバーが起動しているか確認してください。")
