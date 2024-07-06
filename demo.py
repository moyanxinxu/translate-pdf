import base64

import gradio as gr


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


def translate_and_display(text, chat_history):
    translated_text = text[::-1]  # 这里替换成你实际的翻译逻辑
    chat_history.append((text, translated_text))
    return "", chat_history


def clear_text(txt2translate, chatbox):
    return "", [], gr.update(visible=False)


with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column(scale=2):  # PDF栏占比更大
            output_pdf = gr.HTML("从上传PDF文件开始...")
        with gr.Column():
            with gr.Row():
                input_pdf = gr.File(label="上传PDF文件")
                explorer = gr.FileExplorer(
                    label="选择PDF文件", file_count="single", glob="*.pdf"
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
    translate_btn.click(
        translate_and_display,
        [txt2translate, chatbox],
        [txt2translate, chatbox],
    )
    clear_btn.click(clear_text, [txt2translate, chatbox], [txt2translate, chatbox])


demo.launch()
