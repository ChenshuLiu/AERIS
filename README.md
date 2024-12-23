# AERIS

## TLDR
**AERIS** pronounced as [/ˈɛərɪs/](https://www.vondy.com/phonetically-spell-my-name-generator--FC574ueB?lc=5), stands for "**A**daptive **E**motional **R**esponse and **I**nteractive **S**ystem", which is an AI-in-the-loop emotionally-aware personal assistant powered by light-weight language model that can locally deploy. The smart personal assistant is can detect your emotions through micro-movements and facial expressions with a built-in emotion detector driven by mediapipe, and can provide empathetic responses.

## Deployment
1. The chatbot to be deployed locally is based on **Ollama**, so first [download ollama](https://ollama.com/) to your PC accordingly.
2. Depending on the computation capacity of your device, you can choose the open-source model you would like to locally deploy. For demonstration purpose, I am using llama3
```
ollama pull llama3
```
3. Change to directory of your project. Create virtual environment and load the dependencies according to `AERIS_requirements.txt`.
```
python -m venv [name of virtual environment]
source [name of virtual environment]/bin/activate
pip install -r ./AERIS_requirements.txt
```
4. Run the `main.py` file in the model folder.
```
python ./AERIS_v1/main.py
```