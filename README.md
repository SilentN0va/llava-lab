curl -fsSL https://raw.githubusercontent.com/ollama/ollama/main/scripts/install.sh | sh && \
ollama pull llava:7b && \
sudo apt update && \
sudo apt install -y python3-pip python3-venv imagemagick && \
mkdir -p ~/llava-lab && \
cd ~/llava-lab && \
python3 -m venv venv && \
source venv/bin/activate && \
pip install --upgrade pip && \
pip install ollama pillow && \
