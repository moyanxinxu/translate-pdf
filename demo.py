import base64

import gradio as gr
from gradio_client import Client

API_URL = "https://s5k.cn/api/v1/studio/yangbaosong/Qwen_Turbo_MT/gradio/"
client = Client(API_URL)


def pdf2base64(file):
    """将PDF文件转换为base64编码的字符串。"""
    if file is None:
        return "从上传PDF文件开始..."
    else:
        try:
            with open(file, "rb") as f:
                encoded_pdf = base64.b64encode(f.read()).decode("utf-8")
            return f"""
                        <iframe src="data:application/pdf;base64,{encoded_pdf}"
                                width="100%"
                                height="800px">
                        </iframe>
                        """
        except Exception as e:
            return f"PDF文件加载失败: {e}"


def translate_text(text, source_language, target_language):
    """调用翻译API进行翻译。"""
    try:
        result = client.predict(
            text,
            source_language,
            target_language,
            "",
            "",
            "",
            "",
            "",
            "",
            api_name="/model_chat",
        )
        return result
    except Exception as e:
        return f"翻译失败: {e}"


def update_chat_history(text, translation, chat_history):
    """更新聊天记录。"""
    chat_history.append((text, translation))
    return chat_history


def clear_text(txt2translate, chatbox):
    """清空文本框和聊天记录。"""
    return "", [], gr.update(visible=False)


with gr.Blocks() as demo:
    source_language = gr.State("English")
    target_language = gr.State("Chinese")

    with gr.Row():
        with gr.Column(scale=2):
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
                            source_dropdown = gr.Dropdown(
                                value="英文", choices=["英文", "中文"], label="源语言"
                            )
                            target_dropdown = gr.Dropdown(
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

    def update_source_language(value):
        if value == "英文":
            return "English"
        elif value == "中文":
            return "Chinese"

    def update_target_language(value):
        if value == "中文":
            return "Chinese"
        elif value == "英文":
            return "English"

    input_pdf.change(pdf2base64, input_pdf, output_pdf)
    explorer.change(pdf2base64, explorer, output_pdf)
    source_dropdown.change(update_source_language, source_dropdown, source_language)
    target_dropdown.change(update_target_language, target_dropdown, target_language)

    def translate_and_update(text, chat_history, source, target):
        translation = translate_text(text, source, target)
        return "", update_chat_history(text, translation, chat_history)

    translate_btn.click(
        translate_and_update,
        [txt2translate, chatbox, source_language, target_language],
        [txt2translate, chatbox],
    )
    clear_btn.click(clear_text, [txt2translate, chatbox], [txt2translate, chatbox])

demo.launch()
