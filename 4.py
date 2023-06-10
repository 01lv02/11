import streamlit as st
import numpy as np
from PIL import Image, ImageOps, ImageFilter, ImageDraw, ImageFont
from PIL import Image, ImageEnhance
import tensorflow as tf

st.set_page_config(page_title="图像编辑器", page_icon=":eyeglasses:")

st.title("图像编辑器")

# 上传一个图像
uploaded_file = st.file_uploader("上传一个图像", type=["png", "jpg", "jpeg"])
if not uploaded_file:
    st.warning("请上传一张图像。")
    st.stop()

original_image = Image.open(uploaded_file)

# 显示原始图像
st.image(original_image, use_column_width=True, caption="原始图像")

# 调整亮度和对比度
brightness = st.slider("亮度", -100, 100, 0, 1) / 100.0
adjusted_image = ImageEnhance.Brightness(original_image).enhance(brightness)

# 滤镜效果
mode = st.sidebar.radio("滤镜效果", ["原图", "模糊", "边缘增强", "浮雕"])
if mode == "模糊":
    filtered_image = adjusted_image.filter(ImageFilter.BLUR)
elif mode == "边缘增强":
    filtered_image = adjusted_image.filter(ImageFilter.FIND_EDGES)
elif mode == "浮雕":
    filtered_image = adjusted_image.filter(ImageFilter.EMBOSS)
else:
    filtered_image = adjusted_image

# 裁剪区域
left = st.sidebar.slider("左边界", 0, filtered_image.width-1, 0, 1)
top = st.sidebar.slider("上边界", 0, filtered_image.height-1, 0, 1)
right = st.sidebar.slider("右边界", left, filtered_image.width-1, filtered_image.width-1, 1)
bottom = st.sidebar.slider("下边界", top, filtered_image.height-1, filtered_image.height-1, 1)
cropped_image = filtered_image.crop((left, top, right, bottom))

# 更改大小
new_size = st.sidebar.slider("更改大小", 0.1, 2.0, 1.0, 0.1)
new_width = int(cropped_image.width * new_size)
new_height = int(cropped_image.height * new_size)
resized_image = cropped_image.resize((new_width, new_height), Image.BICUBIC)

# 更改颜色
new_color = st.sidebar.slider("更改颜色数", 1, 8, value=8, step=1)
color_image = ImageOps.posterize(resized_image, new_color)

# 添加文本
add_text = st.sidebar.checkbox("添加文本")
if add_text:
    text = st.sidebar.text_input("输入文本")
    if text:
        draw = ImageDraw.Draw(color_image)
        font = ImageFont.truetype("arial.ttf", 50)
        text_width, text_height = draw.textsize(text, font)
        text_position = ((color_image.width - text_width) / 2, (color_image.height - text_height) / 2)
        draw.text(text_position, text, fill=(255, 0, 0, 255), font=font)

# 展示最终结果
st.image(color_image, use_column_width=True, caption="最终结果")

# 下载按钮
def download_image():
  download = st.button("点击下载")
  if download:
    with open("edited_image.png", "wb") as f:
      color_image.save(f, "png")
    st.success("图像已下载！")

download_image()