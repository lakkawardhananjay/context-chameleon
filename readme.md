<div align="center">
  <img src="https://user-images.githubusercontent.com/12345/some-banner-image.png" alt="Context Chameleon Banner" width="600"/>
  <br/>
  <h1>Context Chameleon</h1>
  <p><strong>Transform Your Product into Marketing Gold with AI-Powered Context Generation</strong></p>
  
  <p>
    <!-- Core Status Badges -->
    <img src="https://img.shields.io/badge/Status-Hackathon_Prototype-blue" alt="Status: Hackathon Prototype">
    <img src="https://img.shields.io/badge/Powered_By-Bria_FIBO-purple" alt="Powered By: Bria FIBO">
    <br/>
    <!-- Tech Stack Badges -->
    <a href="#"><img src="https://img.shields.io/badge/Python-3.12+-blue.svg" alt="Python 3.12+"></a>
    <a href="#"><img src="https://img.shields.io/badge/Framework-Streamlit-red.svg" alt="Streamlit"></a>
    <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License: MIT"></a>
    <a href="#"><img src="https://img.shields.io/github/last-commit/your-username/context-chameleon" alt="Last Commit"></a>
  </p>
</div>

---

> A Streamlit web application that transforms a single product image into a variety of professional, high-resolution (8K) marketing assets using a two-stage AI process.

<br/>

<p align="center">
  <em>(Your App Demo GIF Here)</em>
  <br/>
  <sup>A brief demonstration of uploading a product and generating marketing assets.</sup>
</p>

## 📋 Table of Contents
- [📋 Table of Contents](#-table-of-contents)
- [🚀 About The Project](#-about-the-project)
- [✨ Key Features](#-key-features)
  - [Available Marketing Vibes](#available-marketing-vibes)
- [🛠️ Technology Stack](#️-technology-stack)
- [🏁 Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Application](#running-the-application)
- [🎈 Usage](#-usage)
- [📂 Project Structure](#-project-structure)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

## 🚀 About The Project

Creating compelling marketing assets is a time-consuming and expensive process. Small businesses and marketers often struggle to produce a variety of high-quality images needed for different platforms and campaigns. **Context Chameleon** solves this problem by leveraging a powerful two-stage AI pipeline to automate the creation of stunning, context-aware marketing visuals.

Simply upload a single product image, and let our AI do the heavy lifting.

1.  **🔍 Analysis:** Google's advanced Gemini Vision API analyzes your product image to understand its every detail—content, lighting, composition, and key subjects.
2.  **🎨 Generation:** The Bria FIBO API then uses this rich analysis to generate brand-new, high-quality marketing images based on your selected "vibe" and customizations, delivering professional results in stunning 8K resolution.

## ✨ Key Features

| Feature | Description |
| :--- | :--- |
| 🤖 **AI-Powered Generation** | Uses a sophisticated Gemini + Bria pipeline to create context-aware marketing assets from a single image. |
| 🖼️ **High-Resolution Output** | Delivers all generated images in stunning **8K resolution**, ready for professional print or digital use. |
| 🎭 **Variety of "Vibes"** | Choose from a curated list of marketing contexts to instantly change the look and feel of your assets. |
| 🔧 **Customizable Options** | Fine-tune generations with specific camera angles and dynamic consumption scenarios. |
| 🍾 **Intelligent Scenarios** | Automatically handles details like removing bottle caps for pouring/drinking scenes and adds contextual elements for different product types. |
| 🚫 **Negative Prompts** | Provides granular control by allowing the exclusion of unwanted elements from the generated images. |

### Available Marketing Vibes

| Vibe | Emoji | Description |
| :--- | :---: | :--- |
| **Marketplace Clean** | 🛒 | For e-commerce product listings with a pure white background. |
| **Consumption/Active** | 🧗 | Showcases your product in real-world use with dynamic scenarios (e.g., Pouring, Drinking, Hand Holding). |
| **Insta Lifestyle** | 📸 | For aesthetic, influencer-style shots with natural lighting and soft focus. |
| **Midnight Luxury** | 🌃 | A moody, cinematic vibe with neon/dark lighting in an urban context. |
| **Hero Spotlight** | ✨ | Creates a dramatic, high-contrast "hero shot" for premium product emphasis. |
| **Tech Abstract** | 🔮 | A clean, futuristic look with cool lighting, perfect for electronics and modern gadgets. |


## 🛠️ Technology Stack

- **Backend:** Python
- **Web Framework:** Streamlit
- **AI Services:**
  - Google Gemini API
  - Bria FIBO API
- **Image Processing:** Pillow

## 🏁 Getting Started

Follow these steps to get the project up and running on your local machine.

### Prerequisites

- Python 3.12 or higher
- An environment with `pip`

### Installation

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/your-username/context-chameleon.git
    cd context-chameleon
    ```

2.  **Create and activate a virtual environment:**
    - **Windows:**
      ```sh
      python -m venv venv
      venv\Scripts\activate
      ```
    - **macOS & Linux:**
      ```sh
      python3 -m venv venv
      source venv/bin/activate
      ```

3.  **Install the dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

4.  **Set up your API keys:**
    - Create a file named `.env` in the root of the project.
    - Add your API keys to the `.env` file like this:
      ```env
      GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
      BRIA_API_KEY="YOUR_BRIA_API_KEY"
      ```

### Running the Application

Once you've installed the dependencies and set up your API keys, run the application with this command:

```sh
streamlit run app.py
```

## 🎈 Usage

1.  **Upload Image:** Use the file uploader to select an image of your product.
2.  **Analyze Image:** Click the "Analyze Image" button to let Gemini understand your product.
3.  **Select Vibes:** Choose one or more marketing vibes from the selection.
4.  **Customize:** Adjust the options for each vibe (e.g., select a "Pouring" scenario for the Consumption vibe).
5.  **Generate:** Click "Generate Campaign Assets" and watch the AI create your new marketing images.

## 📂 Project Structure

<details>
<summary>Click to view the project structure</summary>

```
.
├── .env
├── app.py
├── readme.md
├── requirements.txt
├── assets/
│   ├── angles/
│   └── consumption/
├── config/
│   ├── __init__.py
│   ├── consumption_data.py
│   ├── settings.py
│   └── vibe_configs.py
├── services/
│   ├── __init__.py
│   ├── bria_service.py
│   ├── gemini_service.py
│   └── image_service.py
├── ui/
│   ├── __init__.py
│   ├── components.py
│   └── styles.py
└── utils/
    ├── __init__.py
    └── session_state.py
```
</details>

## 🤝 Contributing

Contributions are welcome! If you have any ideas, suggestions, or bug reports, please open an issue or submit a pull request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.