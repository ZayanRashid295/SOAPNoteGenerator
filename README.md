# SOAP Note Generator

The **SOAP Note Generator** is a Python-based application that leverages multiple AI APIs via OpenRouter to automatically generate structured SOAP (Subjective, Objective, Assessment, Plan) notes from doctor-patient conversations. It supports multiple LLMs for comparative analysis.

---

## ✨ Features
- **Multi-API Integration**:  
  - DeepSeek | Gemma | Meta Llama | Microsoft MAI-DS-R1 | OpenAI
- **Asynchronous Processing**:  
  - Parallel API calls via `httpx` + `asyncio` for faster generation
- **Customizable Input**:  
  - Accepts raw conversation text or audio transcripts
- **Smart Evaluation**:  
  - Auto-selects best SOAP note based on completeness/clarity scoring
- **Error Resilience**:  
  - Fallback mechanisms and detailed logging

---

## ⚙️ Installation

### Prerequisites
- Python 3.8+
- API keys for at least one supported model

### Setup
```bash
# Clone repository
git clone https://github.com/ZayanRashid295/SOAPNoteGenerator.git
cd SOAPNoteGenerator

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Add your API keys to .env
```

---

## 🚀 Usage

### Basic Generation
```bash
python main.py --input conversations/CAR0004.txt
```

### Advanced Options
```bash
# Specify preferred models (comma-separated)
python main.py -i input.txt --models deepseek,gemma

# Save output to file
python main.py -i input.txt -o output.json

# Enable verbose logging
python main.py -i input.txt --debug
```

---

## 📂 Project Structure
```
SOAP/
├── __pycache__/               # Python bytecode cache (auto-generated)
├── conversations/             # Sample doctor-patient dialogues
│   └── CAR0004.txt            # Example conversation file
├── output/                    # Generated SOAP notes (PDF/JSON)
├── venv/                      # Virtual environment (optional)
│
├── Core Modules/
│   ├── api_clients.py         # API integrations (DeepSeek/Gemma/etc)
│   ├── comparison_engine.py   # Scores and compares SOAP notes
│   ├── explanation_generator.py  # Analyzes results
│   └── pdf_generator.py       # Creates printable outputs
│
├── Tests/
│   ├── test_api_clients.py    # API connection tests
│   ├── test_deepseek.py       # DeepSeek-specific tests
│   ├── test_gemma.py          # Gemma-specific tests
│   ├── test_meta_llama.py     # Llama-specific tests
│   └── test_openai_gpt_41.py  # OpenAI-specific tests
│
├── main.py                    # Entry point
└── requirements.txt           # Dependency list
```

---

## 🔧 Configuration
Edit `.env` to customize:
```ini
# Required (at least one API key)
DEEPSEEK_API_KEY=your_key_here
OPENROUTER_API_KEY=your_key_here

# Optional
MAX_TOKENS=1000                # Response length limit
TIMEOUT=30                     # API timeout in seconds
```

---

## 📊 Supported Models
| Model            | Context | Specialization          | Requirements |
|------------------|---------|-------------------------|--------------|
| DeepSeek-V3      | 128K    | Medical terminology     | API Key      |
| Microsoft MAI-DS-R1 | ?      | Clinical domain-focused | Azure Access |
| Gemma-7B         | 8K      | General purpose         | OpenRouter   |
| Llama-3-70B      | 8K      | Balanced performance    | OpenRouter   |

---

## 🤝 Contributing
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit changes (`git commit -m 'Add new feature'`)
4. Push to branch (`git push origin feature/improvement`)
5. Open a Pull Request

