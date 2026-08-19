import omni.ext
import omni.ui as ui
import json
import urllib.request
import threading

class EyricAIExtension(omni.ext.IExt):
    def on_startup(self, ext_id):
        print("[omni.eyric.ai] Eyric AI Extension starting up")

        self._window = ui.Window("Eyric AI Assistant", width=300, height=300)
        with self._window.frame:
            with ui.VStack(spacing=5):
                ui.Label("Ask NVIDIA Cloud AI", height=20, alignment=ui.Alignment.CENTER)
                
                self._input_field = ui.StringField(height=20)
                self._input_field.model.set_value("What is Omniverse?")
                
                def on_click():
                    prompt = self._input_field.model.get_value_as_string()
                    self._output_label.text = "Thinking..."
                    # Run API call in a background thread to avoid blocking the Omniverse UI
                    threading.Thread(target=self._call_nvidia_api, args=(prompt,)).start()

                ui.Button("Generate with Llama 3.1 8B", clicked_fn=on_click, height=30)
                
                # Scrollable area for output
                with ui.ScrollingFrame(horizontal_scrollbar_policy=ui.ScrollBarPolicy.SCROLLBAR_ALWAYS_OFF):
                    self._output_label = ui.Label("AI Output will appear here.", word_wrap=True)

    def _call_nvidia_api(self, prompt):
        url = "https://integrate.api.nvidia.com/v1/chat/completions"
        api_key = "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"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "meta/llama-3.1-8b-instruct",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
            "max_tokens": 512
        }
        
        try:
            req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers)
            with urllib.request.urlopen(req, timeout=30) as response:
                result = json.loads(response.read().decode('utf-8'))
                text = result['choices'][0]['message']['content']
                self._output_label.text = text
        except Exception as e:
            self._output_label.text = f"Error: {str(e)}"

    def on_shutdown(self):
        print("[omni.eyric.ai] Eyric AI Extension shutting down")
        if self._window:
            self._window.destroy()
            self._window = None
