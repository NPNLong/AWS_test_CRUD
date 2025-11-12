import streamlit as st
import requests
from io import BytesIO
from PIL import Image

BACKEND_URL = "http://host.docker.internal:5000"  # Docker Desktop

DEFAULT_AVATAR = "https://i.pravatar.cc/100?img=1"  # ảnh mặc định nếu URL lỗi

st.title("Danh sách mọi người")

# Lấy danh sách
resp = requests.get(f"{BACKEND_URL}/people")
people = resp.json()

def load_image(url):
    try:
        r = requests.get(url, timeout=3)
        r.raise_for_status()
        return Image.open(BytesIO(r.content))
    except:
        # Nếu lỗi, trả về ảnh mặc định
        r = requests.get(DEFAULT_AVATAR)
        return Image.open(BytesIO(r.content))

for person in people:
    img = load_image(person["avatar_url"])
    st.image(img, width=50)
    st.text(f"{person['id']}: {person['name']}")
    
    cols = st.columns(2)
    with cols[0]:
        if st.button(f"Sửa {person['id']}"):
            new_name = st.text_input("Tên mới", value=person['name'], key=f"name{person['id']}")
            new_avatar = st.text_input("Avatar URL", value=person['avatar_url'], key=f"avatar{person['id']}")
            if st.button("Cập nhật", key=f"update{person['id']}"):
                requests.put(f"{BACKEND_URL}/people/{person['id']}", 
                             json={"name": new_name, "avatar_url": new_avatar})
                st.rerun()
    with cols[1]:
        if st.button(f"Xoá {person['id']}"):
            requests.delete(f"{BACKEND_URL}/people/{person['id']}")
            st.rerun()
# Thêm người mới
st.header("Thêm người mới")
name_new = st.text_input("Tên mới", key="new_name")
avatar_new = st.text_input("Avatar URL", key="new_avatar")
if st.button("Thêm"):
    if name_new:
        requests.post(f"{BACKEND_URL}/people", json={"name": name_new, "avatar_url": avatar_new})
        st.rerun()