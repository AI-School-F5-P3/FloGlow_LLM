import gradio as gr
from typing import Dict, Any, Tuple, Optional
from app.core.models import ContentRequest, Platform, ContentType
from app.core.config import settings
from app.core.llm_handler import LLMHandler

class FlowGlowInterface:
    def __init__(self):
        self.generator = LLMHandler()
    
    def create_interface(self) -> gr.Interface:
        with gr.Blocks(title="FlowGlow Content Generator") as interface:
            gr.Markdown("# FlowGlow Content Generator")
            gr.Markdown("Generate platform-optimized content with AI")
            
            with gr.Row():
                with gr.Column(scale=2):
                    platform = gr.Dropdown(
                        choices=[p.value for p in Platform],
                        label="Platform",
                        info="Select your target platform",
                        value="blog"
                    )
                    topic = gr.Textbox(
                        label="Topic",
                        placeholder="Enter your content topic..."
                    )
                    audience = gr.Textbox(
                        label="Target Audience",
                        placeholder="Describe your target audience..."
                    )
                    tone = gr.Dropdown(
                        choices=["professional", "casual", "formal", "friendly"],
                        label="Tone",
                        value="professional"
                    )
                    language = gr.Dropdown(
                        choices=["en", "es", "fr", "it"],
                        label="Language",
                        value="en"
                    )
                
                with gr.Column(scale=1):
                    include_image = gr.Checkbox(
                        label="Include Image",
                        value=True
                    )
                    image_size = gr.Radio(
                        choices=["small", "regular", "large"],
                        label="Image Size",
                        value="regular",
                        visible=True
                    )
                    image_orientation = gr.Radio(
                        choices=["landscape", "portrait", "squarish"],
                        label="Image Orientation",
                        value="landscape",
                        visible=True
                    )

            with gr.Row():
                clear_btn = gr.Button("Clear")
                submit_btn = gr.Button("Generate Content", variant="primary")

            with gr.Row():
                output = gr.Textbox(
                    label="Generated Content",
                    lines=10,
                    interactive=False
                )

            with gr.Row():
                image_output = gr.Image(
                    label="Generated Image",
                    show_label=True
                )

            def update_image_controls(include_imgs):
                return {
                    image_size: gr.update(visible=include_imgs),
                    image_orientation: gr.update(visible=include_imgs)
                }

            async def generate_content(
                platform, topic, audience, tone, lang, 
                include_imgs, img_size, img_orientation
            ):
                try:
                    request = ContentRequest(
                        platform=platform,
                        topic=topic,
                        audience=audience,
                        tone=tone,
                        language=lang
                    )
                    
                    content, image_url = await self.generator.generate(
                        str(request),
                        include_image=include_imgs,
                        image_params={
                            "size": img_size,
                            "orientation": img_orientation
                        }
                    )
                    
                    return content, image_url
                    
                except Exception as e:
                    return f"Error generating content: {str(e)}", None

            def clear_outputs():
                return "", None

            include_image.change(
                fn=update_image_controls,
                inputs=[include_image],
                outputs=[image_size, image_orientation]
            )

            submit_btn.click(
                fn=generate_content,
                inputs=[
                    platform, topic, audience, tone, language,
                    include_image, image_size, image_orientation
                ],
                outputs=[output, image_output]
            )
            
            clear_btn.click(
                fn=clear_outputs,
                outputs=[output, image_output]
            )

        return interface

def launch_app():
    interface = FlowGlowInterface()
    app = interface.create_interface()
    app.launch(share=True)

if __name__ == "__main__":
    launch_app()