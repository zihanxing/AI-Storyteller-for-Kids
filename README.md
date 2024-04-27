# Imaginative Tales - An AI Storyteller for Kids with Visual Narratives
Individual Project for the course AIPI540 of the Master of Engineering in AI at Duke University, Spring 2024

## Project Description
This project aims to create an AI storyteller for kids with visual narratives. Story is generated based on kids' preferences, and images are generated based on kids' preferred art style. The project is designed to be interactive and engaging for kids. Solving the problem of needing to create a **personalized, engaging, diverse, and interactive** story for kids, this project will provide a solution that can be used by parents, teachers, and kids themselves.

**You can access the app [here](https://imaginativetales.streamlit.app/).**

## Features
1. **Personalized Storytelling**: The AI will generate a story based on kids' preferences.
2. **Visual Narratives**: The AI will generate images based on kids' preferred art style chosen from Disney and DC Comics.
3. **Interactive and Engaging**: The project is designed to be interactive and engaging for kids.
4. **Childlike Voice**: A childlike voice will read the story out loud, just like a friend telling a story.

## Main Components
- **Text Generation**: GPT-4
- **Image Generation**: SDXL + LORA
- **Text-to-Speech**: lova.ai

a overall architecture of the project is shown below:
![](<assets/overview.png>)

## Repository Structure
```
.
├── README.md 
├── Tell_story.py       # the main script to run the project
├── assets              # used to store the audio files
├── data                # all the training data
│   ├── DC_samples.zip
│   ├── disney_original_images
│   ├── disney_resized_images
│   ├── original_images
│   └── resized_images
├── requirements.txt
├── scripts
│   ├── requirements_sdxl.txt   # the requirements for the training script
│   ├── resize.py       # a script to resize the training images
│   ├── train.sh        # a bash script to train the model
│   └── train_dreambooth_lora_sdxl.py   # the main script to train the model
├── static
└── tools               
    ├── difussion.py    # a testing refernece script
    ├── helper.py       # a helper script to play the audio automatically
    ├── storyteller.py  # the main script to generate the story
    └── text2speech.py  # a script to convert text to speech
```

## To run the app locally
1. Clone the repository
```bash
git clone git@github.com:zihanxing/SDXL-lora-for-kids.git
```
2. Install the required packages
```bash
pip install -r requirements.txt
```
3. Run the project
```bash
streamlit run Tell_story.py
```

## To train the model
You have to equip with a powerful GPU to train the model. The training process is time-consuming and resource-intensive. The following steps are for reference only.
1. Clone the repository
```bash
git clone git@github.com:zihanxing/SDXL-lora-for-kids.git
```
2. Get into the scripts folder
```bash
cd scripts
```
3. Install the required packages
```bash
pip install -r requirements_sdxl.txt
```
4. Modify the `train.sh` file to specify the parameters and paths for training
5. Run the training script
```bash
bash train.sh
```

