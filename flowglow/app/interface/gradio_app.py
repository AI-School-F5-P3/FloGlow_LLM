import gradio as gr
from typing import Dict, Any
from app.core.models import ContentRequest, Platform, ContentType
from app.core.config import settings

class FlowGlowInterface:
    """Gradio interface for FlowGlow content generator"""
    
    def __init__(self):
        self.generator = ContentGenerator()
    
    def create_interface(self) -> gr.Interface:
        """Create and configure Gradio interface"""
        
        interface = gr.Interface(
            fn=self._generate_content,
            inputs=[
                gr.Dropdown(
                    choices=[p.value for p in Platform],
                    label="Platform",
                    info="Select your target platform"
                ),
                gr.Textbox(
                    label="Topic",
                    placeholder="Enter your content topic..."
                ),
                gr.Textbox(
                    label="Target Audience",
                    placeholder="Describe your target audience..."
                ),
                gr.Dropdown(
                    choices=["professional", "casual", "formal", "friendly"],
                    label="Tone",
                    value="professional"
                ),
                gr.Dropdown(
                    choices=["en", "es", "fr", "it"],
                    label="Language",
                    value="en"
                )
            ],
            outputs=gr.Textbox(label="Generated Content"),
            title="FlowGlow Content Generator",
            description="Generate platform-optimized content with AI",
            theme=gr.themes.Soft()
        )
        
        return interface
    
    def _generate_content(self, platform: str, topic: str, 
                         audience: str, tone: str, language: str) -> str:
        """Handle content generation request"""
        try:
            request = ContentRequest(
                platform=platform,
                topic=topic,
                audience=audience,
                tone=tone,
                language=language
            )
            
            response = self.generator.generate(request)
            return response.content
            
        except Exception as e:
            return f"Error generating content: {str(e)}"

def launch_app():
    """Launch the Gradio application"""
    interface = FlowGlowInterface()
    app = interface.create_interface()
    app.launch(share=True)