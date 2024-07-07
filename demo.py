import base64

import gradio as gr
from gradio_client import Client

client = Client("https://s5k.cn/api/v1/studio/yangbaosong/Qwen_Turbo_MT/gradio/")
source = "English"
target = "Chinese"

def pdf2base64(file):
    if file is None:
        return "从上传PDF文件开始..."
    else:
        with open(file, "rb") as f:
            encoded_pdf = base64.b64encode(f.read()).decode("utf-8")
        return f"""
                    <iframe src="data:application/pdf;base64,{encoded_pdf}"
                            width="100%"
                            height="800px">
                    </iframe>
                    """


def change_source_language(sorce_language):
    global source
    if sorce_language == "英文":
        source = "English"
    elif sorce_language == "中文":
        source = "Chinese"


def change_target_language(target_language):
    global target
    if target_language == "中文":
        target = "Chinese"
    elif target_language == "英文":
        target = "English"


def translate_and_display(text, chat_history):
    global source, target
    result = client.predict(
        text,  # str  in 'Input' Textbox component
        source,  # Literal['Chinese', 'English', 'Japanese', 'Korean', 'Thai', 'French', 'German', 'Spanish', 'Arabic', 'Indonesian', 'Vietnamese', 'Portuguese']  in 'Source Language' Dropdown component
        target,  # Literal['Chinese', 'English', 'Japanese', 'Korean', 'Thai', 'French', 'German', 'Spanish', 'Arabic', 'Indonesian', 'Vietnamese', 'Portuguese']  in 'Target Language' Dropdown component
        "",
        "",
        "",
        "",
        "",
        "",
        api_name="/model_chat",
    )
    chat_history.append((text, result))
    return "", chat_history


def clear_text(txt2translate, chatbox):
    return "", [], gr.update(visible=False)


with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column(scale=2):  # PDF栏占比更大
            output_pdf = gr.HTML("从上传PDF文件开始...")
        with gr.Column():
            with gr.Tab(label="传递PDF文件"):
                input_pdf = gr.File(label="上传PDF文件")
                explorer = gr.FileExplorer(
                    label="选择PDF文件", file_count="single", glob="*.pdf"
                )
            with gr.Tab(label="文本翻译"):
                with gr.Row():
                    with gr.Column():
                        with gr.Row():
                            sorce_language = gr.Dropdown(
                                value="英文", choices=["英文", "中文"], label="源语言"
                            )
                            target_language = gr.Dropdown(
                                value="中文", choices=["中文", "英文"], label="目标语言"
                            )
                with gr.Row():
                    txt2translate = gr.Textbox(
                        label="输入",
                        placeholder="从PDF复制或输入文本以进行翻译",
                    )

                    with gr.Column():
                        with gr.Row():
                            translate_btn = gr.Button(value="翻译")
                            clear_btn = gr.Button(value="清空")
                with gr.Column():
                    chatbox = gr.Chatbot(
                        show_copy_button=True,
                    )

    input_pdf.change(pdf2base64, input_pdf, output_pdf)
    explorer.change(pdf2base64, explorer, output_pdf)
    sorce_language.change(change_source_language, sorce_language)
    target_language.change(change_target_language, target_language)
    translate_btn.click(
        translate_and_display,
        [txt2translate, chatbox],
        [txt2translate, chatbox],
    )
    clear_btn.click(clear_text, [txt2translate, chatbox], [txt2translate, chatbox])


demo.launch()
