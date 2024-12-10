import gradio as gr
from typing import Dict, Any
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
                with gr.Column():
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

            with gr.Row():
                clear_btn = gr.Button("Clear")
                submit_btn = gr.Button("Generate Content", variant="primary")

            output = gr.Textbox(
                label="Generated Content",
                lines=10,
                interactive=False
            )

            async def generate_content(platform, topic, audience, tone, lang):
                try:
                    request = ContentRequest(
                        platform=platform,
                        topic=topic,
                        audience=audience,
                        tone=tone,
                        language=lang
                    )
                    
                    content = await self.generator.generate(str(request))
                    return content
                    
                except Exception as e:
                    return f"Error generating content: {str(e)}"

            def clear_outputs():
                return ""

            submit_btn.click(
                fn=generate_content,
                inputs=[platform, topic, audience, tone, language],
                outputs=output
            )
            
            clear_btn.click(
                fn=clear_outputs,
                outputs=[output]
            )

        return interface

def launch_app():
    interface = FlowGlowInterface()
    app = interface.create_interface()
    app.launch(share=True)

if __name__ == "__main__":
    launch_app()