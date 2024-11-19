# PDF2PPT: Academic Paper to Presentation Converter

PDF2PPT is an AI-powered tool that automatically converts academic papers (PDF) into structured PowerPoint presentations while maintaining technical accuracy and logical flow. It leverages OpenAI's GPT-4 for content analysis and generates comprehensive presentations with proper figure integration.

## Features

- Automatic extraction of paper structure and content
- Comprehensive figure analysis and integration
- Maintains technical accuracy and paper's logical flow
- Rich content summarization with evidence and implications
- Automatic PowerPoint generation with proper formatting
- Support for multi-panel figures and technical details

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/pdf2ppt.git
cd pdf2ppt
```

2. Create and activate a virtual environment:
```bash
python -m venv pdf2ppt
source pdf2ppt/bin/activate  # On Windows: pdf2ppt\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up OpenAI API key:
Create a `.env` file in the project root and add your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

## Usage

Run the script with your PDF file:
```bash
python main.py
```

When prompted, enter the path to your PDF file or a URL. The script will:
1. Extract figures from the PDF
2. Analyze the paper's content and structure
3. Generate a comprehensive PowerPoint presentation
4. Save the presentation in the `output` directory

## Project Structure

```
pdf2ppt/
├── src/
│   ├── __init__.py
│   ├── content_analyzer.py
│   ├── document_processor.py
│   ├── figure_extractor.py
│   └── presentation_generator.py
├── output/
│   └── figures/
├── main.py
├── requirements.txt
└── README.md
```

## Requirements

- Python 3.8+
- OpenAI API key
- Dependencies listed in requirements.txt:
  - PyMuPDF
  - opencv-python-headless
  - python-pptx
  - openai
  - python-dotenv
  - Pillow
  - numpy

## Limitations

- Requires OpenAI API access and credits
- Processing time depends on paper length
- Figure extraction quality depends on PDF format
- May require manual verification for complex technical content

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- OpenAI for GPT-4 API
- PyMuPDF for PDF processing
- python-pptx for presentation generation
- All contributors and users of this project

## Citation

If you use this tool in your research, please cite:
```bibtex
@software{pdf2ppt2024,
  author = {Your Name},
  title = {PDF2PPT: Academic Paper to Presentation Converter},
  year = {2024},
  url = {https://github.com/yourusername/pdf2ppt}
}
``` 
